"""
Copyright (c) 2020 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: Rohit.Khurd@teradata.com
Secondary Owner:

teradataml Model Cataloging utilities
-------------------------------------
The teradataml Model Cataloging utility functions provide internal utilities that
the Model Cataloging APIs make use of.
"""
import importlib
import warnings
import pandas as pd
import re

from teradataml.common.constants import ModelCatalogingConstants as mac,\
    FunctionArgumentMapperConstants as famc
from teradataml.common.constants import TeradataConstants
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.utils import UtilFuncs
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.messages import Messages
from teradataml.context.context import get_context, _get_current_databasename
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.catalog.function_argument_mapper import _argument_mapper
from teradataml.common.sqlbundle import SQLBundle
from teradatasqlalchemy import CLOB
from teradatasqlalchemy.dialect import preparer, dialect as td_dialect
from sqlalchemy.sql.expression import select, case as case_when
from sqlalchemy import func


def __get_arg_sql_name_from_tdml(function_arg_map, arg_type, name):
    """
    DESCRIPTION:
        Internal function to find SQL equivalent name for given teradataml name.

    PARAMETERS:
        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

        arg_type:
            Required Argument.
            Specifies a string representing the type of lookup, one of the keys in the function argument map.
            Acceptable values: 'arguments', 'inputs', 'outputs'
            Types: str

        name:
            Required Argument.
            Specifies the teradataml input, output, or argument name to lookup.
            Types: str

    RETURNS:
        A String representing the SQL equivalent name for the teradataml name passed as input.

    EXAMPLES:
        >>> sql_name = __get_arg_sql_name_from_tdml(function_arg_map, arg_type, name)
    """
    if name in function_arg_map[arg_type][famc.TDML_TO_SQL.value]:
        sql_name = function_arg_map[arg_type][famc.TDML_TO_SQL.value][name]

        if isinstance(sql_name, dict):
            sql_name = sql_name[famc.TDML_NAME.value]

        if isinstance(sql_name, list):
            sql_name = sql_name[0]

        return sql_name

    # No SQL name found for given teradataml input name
    return None


def __get_arg_tdml_name_from_sql(function_arg_map, arg_type, name):
    """
    DESCRIPTION:
        Internal function to find teradataml equivalent name and type, if any, for given SQL name.

    PARAMETERS:
        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

        arg_type:
            Required Argument.
            Specifies a string representing the type of lookup, one of the keys in the function argument map.
            Acceptable values: 'arguments', 'inputs', 'outputs'
            Types: str

        name:
            Required Argument.
            Specifies the SQL input, output, or argument name to lookup.
            Types: str

    RETURNS:
        * A String representing the teradataml equivalent name for the SQL name when arg_type
          is 'inputs' or 'outputs'.
        * A dictionary with tdml_name and tdml_type for the SQL name when arg_type
          is 'arguments'.


    EXAMPLES:
        >>> tdml_name = __get_arg_tdml_name_from_sql(function_arg_map, arg_type, name)
    """
    if name in function_arg_map[arg_type][famc.SQL_TO_TDML.value]:
        tdml_name = function_arg_map[arg_type][famc.SQL_TO_TDML.value][name]

        # Check for alternate names.
        if isinstance(tdml_name, dict) and famc.ALTERNATE_TO.value in tdml_name:
            alternate_to = function_arg_map[arg_type][famc.SQL_TO_TDML.value][name][
                famc.ALTERNATE_TO.value]
            tdml_name = function_arg_map[arg_type][famc.SQL_TO_TDML.value][alternate_to]

        if isinstance(tdml_name, list):
            tdml_name = tdml_name[0]

        return tdml_name

    # No teradataml name found for given teradataml input name
    return None


