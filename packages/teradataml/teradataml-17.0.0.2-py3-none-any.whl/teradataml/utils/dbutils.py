"""
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: rameshchandra.d@teradata.com
Secondary Owner:

teradataml db utilities
----------
A teradataml database utility functions provide interface to Teradata Vantage common tasks such as drop_table, drop_view, create_table etc.
"""
import pandas as pd
import teradataml.context.context as tdmlctx
from teradataml.common.utils import UtilFuncs
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.constants import TeradataTableKindConstants
from teradataml.common.sqlbundle import SQLBundle

def drop_table(tablename):
    """
    Drops the table from the current database.

    PARAMETERS:
        tablename - The table name which needs to be dropped from the current database.

    RETURNS:
        True - if the operation is successful.

    RAISES:
        TeradataMlException - If the table doesn't exist.

    EXAMPLES:
        drop_table('mytable')
        drop_table('mydb.mytable')
        drop_table("mydb"."mytable")
    """
    if tablename is None or not tablename or type(tablename) is not str:
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_TABLE_NAME_ARGS), MessageCodes.INVALID_TABLE_NAME_ARGS)

    try:
        return UtilFuncs._drop_table(tablename)
    except TeradataMlException:
        raise
    except Exception as err:
        raise TeradataMlException(Messages.get_message(MessageCodes.DROP_TABLE_FAILED),
                                      MessageCodes.DROP_TABLE_FAILED) from err

def list_db_tables(schema_name = None, table_name = None, table_kind = 'all'):
    """
    List the table names from the specified schema name.

    PARAMETERS:
        schema_name - The Name of schema in the database. The default value is the current database name.
        table_name -  The pattern to be used to filtering the table names from the database.
                      The table name argument can contain '%' as pattern matching charecter.For example '%abc'
                      will return all table names starting with any charecters and ending with abc.
        table_kind -  The table kind to apply the filter. The valid values are 'all','table','view','volatile','temp'. The default value is 'all'.
                      all - list the all the table kinds.
                      table - list only tables.
                      view - list only views.
                      volatile - list only volatile temp.
                      temp - list all teradata ml temporary objects created in the specified database.
    RETURNS:
        Panda's DataFrame - if the operation is successful.

    RAISES:
        TeradataMlException - If the tablekind argument is provided with invalid values. Or if any database sql errors occures during processing.

    EXAMPLES:
        list_db_tables()
        list_db_tables('db1', 'abc_%', None)
        list_db_tables(None, 'abc_%', 'all')
        list_db_tables(None, 'abc_%', 'table')
        list_db_tables(None, 'abc_%', 'view')
        list_db_tables(None, 'abc_%', 'volatile')
        list_db_tables(None, 'abc_%', 'temp')
    """
    if tdmlctx.get_connection() is None:
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_CONTEXT_CONNECTION), MessageCodes.INVALID_CONTEXT_CONNECTION)

    if table_kind is None or not table_kind or type(table_kind) is not str:
        raise TeradataMlException(Messages.get_message(MessageCodes.ARG_EMPTY, 'table_kind'),
                                          MessageCodes.ARG_EMPTY)

    if not table_kind in [TeradataTableKindConstants.ALL.value, TeradataTableKindConstants.TABLE.value, TeradataTableKindConstants.VIEW.value, TeradataTableKindConstants.VOLATILE.value,TeradataTableKindConstants.TEMP.value]:
        raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                          str(table_kind), 'table_kind', 'all,table,view,volatile or temp'),
                                          MessageCodes.INVALID_ARG_VALUE)

    try:
        return _get_select_table_kind(schema_name, table_name, table_kind)
    except TeradataMlException:
        raise
    except Exception as err:
        raise TeradataMlException(Messages.get_message(MessageCodes.LIST_DB_TABLES_FAILED),
                                      MessageCodes.LIST_DB_TABLES_FAILED) from err


def _get_select_table_kind(schema_name, table_name, table_kind):
    """
    Get the list of the table names from the specified schema name.

    PARAMETERS:
        schema_name - The Name of schema in the database. The default value is the current database name.
        table_name -  The pattern to be used to filtering the table names from the database.
                      The table name argument can contain '%' as pattern matching charecter.For example '%abc'
                      will return all table names starting with any charecters and ending with abc.
        table_kind -  The table kind to apply the filter. The valid values are 'all','table','view','volatile','temp'.
                      all - list the all the table kinds.
                      table - list only tables.
                      view - list only views.
                      volatile - list only volatile temp.
                      temp - list all teradata ml temporary objects created in the specified database.
    RETURNS:
        Panda's DataFrame - if the operation is successful.

    RAISES:
        Database error if an error occurred while executing query.

    EXAMPLES:
        _get_select_table_kind("schema_name", "table_name", "all")
    """
    object_name_str = None
    if table_name is not None:
        object_name_str = "'{0}'".format(table_name)
    object_table_kind = None

    # Check the schema name.
    if schema_name is None:
        schema_name = tdmlctx._get_current_databasename()

    # Check the table kind.
    if (table_kind == TeradataTableKindConstants.VOLATILE.value):
        query = SQLBundle._build_help_volatile_table()
    else:
        # Tablekind:
        # 'O' - stands for Table with no primary index and no partitioning
        # 'Q' - stands for Queue table
        # 'T' - stands for a Table with a primary index or primary AMP index, partitioning, or both.
        #       Or a partitioned table with NoPI
        # 'V' - stands for View
        if (table_kind == TeradataTableKindConstants.TABLE.value):
            object_table_kind = "'{0}','{1}','{2}'".format('O', 'Q', 'T')
        elif (table_kind == TeradataTableKindConstants.VIEW.value):
            object_table_kind = "'{0}'".format('V')
        elif (table_kind == TeradataTableKindConstants.TEMP.value):
            if table_name is None:
                object_name_str = "'{0}'".format(TeradataTableKindConstants.ML_PATTERN.value)
            else:
                object_name_str = "'{0}','{1}'".format(table_name,TeradataTableKindConstants.ML_PATTERN.value)
        else:
            object_table_kind = "'{0}','{1}','{2}','{3}'".format('O', 'Q', 'T', 'V')
        query = SQLBundle._build_select_table_kind(schema_name, object_name_str, object_table_kind)

    try:
        pddf = pd.read_sql(query, tdmlctx.td_connection.connection)
        # Check if all table kind is requested and add also volatile tables to the pdf.
        if (table_kind == TeradataTableKindConstants.ALL.value):
            try:
                #add volatile tables to all dataframe.
                vtquery = SQLBundle._build_help_volatile_table()
                vtdf = pd.read_sql(vtquery, tdmlctx.td_connection.connection)
                if not vtdf.empty:
                    vtdf.rename(columns={TeradataTableKindConstants.VOLATILE_TABLE_NAME.value: TeradataTableKindConstants.REGULAR_TABLE_NAME.value}, inplace=True)
                    frames = [pddf, vtdf[[TeradataTableKindConstants.REGULAR_TABLE_NAME.value]]]
                    pddf = pd.concat(frames)
                    pddf.reset_index(drop=True, inplace=True)
            except Exception as err:
                pass #no volatle tables exist.
        if (table_kind == TeradataTableKindConstants.VOLATILE.value):
            pddf.rename(columns={TeradataTableKindConstants.VOLATILE_TABLE_NAME.value: TeradataTableKindConstants.REGULAR_TABLE_NAME.value}, inplace=True)
            return pddf[[TeradataTableKindConstants.REGULAR_TABLE_NAME.value]]
        else:
            return pddf
    except Exception as err:
        return pd.DataFrame()