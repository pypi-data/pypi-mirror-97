"""Defines all functions within the RDS (relational DB service) module."""

# Standard library imports
from logging import getLogger
from traceback import format_exc
from time import time
from configparser import ConfigParser
from re import match

# Related third party imports
import psycopg2
from sqlalchemy import create_engine, Table, MetaData, exc
from sqlalchemy.engine import reflection
from numpy import dtype
from pandas import (
    DataFrame,
    read_sql_query,
    to_datetime,
    to_numeric,
    StringDtype,
    BooleanDtype,
    Int64Dtype,
    Int32Dtype,
)


def config(
    file_path: str = "/home/ec2-user/SageMaker/.config/database.ini",
    section: str = "maximo",
) -> dict:
    """Get database credentials from stored .ini file.

    The following config() function reads in the database.ini file and
    returns the connection parameters as a dictionary. This function will be
    imported in to the main python script.

    Arguments:
        file_path       - Path to the database.ini-file required to initiate
                          connection.
        section         - Section of database.ini-file where the
                          connection-parameters are stored.
    Returns:
        db_cred         - All connection parameters in the specified file_path
                          and section

    """
    parser = ConfigParser()  # Create a parser
    parser.read(file_path)  # Read config file
    db_cred = {}  # Get section, default to postgresqs

    if parser.has_section(section):  # Checks to see (section) parser exists
        params = parser.items(section)
        for param in params:
            db_cred[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {file_path} file")
    return db_cred


def check_connection(db_cred: dict):
    """Check connection settings against DB and print version of postgreSQL.

    Arguments:
        db_cred (dict)  - Connection parameters from config file or manually
                          defined dictionary

    """
    connection = None

    # Initiate Logger
    logger = getLogger(__name__)
    logger.info("Checking DB Connection:")

    try:
        # Setup connection
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        dsn_para = connection.get_dsn_parameters()

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()

        # Construct connection string
        logger.info("DSN Parameters: %s.", dsn_para)
        logger.info("\tConnection information: %s.", record)

    except psycopg2.Error as error:
        # Catch, logg and raise specific psycopg2 errors
        logger.error("Error while connecting to PostgreSQL, %s.", error)
        raise error

    finally:
        # Closing DB-connection (if initiated)
        if connection:
            cursor.close()
            connection.close()
            logger.info("\tConnection is closed.")
        else:
            logger.info("\tNo connection initiated.")


def import_data(
    sql_query: str,
    db_cred: dict,
    df_meta: DataFrame = None,
    post_rename: dict = None,
    convert_dtypes: bool = True,
    query_name: str = None,
) -> DataFrame:
    """Load data from RDS instance.

    The function runs the provided sql_query against the database specified
    in the db_cred dictionary. If df_meta-DataFrame is provided and
    convert_dtypes = True (default), the function will also convert all columns
    to optimal Pandas dtype according to the provided meta data.

    Arguments:
        sql_query (str)         - SQL-query to run
        db_cred (dict)          - Connection parameters from config file
        df_meta (DataFrame)     - DataFrame with schema information from
                                  import_meta_data function
        post_rename (dict)      - Dictionary for renaming dictionaries after
                                  dtype conversion
        convert_dtypes (bool)   - Flag if data types should be converted using
                                  the data base schema for the used table
        query_name (str)        - Name of query to be executed (only for
                                  logging purposes).
    Returns:
        df_ (DataFrame)         - DataFrame with loaded data

    """
    connection = None

    # Initiate Logger
    logger = getLogger(__name__)
    start = time()

    if query_name:
        logger.info("Loading %s Data:", query_name)
    else:
        logger.info("Loading Data:")

    # Get data from DB
    try:
        connection = psycopg2.connect(**db_cred)
        cursor = connection.cursor()
        df_ = read_sql_query(sql_query, connection)

        logger.info(
            "\tOK! Query executed in %f [s]. Shape = %s" "",
            time() - start,
            df_.shape,
        )

    except psycopg2.Error as error:
        logger.error("Error while connecting to PostgreSQL, %s, %s",
                     error,
                     format_exc())
        raise error

    finally:
        if connection:
            cursor.close()
            connection.close()
            logger.info("\tConnection is closed")

    # Convert dtype to pandas 1.0> compatible dtypes
    if (df_meta is not None) & (convert_dtypes):
        for col, data_dtype in df_.dtypes.iteritems():

            # Check schema
            df_meta_sub = df_meta.loc[
                df_meta.name == col,
            ]

            if df_meta_sub.empty is False:

                # If there are more than one schema type present in df_meta
                if df_meta_sub.type.nunique() > 1:
                    schema_dtype = df_meta_sub.type.value_counts().index[0]
                    logger.warning(
                        "\t'%s' has multiple dtypes "
                        "in schema. Using most popular dtype "
                        " %s for conversion",
                        col,
                        schema_dtype,
                    )
                else:
                    schema_dtype = df_meta_sub.type.unique()[0]

                # Int64s
                if schema_dtype == "BIGINT":
                    df_[col] = df_[col].astype(Int64Dtype())

                # Int32s
                elif schema_dtype == "INTEGER":
                    df_[col] = df_[col].astype(Int32Dtype())

                # Bools
                elif schema_dtype == "BOOLEAN":
                    df_[col] = df_[col].astype(BooleanDtype())

                # Float64s
                elif schema_dtype == "DOUBLE PRECISION":
                    df_[col] = to_numeric(
                        df_[col], errors="coerce", downcast="float"
                    )

                # Float64s
                elif bool(
                    match(
                        r"NUMERIC\([0-9]{1,6},\s[0-9]{1,6}\)", schema_dtype
                    )
                ):
                    df_[col] = to_numeric(
                        df_[col], errors="coerce", downcast="float"
                    )

                # Float 32s
                elif schema_dtype == "REAL":
                    df_[col] = to_numeric(
                        df_[col], errors="coerce", downcast="float"
                    )

                # PostgreSQL provides users with the interval data type
                # that allows users to store and manipulate a time period.
                elif schema_dtype == "INTERVAL":
                    # Implement better solution for this dtype when needed
                    df_[col] = df_[col].astype(StringDtype())

                # Dates and timestamps
                elif schema_dtype == "DATE":
                    df_[col] = to_datetime(
                        df_[col],
                        infer_datetime_format=True,
                        utc=True,
                        errors="raise",
                    )

                elif schema_dtype == "TIMESTAMP WITHOUT TIME ZONE":
                    if data_dtype == dtype("O"):
                        df_[col] = to_datetime(
                            df_[col],
                            infer_datetime_format=True,
                            utc=True,
                            errors="raise",
                        )

                elif schema_dtype == "TIMESTAMP WITH TIME ZONE":
                    if data_dtype == dtype("O"):
                        df_[col] = to_datetime(
                            df_[col],
                            infer_datetime_format=True,
                            utc=True,
                            errors="raise",
                        )
                # Strings
                elif schema_dtype in ["TEXT"] or bool(
                    match(r"VARCHAR\([0-9]{1,6}\)", schema_dtype)
                ):
                    df_[col] = df_[col].astype(StringDtype())

                # Raise error if conversion hasn't been implemented
                else:
                    raise_str = f"\tData conversion '{schema_dtype}' not \
                                implemented. Please contact package \
                                administrator"
                    logger.critical(raise_str)
                    raise Exception(raise_str)
            else:
                logger.warning("\tNo dtype for %s found in schema", col)
    elif df_meta is None:
        logger.warning(
            "\tNo dtype conversion was executed. Meta data"
            " (df_meta) not passed to function"
        )

    # Remove Timezone info from datetime tags
    for col in df_.select_dtypes(include="datetime64[ns, UTC]").columns:
        df_[col] = df_[col].dt.tz_localize(None)

    # Post rename
    if post_rename:
        df_ = df_.rename(columns=post_rename)

    return df_


def import_meta_data(
    db_cred: dict, like_str: str = "maximoworker"
) -> DataFrame:
    """Import schema to pandas DataFrame.

    The functions main purpose is to import data type for all tables containing
    the like_str argument in the db accociated with the passed credentials.

    Arguments:
        db_cred (dict)  - Dictionary containing all login information either
                          manually entered or using the config function of
                          the exergi-package.
        like_str (str)  - List all tables with table_name starting with
                          this string. (default: "maximoworker")

    Keyword Arguments:
        kwargs          - Key word arguments passed to create_engine from
                          sqlalchemy

    Returns:
        df_meta   - DataFrame containing

    """
    # Initiate Logger
    logger = getLogger(__name__)
    logger.info("Loading Meta Data:")
    start = time()

    try:
        engine = create_engine(
            "postgresql+psycopg2://{}:{}@{}/{}".format(
                db_cred["user"],
                db_cred["password"],
                db_cred["host"],
                db_cred["database"],
            )
        )

        # Get metadata
        metadata = MetaData(bind=engine)
        insp = reflection.Inspector.from_engine(engine)
        tables = [
            t for t in insp.get_table_names(schema="public") if like_str in t
        ]

        # Test if any tables were found
        assert len(tables) > 0, "No meta data for tables matching " \
            f"{like_str} found."

        # Store metadata in Pandas DataFrame
        df_meta = DataFrame(
            data=[
                {
                    "table": t,
                    "name": c.name,
                    "type": str(c.type),
                    "python_type": c.type.python_type,
                    "nullable": c.nullable,
                }
                for t in tables
                for c in Table(
                    t, metadata, autoload=True, autoload_with=engine
                ).columns
            ]
        )

        # Set dtypes
        df_meta = df_meta.astype(
            {
                "table": StringDtype(),
                "name": StringDtype(),
                "type": StringDtype(),
                "nullable": bool,
            }
        )
        # Log results
        logger.info(
            """\tOK! Query executed in %.3f [s]. Shape = %s""",
            (time() - start),
            df_meta.shape,
        )

    except exc.SQLAlchemyError as error:
        logger.info("\tSQL Alchemy Error while querying data, %s", error)
        raise error

    except psycopg2.Error as error:
        logger.info("\tPsycopg 2 Error while querying data, %s", error)
        raise error

    finally:
        if engine:
            logger.info("\tConnection is closed")
            engine.dispose()

    return df_meta