def __get_model_inputs_outputs(model, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get input and output information of the model to be saved.

    PARAMETERS:
        model:
            Required Argument.
            The model (analytic function object instance) to be saved.
            Types: teradataml Analytic Function object

        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        A tuple of two dictionaries, and a list:
        * The first containing input information.
        * The second containing output information.
        * The list containing names of tables to remove entries from GC for.

    EXAMPLE:
        >>> inputs, outputs, tables_to_not_gc = __get_model_inputs_outputs(model, function_arg_map)
    """
    input_json = {}
    output_json = {}
    remove_tables_entries_from_gc = []

    # First, let's identify the output DataFrames
    output_tables = [df._table_name for df in model._mlresults]

    for key in model.__dict__:
        if not key.startswith('_'):
            member = getattr(model, key)
            # The DataFrame is input if it is not output
            if isinstance(member, DataFrame):
                if member._table_name not in output_tables:
                    # Populate the input dictionary
                    # We construct a dictionary of the following form:
                    # { "<schema_name> :
                    #     { "<table_name>" :
                    #         { "nrows": <num_rows>,
                    #           "ncols": <num_cols>,
                    #           "input_name": <SQL name for the input>,
                    #           "client_specific_input_name": <tdml name for the input>
                    #         },
                    #         ...
                    #     }
                    # }
                    tdp = preparer(td_dialect)
                    nrows, ncols = member.shape
                    db_schema = UtilFuncs._extract_db_name(member._table_name)
                    # Add quotes around the DB name in case we are getting it using _get_current_databasename()
                    db_schema = tdp.quote(_get_current_databasename()) if db_schema is None else db_schema
                    db_table_name = UtilFuncs._extract_table_name(member._table_name)

                    if db_schema not in input_json:
                        input_json[db_schema] = {}
                    input_json[db_schema][db_table_name] = {}
                    input_json[db_schema][db_table_name]["nrows"] = nrows.item()
                    input_json[db_schema][db_table_name]["ncols"] = ncols
                    input_json[db_schema][db_table_name]["input_name"] = __get_arg_sql_name_from_tdml(function_arg_map,
                                                                                                      arg_type=famc.INPUTS.value,
                                                                                                      name=key)
                    input_json[db_schema][db_table_name]["client_specific_input_name"] = key
                else:
                    # Populate the output dictionary
                    # We construct a dictionary of the following form:
                    # { "<Output SQL Name> :
                    #     { "table_name": "<Database qualified name of the table>",
                    #       "client_specific_name": "<TDML specific name of the output>"
                    #     },
                    #     ...
                    # }

                    # teradataml Analytic functions models can be of two types:
                    #   1. Non-lazy OR
                    #   2. Lazy
                    # When model is non-lazy, that means model tables are already present/created on the system.
                    # When model is lazy, it may happen that model tables are yet to be evaluated/created.
                    # So first, let's make sure that model is evaluated, i.e., model tables are created,
                    # if they are not created already.
                    #
                    if member._table_name is None:
                        member._table_name = df_utils._execute_node_return_db_object_name(member._nodeid,
                                                                                          member._metaexpr)
                    output_table_name = member._table_name
                    if __is_view(output_table_name):
                        # If output table is not of type table, which means it's a view.
                        # So instead of using view name for persisting, we must materialize the same.
                        #
                        # To do so, let's just generate another temporary table name. One can notice, when
                        # we generate the temporary table name, we set the following flag 'gc_on_quit=True'.
                        # One can say, why to mark it for GC, when we are going to persist it.
                        # Only reason we added it for GC, so that, if in case anything goes wrong from the point
                        # we create the table to the end of the model saving, later this will be GC'ed as
                        # model saving had failed. Later we remove entry from GC, when model info is saved in
                        # MC tables and model is persisted in table.
                        #
                        output_table_name = UtilFuncs._generate_temp_table_name(prefix="td_saved_model_",
                                                                                use_default_database=True,
                                                                                gc_on_quit=True, quote=False,
                                                                                table_type=TeradataConstants.TERADATA_TABLE)

                        base_query = SQLBundle._build_base_query(member._table_name)
                        crt_table_query = SQLBundle._build_create_table_with_data(output_table_name, base_query)
                        UtilFuncs._execute_ddl_statement(crt_table_query)

                    # Append the name of the table to remove entry from GC.
                    remove_tables_entries_from_gc.append(output_table_name)

                    sql_name = __get_arg_sql_name_from_tdml(function_arg_map, arg_type=famc.OUTPUTS.value, name=key)
                    output_json[sql_name] = {}
                    output_json[sql_name]["table_name"] = output_table_name
                    output_json[sql_name]["client_specific_name"] = key

    return input_json, output_json, remove_tables_entries_from_gc


def __check_if_client_specific_use(key, function_arg_map, is_sql_name=False):
    """
    DESCRIPTION:
        Internal function to check if the argument corresponds to a client-only specific argument.

    PARAMETERS:
        key:
            Required Argument.
            The teradataml or SQL argument name to check for.
            Types: str

        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

        is_sql_name:
            Optional Argument.
            Specifies a boolean value indicating whether the key is a SQL or teradataml key.
            Types: bool
            Default Value: False

    RETURNS:
        A tuple containing:
        * A boolean value indicating whether the argument is or has:
            - a client-only specific argument: True
            - else False
        * A string specifying whether it is used in sequence_column ('used_in_sequence_by') or formula ('used_in_formula')

    EXAMPLES:
        >>> client_only, where_used = __check_if_client_specific_use(key, function_arg_map, is_sql_name=False)
    """
    # Let's assume SQL Name was passed
    sql_name = key

    if not is_sql_name:
        if key in function_arg_map[famc.ARGUMENTS.value][famc.TDML_TO_SQL.value]:
            sql_name = __get_arg_sql_name_from_tdml(function_arg_map, arg_type=famc.ARGUMENTS.value, name=key)
        else:
            # No SQL name found for given teradataml input name
            return False, None

    if isinstance(sql_name, dict):
        sql_name = sql_name[famc.TDML_NAME.value]

    if isinstance(sql_name, list):
        sql_name = sql_name[0]

    # Check if SQL name is an alternate name
    sql_block = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][sql_name]
    if famc.ALTERNATE_TO.value in sql_block:
        alternate_to = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][sql_name][famc.ALTERNATE_TO.value]
        sql_block = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][alternate_to]

    # Check and return boolean indicating if it is a formula or sequence_input_by argument
    if famc.USED_IN_SEQUENCE_INPUT_BY.value in sql_block:
        return True, famc.USED_IN_SEQUENCE_INPUT_BY.value
    elif famc.USED_IN_FORMULA.value in sql_block:
        return True, famc.USED_IN_FORMULA.value
    else:
        return False, None


def __get_model_parameters(model, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get parameter information of the model to be saved.

    PARAMETERS:
        model:
            Required argument.
            The model (analytic function object instance) to be saved.
            Types: teradataml Analytic Function object.

        function_arg_map:
            Required argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        A dict containing the information about parameters passed to model.

    EXAMPLES:
        >>> model_parameters = __get_model_parameters(model, function_arg_map)
    """
    parameter_json = {}

    # Get the attributes that are specific to the SQL syntax of the model algorithm
    sql_specific_attributes = model._get_sql_specific_attributes()

    # First, let's identify the parameters
    nonsql_argument_counter = 1
    for key in model.__dict__:
        if not key.startswith('_'):
            member = getattr(model, key)
            # Check if this is an attribute, not a DataFrame
            if not isinstance(member, DataFrame) and key != "sqlmr_query":
                # Check if it is a special or client specific argument
                special_use, used_in = __check_if_client_specific_use(key, function_arg_map)

                value = member
                # Add quotes to Boolean values as they tend to be handled in unintended way with JSON.
                if type(member) == bool or key == famc.TDML_FORMULA_NAME.value:
                    value = str(member)
                else:
                    if isinstance(member, list):
                        # We try to save the list as a string representation that could readily be used,
                        # in SQL, and has no language specific representation.
                        # Here, we remove the '[' and ']' from the string representation.
                        # We also avoid adding quotes around single-item list.
                        if len(member) == 1:
                            value = str(member[0]) if type(member[0]) == bool else member[0]
                        elif len(member) > 1:
                            if type(member[0]) == bool:
                                member = ['{}'.format(val) for val in member]
                            value = str(member).lstrip('[').rstrip(']')
                        else:
                            # Empty list has no meaning, but no chance of running into this with the validation
                            # in the function wrappers.
                            value = None
                if value is not None:
                    if special_use:
                        sql_name = '__nonsql_argument_{}__'.format(nonsql_argument_counter)
                        nonsql_argument_counter = nonsql_argument_counter + 1
                    else:
                        sql_name = __get_arg_sql_name_from_tdml(function_arg_map,arg_type=famc.ARGUMENTS.value,name=key)
                    parameter_json[sql_name] = {}
                    parameter_json[sql_name]["value"] = value
                    parameter_json[sql_name]["client_specific_name"] = key

    sql_name = '__nonsql_argument_{}__'.format(nonsql_argument_counter)
    parameter_json[sql_name] = {}
    parameter_json[sql_name]["value"] = model.__class__.__name__
    parameter_json[sql_name]["client_specific_name"] = "__class_name__"

    # Add the SQL specific arguments
    for sql_name in sql_specific_attributes:
        parameter_json[sql_name] = {}
        parameter_json[sql_name]["value"] = sql_specific_attributes[sql_name]
        # Also save the formula related property names for corresponding SQL arguments
        if hasattr(model, '_sql_formula_attribute_mapper'):
            if sql_name in model._sql_formula_attribute_mapper:
                parameter_json[sql_name]["client_specific_name"] = model._sql_formula_attribute_mapper[sql_name]

    return parameter_json


def __check_if_model_exists(name, created=False, accessible=False,
                            raise_error_if_exists=False, raise_error_if_model_not_found=False):
    """
    DESCRIPTION:
        Internal function to check if model with model_name, exists or not.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to check whether it exists or not.
            Types: str

        created:
            Optional Argument.
            Specifies whether to check if the model exists and is created by the user.
            Default Value: False (Check for all models)
            Types: bool

        accessible:
            Optional Argument.
            Specifies whether to check if the model exists and is accessible by the user.
            Default Value: False (Check for all models)
            Types: bool

        raise_error_if_exists:
            Optional Argument.
            Specifies the flag to decide whether to raise error when model exists or not.
            Default Value: False (Do not raise exception)
            Types: bool

        raise_error_if_model_not_found:
            Optional Argument.
            Specifies the flag to decide whether to raise error when model is found or not.
            Default Value: False (Do not raise exception)
            Types: bool

    RETURNS:
        None.

    RAISES:
        TeradataMlException - MODEL_ALREADY_EXISTS, MODEL_NOT_FOUND

    EXAMPLES:
        >>> meta_df = __check_if_model_exists("glm_out")
    """
    # Get the DataFrame for the Models metadata table.
    if created:
        current_user = __get_current_user()
        models_meta_df = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS.value))
        models_meta_df = models_meta_df[models_meta_df[mac.CREATED_BY.value].str.lower() == current_user.lower()]
    elif accessible:
        models_meta_df = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELSX.value))
    else:
        models_meta_df = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS.value))

    # Get the model created by current client user, using teradataml, with name as model_name.
    model_name = models_meta_df.Name

    # Filter Expression.
    if name is not None:
        models_meta_df = models_meta_df[model_name == name]

    num_rows = models_meta_df.shape[0]

    if raise_error_if_exists:
        if num_rows == 1 and name is not None:
            # If model with name 'name' already exists.
            raise TeradataMlException(Messages.get_message(MessageCodes.MODEL_ALREADY_EXISTS,
                                                           name),
                                      MessageCodes.MODEL_ALREADY_EXISTS)

    if raise_error_if_model_not_found:
        if num_rows == 0:
            if not created:
                # 'name' MODEL_NOT_FOUND
                raise TeradataMlException(Messages.get_message(MessageCodes.MODEL_NOT_FOUND,
                                                               name, ''),
                                          MessageCodes.MODEL_NOT_FOUND)
            else:
                # 'name' MODEL_NOT_FOUND or not created by user.
                raise TeradataMlException(Messages.get_message(MessageCodes.MODEL_NOT_FOUND,
                                                               name, ' or not created by user'),
                                          MessageCodes.MODEL_NOT_FOUND)


