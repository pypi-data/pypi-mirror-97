"""Defines all functions within the snowflake module."""


import logging
import os

import pandas as pd

# Snowflake libraries
import snowflake.connector
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry

registry.register("snowflake", "snowflake.sqlalchemy", "dialect")


def execute_query(
    sql_query: str,
):
    """Execute query on Snowflake.

    Please note that the following environment variables must have been set:
        - SNOWFLAKE_USER
        - SNOWFLAKE_PASSWORD
        - SNOWFLAKE_ACCOUNT
        - SNOWFLAKE_WH
        - SNOWFLAKE_DB
        - SNOWFLAKE_SCHEMA

    Arguments:
        sql_query (str) - Query to execute
    Returns:
        None
    """
    logger = logging.getLogger()

    # Setup connection
    ctx = snowflake.connector.connect(
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        warehouse=os.environ["SNOWFLAKE_WH"],
        database=os.environ["SNOWFLAKE_DB"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )

    # Execute query
    cs = ctx.cursor()
    cs.execute(sql_query)
    ctx.close()


def upload_df(
    df_: pd.DataFrame,
    table_name: str,
    **kwargs,
):
    """Upload DataFrame to Snowflake using SQLalchemy and Pandas.to_sql()

    Arguments:
            df_ (pd.DataFrame) - Dataframe to be written.
            table_name (str)   - Table name in Snowflake.
            **kwargs ()        - Key-word arguments for the to_sql() method.
    Returns:
        None
    """
    logger = logging.getLogger()

    # Fill in your SFlake details here
    engine = create_engine(
        snowflake.sqlalchemy.URL(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            warehouse=os.environ["SNOWFLAKE_WH"],
            database=os.environ["SNOWFLAKE_DB"],
            schema=os.environ["SNOWFLAKE_SCHEMA"],
        )
    )

    connection = engine.connect()

    # Make sure index is False, Snowflake doesnt accept indexes
    df_.to_sql(table_name, con=engine, index=False, **kwargs)

    connection.close()
    engine.dispose()
