import logging
import os

# Snowflake libraries
import snowflake.connector
from sqlalchemy import create_engine
from sqlalchemy.dialects import registry
registry.register('snowflake', 'snowflake.sqlalchemy', 'dialect')

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