def __check_if_model_cataloging_tables_exists(raise_error_if_does_not_exists=True):
    """
    DESCRIPTION:
        Check whether Model Cataloging tables (one of the views - ModelCataloging.ModelsV) exists or not.

    PARAMETERS:
        raise_error_if_does_not_exists:
            Optional Argument.
            Specifies the flag to decide whether to raise error when Model Cataloging tables does not exist.
            Default Value: True (Raise exception)
            Types: bool

    RAISES:
        None.

    RETURNS:
        True, if the view exists, else False.

    EXAMPLES:
        >>>  __check_if_model_cataloging_tables_exists()
    """
    # Get current context()
    conn = get_context()

    # Check whether tables exists on the system or not.
    model_table_exists = conn.dialect.has_view(conn, view_name=mac.MODELS.value,
                                                schema=mac.MODEL_CATALOG_DB.value)

    # If both tables exist, return True.
    if model_table_exists:
        return True

    # We are here means the Model Cataloging view does not exist.
    # Let's raise error if 'raise_error_if_does_not_exists' set to True.
    if raise_error_if_does_not_exists:
        # Raise error, as one or both Model Cataloging tables does not exist.
        # MODEL_CATALOGING_TABLE_DOES_EXIST
        raise TeradataMlException(
            Messages.get_message(MessageCodes.MODEL_CATALOGING_TABLE_DOES_EXIST),
            MessageCodes.MODEL_CATALOGING_TABLE_DOES_EXIST)


def __get_tables_for_model(name, current_user):
    """
    DESCRIPTION:
        Function to get model tables for a given model name.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to get the model tables for.
            Types: str

        current_user:
            Required Argument.
            Specifies the name of the current Vantage user.
            Types: str

    RETURNS:
        A list of model tables associated with the model.

    EXAMPLES:
        >>> table_list = __get_tables_for_model(name, current_user)
    """
    # Get list of tables
    model_object_info = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_OBJECTS.value))
    model_info = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELSX.value))
    model_info = model_info[model_info[mac.CREATED_BY.value].str.lower() == current_user.lower()]
    model_info = model_info[model_info[mac.MODEL_NAME.value] == name]
    model_objects_to_publish = model_info.join(model_object_info,
                                               on=[model_info.Name == model_object_info.ModelName],
                                               how='inner').select([mac.MODEL_OBJ_TABLE_NAME.value])

    model_objects_to_publish = model_objects_to_publish.to_pandas().squeeze()
    if isinstance(model_objects_to_publish, str):
        # If there is only one output table
        return [model_objects_to_publish]
    else:
        # For multiple or no output tables
        return model_objects_to_publish.tolist()


def __get_current_user(conn=None):
    """
    DESCRIPTION:
        Internal function to return the current Vantage user

    PARAMETERS:
        conn:
            Optional Argument,
            The underlying SQLAlchemy engine for the connection.
            Types: SQLAlchemy engine

    RETURNS:
        A string representing the name of the current database user.

    EXAMPLE:
        >>> current_user = __get_current_user()
    """
    if conn is None:
        conn = get_context()

    return conn.execute('select user').scalar()


def __get_like_filter_expression_on_col(metaexpr, column_name, like):
    """
    DESCRIPTION:
        Internal function to get the filter expression on column_name containing string matching with like.
        (Case insensitive matching)

    PARAMETERS:
        metaexpr:
            Required Argument.
            Specifies the teradataml DataFrame meta data.
            Types: _MetaExpression

        column_name:
            Required Argument.
            Specifies the column name which is to be used in filter expression.
            Types: str

        like:
            Required Argument.
            Specifies the pattern to be matched in filter expression.
            Types: str

    RETURNS:
        _SQLColumnExpression object

    RAISES:
        None

    EXAMPLES:
        >>> filter_expression = __get_like_filter_expression_on_col(models_meta_df._metaexpr,
        ...                                                         mmc.MMT_COL_model_class.value,
        ...                                                         function_name)
    """
    return metaexpr._filter(0, 'like', [column_name], like = like, match_arg='i')


def __get_model_engine(model):
    """
    DESCRIPTION:
        Internal function to return the engine name on which the model was generated.

    PARAMETERS:
        model:
            Required Argument.
            Model object, for which engine is to be found.
            Types: str

    RETURNS:
        Engine name ('ML Engine' or 'Advanced SQL Engine')

    RAISES:
        TeradataMlException

    EXAMPLES:
        >>> __get_model_engine(model)
    """
    if ".mle." in str(type(model)):
        return mac.MODEL_ENGINE_ML.value
    elif ".sqle." in str(type(model)):
        return mac.MODEL_ENGINE_ADVSQL.value
    else:
        raise TeradataMlException(Messages.get_message(MessageCodes.UNKNOWN_MODEL_ENGINE,
                                                       str(type(model))),
                                  MessageCodes.UNKNOWN_MODEL_ENGINE)


def __get_wrapper_class(model_engine, model_class):
    """
    DESCRIPTION:
        Internal function to the wrapper class that can be executed to create the instance of the
        model_class from engine specified in model_engine.

    PARAMETERS:
        model_engine:
            Required Argument.
            Model engine string 'ML Engine' or 'Advanced SQL Engine'.
            Types: str

        model_class:
            Required Argument.
            Model class string for the analytical function wrapper.
            Types: str

    RETURNS:
        A wrapper CLASS

    RAISES:
        ValueError - When invalid engine is passed.
        AttributeError - When model_class wrapper function, does is not from model_engine.

    EXAMPLES:
        >>> __get_wrapper_class("ML Engine", "GLM")
    """
    if model_engine == mac.MODEL_ENGINE_ML.value:
        module_name = "teradataml.analytics.mle"
    elif model_engine == mac.MODEL_ENGINE_ADVSQL.value:
        module_name = "teradataml.analytics.sqle"
    else:
        raise ValueError("Invalid Engine found in Model Cataloging table.")

    wrapper_module = importlib.import_module(module_name)

    return getattr(wrapper_module, model_class)


def __is_view(tablename):
    """
    DESCRIPTION:
        Internal function to check whether the object is view or not.

    PARAMETERS:
        tablename:
            Required Argument.
            Table name or view name to be checked.
            Types: str

    RAISES:
        None.

    RETURNS:
        True when the tablename is view, else false.

    EXAMPLES:
        >>> __is_view('"dbaname"."tablename"')
    """
    db_name = UtilFuncs._teradata_unquote_arg(UtilFuncs._extract_db_name(tablename), "\"")
    table_view_name = UtilFuncs._teradata_unquote_arg(UtilFuncs._extract_table_name(tablename), "\"")
    query = SQLBundle._build_select_table_kind(db_name, "{0}".format(table_view_name), "'V'")

    pdf = pd.read_sql(query, get_context())
    if pdf.shape[0] > 0:
        return True
    else:
        return False


def __delete_model_tableview(tableviewname):
    """
    DESCRIPTION:
        Internal function to remove table name or view.

    PARAMETERS:
        tableviewname:
            Required Argument.
            Table name or view name to be deleted.
            Types: str

    RAISES:
        None.

    RETURNS:
        bool

    EXAMPLES:
        >>> __delete_model_tableview('"dbname"."tableviewname"')
    """
    if not __is_view(tableviewname):
        try:
            UtilFuncs._drop_table(tableviewname)
        except:
            return False
    else:
        try:
            UtilFuncs._drop_view(tableviewname)
        except:
            return False

    return True


def __get_all_formula_related_args(function_arg_map):
    """
    DESCRIPTION:
        Internal function to find a list of all formula related arguments for a function.

    PARAMETERS:
        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
         A dictionary mapping all SQL Arguments for the function related to formula to its role in formula.

    EXAMPLE:
        >>> __get_all_formula_related_args(function_arg_map)
    """
    formula_args = {}
    for arg_name in function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value]:
        arg = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][arg_name]
        # Ignore alternate names
        if famc.ALTERNATE_TO.value in arg:
            alternate_name = arg[famc.ALTERNATE_TO.value]
            arg = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][alternate_name]

        if famc.USED_IN_FORMULA.value in arg:
            formula_args[arg_name] = {}
            formula_args[arg_name][famc.USED_IN_FORMULA.value] = arg[famc.USED_IN_FORMULA.value]
            formula_args[arg_name]['arg_value'] = None

    return formula_args


def __fix_imbalanced_quotes(arg):
    """
    DESCRIPTION:
        Internal function to fix imbalanced quotes around a string.

    PARAMETERS:
        arg:
            Required Argument.
            The string to fix the imbalanced quotes for, if any.
            Types: str

    RETURNS:
         The input string with any imbalanced quotes stripped.

    EXAMPLE:
        >>> __fix_imbalanced_quotes('hello"')
        hello
    """
    for quote in ["'", '"']:
        if (arg.startswith(quote) and not arg.endswith(quote)) or (not arg.startswith(quote) and arg.endswith(quote)):
            return arg.strip(quote)

    return arg


def __get_tdml_parameter_value_for_sequence(function_arg_map, attr_value):
    """
    DESCRIPTION:
        Internal function to form sequence_column teradataml argument from SQL arguments.

    PARAMETERS:
        function_arg_map:
            Required Argument.
            The teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

        attr_value:
            Required Argument.
            The value of the SQL sequence argument.

    RETURNS:
         A dictionary mapping the teradataml sequence argument to its values.

    EXAMPLES:
        >>> tdml_sequence_args = __get_tdml_parameter_value_for_sequence(function_arg_map, sql_sequence_arg)
    """
    sequence_dict = {}
    tdml_name = None
    for column in attr_value.split(','):
        if len(column) == 0:
            continue
        if ':' in column:
            input_name, col_val = column.split(':')
            input_name = __fix_imbalanced_quotes(input_name)
            col_val = __fix_imbalanced_quotes(col_val)
            tdml_name = '{}_{}'.format(__get_arg_tdml_name_from_sql(function_arg_map, famc.INPUTS.value,
                                                                    input_name.lower()),
                                       'sequence_column')
            tdml_name = __fix_imbalanced_quotes(tdml_name)
            sequence_dict[tdml_name] = [col_val]
        else:
            if tdml_name not in sequence_dict:
                # This means there is only one input and the input name was not specified in the
                # SequenceInputBy clause. So we get the only input name.
                tdml_name = list(function_arg_map[famc.INPUTS.value][famc.TDML_TO_SQL.value].keys())[0]
                tdml_name = '{}_{}'.format(tdml_name, 'sequence_column')
                sequence_dict[tdml_name] = []
            column = __fix_imbalanced_quotes(column)
            sequence_dict[tdml_name].append(column)

    return sequence_dict


def __get_target_column(name):
    """
    DESCRIPTION:
        Internal function to get the target column of a saved model.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name used to save the model.
            Types: str

    RETURNS:
         A String representing the name of the target column.

    EXAMPLES:
        >>> target_column = __get_target_column('GLMModel')
    """
    model_details = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_DETAILSX.value))
    model_details = model_details[model_details[mac.MODEL_DERIVED_NAME.value] == name]
    target_column = model_details.select([mac.MODEL_DERIVED_TARGET_COLUMN.value]).squeeze()
    return target_column


def __get_tdml_parameter_value_for_formula(formula_args, target_column):
    """
    DESCRIPTION:
        Internal function to build the formula argument based on the SQL equivalent inputs.

    PARAMETERS:
        formula_args:
            Required Argument.
            A dictionary mapping all SQL Arguments for the function related to formula to its role in formula.
            Types: dict

        target_column:
            Required Argument.
            The target column for the model, if any.
            Types: str

    RETURNS:
         A String representing the formula argument to be used with teradataml.

    EXAMPLES:
        >>> formula = __get_tdml_parameter_value_for_formula(formula_args, target_column)
    """
    dependent_var = target_column
    all_vars = []

    for arg in formula_args:
        if formula_args[arg]['arg_value'] is not None:
            if formula_args[arg][famc.USED_IN_FORMULA.value] == famc.DEPENDENT_ATTR.value:
                dependent_var = formula_args[arg]['arg_value'].strip("'")
            else:
                all_vars.extend(formula_args[arg]['arg_value'].split(','))

    # Remove duplicates
    all_vars = list(set(all_vars))
    all_vars = [var.strip("'") for var in all_vars]

    # Remove dependent variable if it occurs in all_vars
    if dependent_var in all_vars:
        all_vars.pop(all_vars.index(dependent_var))

    formula = '{} ~ {}'.format(dependent_var, ' + '. join(all_vars))
    return formula


def __cast_arg_values_to_tdml_types(value, type_):
    """
    DESCRIPTION:
        Internal function used by retrieve_model() to cast the retrieved model parameters to the expected python types.

    PARAMETERS:
        value:
            Required Argument.
            Specifies the value retrieved that needs a type cast.
            Types: str

        type_:
            Required Argument.
            Specifies the Python type the value needs to be cast to.
            Type: Python type or tuple of Python types

    RETURNS:
        The value cast to the required Python type.

    RAISES:
        None

    EXAMPLE:
        >>> cast_value = __cast_arg_values_to_tdml_types('0.1', float)
    """
    return_value = None
    required_type = type_

    accepted_bool_values = ['1', 't', 'true', 'y', 'yes']

    # If the required_type is a tuple, we need to consider the possibility of the value being a list
    if isinstance(required_type, tuple):
        # The function_argument_mapper adds the type of the object in the list as the first value in the tuple
        required_type = required_type[0]

        # Use regex to split the string value into a list.
        # This is required only when we expect the values to be a list as well, in which case,
        # the 'value' will be a comma-separated list of strings.
        # The pattern matches anything but whitespace and comma and not in quotes, or anything in quotes,
        # basically avoiding splitting on a comma when surrounded by quotes.
        pattern = r"[^',\s]+|'[^']*'"
        values = re.findall(pattern, value)
        if len(values) > 1:
            if required_type == bool:
                # Remove the quotes surrounding items in a list,
                # and check for their presence in the acceptable TRUE values.
                return_value = [val.strip().strip("'").lower() in accepted_bool_values for val in values]
            else:
                # Remove the quotes surrounding items in a list cast them to the required type.
                return_value = [required_type(val.strip().strip("'")) for val in values]
        else:
            value = values[0]

    if return_value is None:
        if required_type == bool:
            # Remove the quotes surrounding the value,
            # and check for their presence in the acceptable TRUE values.
            return_value = value.strip().strip("'").lower() in accepted_bool_values
        else:
            # Remove the quotes surrounding the value and cast it to the required type.
            return_value = required_type(value.strip().strip("'"))

    return return_value


def __get_model_access(name):
    """
    DESCRIPTION:
        Internal function to get the current access level of a saved model.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the saved model to get the access level for.
            Types: str

    RAISES:
        None.

    RETURNS:
        A String representing the access level of the saved model.

    EXAMPLES:
        >>> __get_model_access('saved_glm_model')
    """
    df = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_DETAILS.value))
    return df[df[mac.MODEL_DERIVED_NAME.value] == name].select([mac.MODEL_ACCESS.value]).squeeze()


def __get_tdml_type_for_tdml_arg(name, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get the Python type for the given teradataml model class attribute.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the teradataml name for the attribute to get the expected python type for.
            Types: str

        function_arg_map:
            Required Argument.
            Specifies the teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        Python type for the given teradataml model class attribute name.
        None when argument name not found.

    RAISES:
        None

    EXAMPLES:
        >>> from teradataml.catalog.function_argument_mapper import _argument_mapper
        >>> function_arg_map = _argument_mapper._get_function_map('ML Engine', 'glm')
        >>> tdml_type = __get_tdml_type_for_tdml_arg('linkfunction', function_arg_map)
    """
    # Let's check if the function argument mapper has the information about the argument we are looking for.
    # If not, let's return None.
    if name not in function_arg_map[famc.ARGUMENTS.value][famc.TDML_TO_SQL.value]:
        return None

    tdml_type = str
    sql_name = function_arg_map[famc.ARGUMENTS.value][famc.TDML_TO_SQL.value][name]

    # We can ignore formula letting it default to str
    special_use, used_in = __check_if_client_specific_use(name, function_arg_map)
    if not special_use or used_in == famc.USED_IN_SEQUENCE_INPUT_BY.value:
        tdml_type = function_arg_map[famc.ARGUMENTS.value][famc.SQL_TO_TDML.value][sql_name][famc.TDML_TYPE.value]

    return tdml_type


def __retrieve_model_class(name, model_client, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get the teradataml class used for generating model given it's name.

    PARAMETERS:
        name:
            Optional Argument. Required when model was saved by teradataml.
            Specifies the name of the model to retrieve the model attributes and output information for.
            Types: str

        model_client:
            Required Argument.
            Specified the name of the client used to generate the model.
            Types: str

        function_arg_map:
            Optional Argument. Required when model was not saved by teradataml.
            Specifies the teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        A String representing the teradataml class name corresponding to the model.

    EXAMPLES:
        >>> model_class = __retrieve_model_class(name, model_client, function_arg_map)
    """
    if model_client == mac.MODEL_TDML.value:
        # Create DF on top of ModelAttributesV view
        model_arguments = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_ATTRS.value))
        model_arguments = model_arguments[model_arguments[mac.MODEL_DERIVED_NAME.value] == name]
        model_class = model_arguments[model_arguments.ClientSpecificAttributeName.str.
                                          contains(mac.MODEL_CLIENT_CLASS_KEY.value) == 1].\
            select([mac.MODEL_ATTR_VALUE.value]).squeeze()
    else:
        model_class = function_arg_map[famc.FUNCTION_TDML_NAME.value]

    return model_class


def __retrieve_model_client_engine_algorithm(name, return_details=False):
    """
    DESCRIPTION:
        Internal function to get the the model generating engine, client, algorithm, and optionally the model details
        given the model name.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to retrieve the model attributes and output information for.
            Types: str

        return_details:
            Optional Argument.
            Specifies whether to also return the row from the ModelDetailsV corresponding to the model.
            Types: bool
            Default Value: False

    RETURNS:
        A tuple containing:
        * the name of the client that was used to generate the model,
        * the name of the engine that generated the model, and
        * the name of the algorithm used to generate the model.
        * If return_details=True, then additionally, the ModelDetailsV row related to the model.

    EXAMPLES:
        >>> model_client, model_engine, algorithm = __retrieve_model_client_engine_algorithm(name)
    """

    model_details = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_DETAILS.value))
    model_details = model_details[model_details[mac.MODEL_DERIVED_NAME.value] == name]
    model_algorithm = model_details.select([mac.MODEL_DERIVED_ALGORITHM.value]).squeeze().lower()

    model_client_and_eng = model_details.select([mac.MODEL_DERIVED_GENCLIENT.value,
                                                 mac.MODEL_DERIVED_GENENG.value]).squeeze()

    model_client = model_client_and_eng.select([mac.MODEL_DERIVED_GENCLIENT.value]).squeeze()
    model_engine = model_client_and_eng.select([mac.MODEL_DERIVED_GENENG.value]).squeeze()

    if return_details:
        return model_client, model_engine, model_algorithm, model_details
    else:
        return model_client, model_engine, model_algorithm


def __retrieve_model_attributes(name, model_client, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get the the attributes used for generating model given it's name.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to retrieve the model attributes and output information for.
            Types: str

        model_client:
            Required Argument.
            Specified the name of the engine that generated the model.
            Types: str

        function_arg_map:
            Required Argument.
            Specifies the teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        A tuple of dictionaries:
        * the first one containing the attribute names and their values, and
        * the second one containing the formula related properties and their values, if the model saving client was
          teradataml.

    EXAMPLES:
        >>> model_parameters, formula_related_params = __retrieve_model_attributes(name, model_client, function_arg_map)
    """
    # Create DF on top of ModelAttributesV view and
    # 1. get only rows related to the model named 'name'.
    model_arguments = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_ATTRS.value))
    model_arguments = model_arguments[model_arguments[mac.MODEL_DERIVED_NAME.value] == name]

    if model_client == mac.MODEL_TDML.value:
        attr_name_to_use = mac.MODEL_ATTR_CLIENT_NAME.value
    else:
        attr_name_to_use = mac.MODEL_ATTR_NAME.value

    if model_client != mac.MODEL_TDML.value:
        # 2. Filter out the the row where "AttributeName" is not like __nonsql_argument_
        model_arguments = model_arguments.assign(notSqlonly=model_arguments.AttributeName.str.contains('__nonsql_argument_'))
        model_arguments = model_arguments[model_arguments.notSqlonly == 0]
    else:
        # 2. Filter out the the row where "ClientSpecificAttributeName" is not NULL
        model_arguments = model_arguments[model_arguments[attr_name_to_use] != None]

    # Make sure the non-lazy view exists before SQLAlchemy construct can be used
    if model_arguments._table_name is None:
        model_arguments._table_name = df_utils._execute_node_return_db_object_name(model_arguments._nodeid,
                                                                                   model_arguments._metaexpr)

    # Since lengthier arguments can be a clob column, casting the smaller to clob
    # to select one of the two as applicable without values being truncated.
    select_expression = [model_arguments[attr_name_to_use].expression.label("AttrName"),
                         case_when([(model_arguments[mac.MODEL_ATTR_VALUE.value].expression == None,
                                     model_arguments[mac.MODEL_ATTR_VALUEC.value].expression)],
                                   else_=func.cast(model_arguments[mac.MODEL_ATTR_VALUE.value].expression,
                                                   type_=CLOB)).expression.label("AttrValue")]

    # Get the final list of AttNames (Client/SQL) and their values  (CLOB type)
    final_list = DataFrame.from_query(str(select(select_expression).compile(compile_kwargs={"literal_binds": True})))

    # Model Parameters
    final_list = final_list[final_list["AttrName"] != mac.MODEL_CLIENT_CLASS_KEY.value]
    params = final_list.to_pandas().to_dict()
    model_parameters = {}
    formula_related_params = {}

    index_len = len(params["AttrName"])
    if model_client == mac.MODEL_TDML.value:
        for i in range(index_len):
            # Check if the arguments are related to formula
            if params["AttrName"][i] == '__all_columns':
                formula_related_params['__all_columns'] = __cast_arg_values_to_tdml_types(params["AttrValue"][i],
                                                                                          (str, list))
            elif params["AttrName"][i] == '__numeric_columns':
                formula_related_params['__numeric_columns'] = __cast_arg_values_to_tdml_types(params["AttrValue"][i],
                                                                                              (str, list))
            elif params["AttrName"][i] == '__categorical_columns':
                formula_related_params['__categorical_columns'] = __cast_arg_values_to_tdml_types(params["AttrValue"]
                                                                                                  [i], (str, list))
            elif params["AttrName"][i] == '__response_column':
                formula_related_params['__response_column'] = __cast_arg_values_to_tdml_types(params["AttrValue"][i],
                                                                                              str)
            else:
                tdml_type = __get_tdml_type_for_tdml_arg(params["AttrName"][i], function_arg_map)
                # tdml_type can be None when we do not have information about the argument in
                # the function argument mapper. Let's ignore it in the retrieval.
                if tdml_type is not None:
                    model_parameters[params["AttrName"][i]] = __cast_arg_values_to_tdml_types(params["AttrValue"][i],
                                                                                              tdml_type)
    else:
        formula_args = None
        for i in range(index_len):
            model_param_name = __get_arg_tdml_name_from_sql(function_arg_map,
                                                            arg_type=famc.ARGUMENTS.value,
                                                            name=params["AttrName"][i].lower())

            attr_value = params["AttrValue"][i]

            special_use, used_in = __check_if_client_specific_use(params["AttrName"][i].lower(),
                                                                  function_arg_map, is_sql_name=True)
            if special_use:
                if used_in == famc.USED_IN_FORMULA.value:
                    # Get formula
                    if formula_args is None:
                        formula_args = __get_all_formula_related_args(function_arg_map)
                    formula_args[params["AttrName"][i].lower()]['arg_value'] = attr_value
                else:
                    # Get dictionary of sequence_column arguments
                    sequence_by = __get_tdml_parameter_value_for_sequence(function_arg_map, attr_value)
                    if sequence_by:
                        for seq_key in sequence_by:
                            model_parameters[seq_key] = sequence_by[seq_key]
            else:
                # tdml_name can be None when we do not have information about the SQL argument in
                # the function argument mapper. Let's ignore it in the retrieval.
                if model_param_name is None:
                    warnings.warn(Messages.get_message(MessageCodes.CANNOT_TRANSLATE_TO_TDML_NAME,
                                                       params["AttrName"][i]))
                    continue
                model_param_type = model_param_name[famc.TDML_TYPE.value]
                model_param_name = model_param_name[famc.TDML_NAME.value]
                model_parameters[model_param_name] = __cast_arg_values_to_tdml_types(attr_value,
                                                                                     model_param_type)

        if formula_args is not None:
            formula = __get_tdml_parameter_value_for_formula(formula_args, __get_target_column(name))
            model_parameters[famc.TDML_FORMULA_NAME.value] = formula

    return model_parameters, formula_related_params


def __retrieve_model_outputs(name, model_client, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get the output DataFrames corresponding to a saved model given it's name.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to retrieve the model output information for.
            Types: str

        model_client:
            Required Argument.
            Specifies the name of the client that generated the model.
            Types: str

        function_arg_map:
            Required Argument.
            Specifies the teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RAISES:
        TeradataMlException

    RETURNS:
        A Pandas DataFrame with the teradataml specific name for the output, and the underlying
        table names corresponding to them.

    EXAMPLES:
        >>> output_df = __retrieve_model_outputs(name, model_client, function_arg_map)
    """
    # Let's also get the output table map
    model_outputs = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_OBJECTS.value))
    model_outputs = model_outputs[model_outputs[mac.MODEL_DERIVED_NAME.value] == name]
    if model_client == mac.MODEL_TDML.value:
        model_outputs = model_outputs.assign(drop_columns=True,
                                             OutputName=model_outputs[mac.MODEL_OBJ_CLIENT_NAME.value],
                                             OutputTableName=model_outputs[mac.MODEL_OBJ_TABLE_NAME.value]).to_pandas()
    else:
        model_outputs = model_outputs.assign(drop_columns=True,
                                             OutputName=model_outputs[mac.MODEL_OBJ_NAME.value],
                                             OutputTableName=model_outputs[mac.MODEL_OBJ_TABLE_NAME.value]).to_pandas()
        output_names = []
        output_table_names = []
        index_len = len(model_outputs["OutputName"])
        for i in range(index_len):
            output_name = __get_arg_tdml_name_from_sql(function_arg_map, famc.OUTPUTS.value,
                                                       model_outputs["OutputName"][i].lower())
            # We raise an exception when we are not able to get the teradataml name
            # for the SQL name of the output table.
            if output_name is None:
                raise TeradataMlException(Messages.get_message(MessageCodes.CANNOT_TRANSLATE_TO_TDML_NAME),
                                          MessageCodes.CANNOT_TRANSLATE_TO_TDML_NAME)
            output_names.append(output_name)
            output_table_names.append(model_outputs["OutputTableName"][i])
        model_outputs = pd.DataFrame({'OutputName': output_names, 'OutputTableName': output_table_names})

    return model_outputs


def __retrieve_model_inputs(name, model_client, function_arg_map):
    """
    DESCRIPTION:
        Internal function to get the input DataFrames corresponding to a saved model given it's name.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to retrieve the model input information for.
            Types: str

        model_client:
            Required Argument.
            Specifies the name of the client that generated the model.
            Types: str

        function_arg_map:
            Required Argument.
            Specifies the teradataml-sql map for the function obtained using function_argument_mapper.
            Types: dict

    RETURNS:
        A dict mapping the teradataml specific name for the input to actual input DataFrame.
        The dictionary is of the following form:
            {
                <tdml_input_name> :
                    {
                        'TableName' : <actual_table_name>,
                        'NRows': <number of rows>,
                        'NCols': <number of columns>
                    }
            }

    EXAMPLES:
        >>> input_info = __retrieve_model_inputs(name, model_client, function_arg_map)
    """
    model_inputs = {}

    # First get the model_id
    model_id = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS.value))
    model_id = model_id[model_id[mac.MODEL_NAME.value] == name].select([mac.MODEL_ID.value]).squeeze().item()

    # Now find the inputs related to the model
    model_training_data = DataFrame(in_schema(mac.MODEL_CATALOG_DB.value, mac.MODELS_INPUTSX.value))
    model_training_data = model_training_data[model_training_data[mac.MODEL_ID.value] == model_id]
    model_training_data = model_training_data.to_pandas().to_dict()

    index_len = len(model_training_data[mac.MODEL_ID.value])
    for i in range(index_len):
        if model_client == mac.MODEL_TDML.value:
            input_name = model_training_data[mac.MODEL_INPUT_CLIENT_NAME.value][i]
            table_name = model_training_data[mac.MODEL_INPUT_TABLE_NAME.value][i]
        else:
            input_name = __get_arg_tdml_name_from_sql(function_arg_map, famc.INPUTS.value,
                                                      model_training_data[mac.MODEL_INPUT_NAME.value][i].lower())
            # if input_name is None then we have been unable to get the tdml name from the SQL name
            # for the input. In this case, we ignore the input initialization and continue.
            if input_name is None:
                warnings.warn(Messages.get_message(MessageCodes.CANNOT_TRANSLATE_TO_TDML_NAME,
                                                   model_training_data[mac.MODEL_INPUT_NAME.value][i]))
                continue
            table_name = model_training_data[mac.MODEL_INPUT_TABLE_NAME.value][i]

        # No need for further processing if the TableName associated with an input is None.
        if table_name is None:
            continue

        nrows = model_training_data[mac.MODEL_INPUT_NROWS.value][i]
        ncols = model_training_data[mac.MODEL_INPUT_NCOLS.value][i]

        model_inputs[input_name] = {}
        model_inputs[input_name][mac.MODEL_OBJ_TABLE_NAME.value] = table_name
        model_inputs[input_name][mac.MODEL_INPUT_NROWS.value] = nrows
        model_inputs[input_name][mac.MODEL_INPUT_NCOLS.value] = ncols

    return model_inputs


def __retrieve_argument_and_output_map(name):
    """
    DESCRIPTION:
        Internal function to get the teradataml function class corresponding to the model to retrieve,
        along with the attributes and output objects to initialize the model with.

    PARAMETERS:
        name:
            Required Argument.
            Specifies the name of the model to retrieve the model attributes and output information for.
            Types: str

    RETURNS:
        A tuple with the following elements:
        * the function class to initialize for the model,
        * the model generating engine to help with the initialization, and
        * the dictionary containing the attributes and their values including output table objects.

    EXAMPLES:
        >>> model_class, model_engine, attribute_dictionary = __retrieve_argument_and_output_map(name)
    """
    # First, let's get the model engine, client, algorithm, and other details.
    model_client, model_engine, model_algorithm, model_details = __retrieve_model_client_engine_algorithm(name, True)

    # Get the build_time, algorithm_name/model_class, target_column, prediction_type to be returned later as parameters.
    # model_algorithm is also use to figure out the Python class to be instantiated.
    build_time = model_details.select([mac.MODEL_DERIVED_BUILD_TIME.value]).squeeze()
    prediction_type = model_details.select([mac.MODEL_DERIVED_PREDICTION_TYPE.value]).squeeze()
    target_column = model_details.select([mac.MODEL_DERIVED_TARGET_COLUMN.value]).squeeze()

    # Get the teradataml model class corresponding to the model
    function_arg_map = _argument_mapper._get_function_map(engine=model_engine,
                                                          function_name=model_algorithm.lower())
    model_class = __retrieve_model_class(name, model_client, function_arg_map)

    # Get the model attributes and formula related arguments
    model_parameters, formula_related_args = __retrieve_model_attributes(name, model_client, function_arg_map)
    # Also append the algorithm_name, build_time, target_column, and prediction_type for the function
    model_parameters['__algorithm_name'] = model_algorithm
    if build_time is not None:
        model_parameters['__build_time'] = build_time.item()
    if target_column is not None:
        model_parameters['__target_column'] = target_column
    if prediction_type is not None:
        model_parameters['__prediction_type'] = prediction_type

    # Merge the formula related arguments
    model_parameters = {**model_parameters, **formula_related_args}

    # Try plugging in the input DataFrames as well
    model_inputs = __retrieve_model_inputs(name, model_client, function_arg_map)
    for input_name in model_inputs:
        table_name = model_inputs[input_name][mac.MODEL_OBJ_TABLE_NAME.value]
        sname = UtilFuncs._extract_db_name(table_name)
        tname = UtilFuncs._extract_table_name(table_name)

        # Add quoted around the DB and Table names if necessary.
        tdp = preparer(td_dialect)
        if sname is not None:
            sname = tdp.quote(UtilFuncs._teradata_unquote_arg(sname, quote='"'))
        if tname is not None:
            tname = tdp.quote(UtilFuncs._teradata_unquote_arg(tname, quote='"'))

        # Try creating the input DataFrames
        try:
            if sname is None:
                input = DataFrame(tname)
            else:
                input = DataFrame(in_schema(sname, tname))

            model_inputs[input_name] = input
        except Exception as err:
            # We are most likely not able to create a DataFrame on the input as the input may no longer be existent.
            # In this case, we just initialize it to None.
            warnings.warn("Unable to fetch input details for the '{}' argument "
                          "from underlying object named '{}'".format(input_name, table_name))
            model_inputs[input_name] = None

    # Let's also get the output table map
    model_outputs = __retrieve_model_outputs(name, model_client, function_arg_map)
    tables = model_outputs.to_dict()
    model_tables = {}
    index_len = len(tables["OutputName"])
    for i in range(index_len):
        output_name = tables["OutputName"][i]
        model_tables[output_name] = tables["OutputTableName"][i]

    return model_class, model_engine, {**model_inputs, **model_parameters, **model_tables}


from teradataml.dataframe.dataframe import DataFrame, in_schema
