#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.2
# Function Version: 1.0
# 
# ################################################################## 

import inspect
import time
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import *
from teradataml.dataframe.dataframe import DataFrame
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.options.display import display

class Sessionize:
    
    def __init__(self,
        data = None,
        time_column = None,
        time_out = None,
        click_lag = None,
        emit_null = False,
        data_partition_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The Sessionize function maps each click in a session to a unique 
            session identifier. A session is defined as a sequence of clicks by 
            one user that are separated by at most n seconds.
            
            The function is useful both for sessionization and for detecting web 
            crawler (bot) activity. It is typically used to understand user browsing
            behavior on a web site.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame.
            
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple columns 
                are used for partition.
                Types: str OR list of Strings (str)
            
            data_order_column:
                Required Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple columns 
                are used for ordering.
                Types: str OR list of Strings (str)
            
            time_column:
                Required Argument.
                Specifies the name of the input column that contains the click
                times.
                Note: The time_column must also be an data_order_column.
                Types: str
            
            time_out:
                Required Argument.
                Specifies the number of seconds at which the session times out. If 
                time_out seconds elapse after a click, then the next click
                starts a new session.
                Types: float
            
            click_lag:
                Optional Argument.
                Specifies the minimum number of seconds between clicks for the 
                session user to be considered human. If clicks are more frequent, 
                indicating that the user is a "bot," the function ignores the 
                session. The click_lag must be less than time_out.
                Types: float
            
            emit_null:
                Optional Argument.
                Specifies whether to output rows that have None values in their 
                session id and rapid fire columns, even if their time_column has 
                a None value. 
                Default Value: False
                Types: bool
         
        RETURNS:
            Instance of Sessionize.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SessionizeObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("Sessionize","sessionize_table")
            
            # Create teradataml DataFram object.
            sessionize_table = DataFrame.from_table("sessionize_table")
            
            # Example 1 - This example maps each click in a session to a unique session identifer, 
            # which uses input table web clickstream data recorded as user navigates through a web site
            # based on events — view, click, and so on which are recorded with a timestamp.
            td_sessionize_out = Sessionize(data = sessionize_table,
                                           data_partition_column = ["partition_id"],
                                           data_order_column = ["clicktime"],
                                           time_column = "clicktime",
                                           time_out = 60.0,
                                           click_lag = 0.2
                                           )
            
            # Print the result DataFrame
            print(td_sessionize_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.time_column  = time_column 
        self.time_out  = time_out 
        self.click_lag  = click_lag 
        self.emit_null  = emit_null 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["time_column", self.time_column, False, (str)])
        self.__arg_info_matrix.append(["time_out", self.time_out, False, (float)])
        self.__arg_info_matrix.append(["click_lag", self.click_lag, True, (float)])
        self.__arg_info_matrix.append(["emit_null", self.emit_null, True, (bool)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Execute ML query
            self.__execute()
            # Get the prediction type
            self._prediction_type = self.__awu._get_function_prediction_type(self)
        
        # End the timer to get the build time
        _end_time = time.time()
        
        # Calculate the build time
        self._build_time = (int)(_end_time - _start_time)
        
    def __validate(self):
        """
        Function to validate sqlmr function arguments, which verifies missing 
        arguments, input argument and table types. Also processes the 
        argument values.
        """
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.time_column, "time_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_column, "time_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TimeColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.time_column, "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TimeOut")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.time_out, ""))
        self.__func_other_arg_json_datatypes.append("DOUBLE PRECISION")
        
        if self.click_lag is not None:
            self.__func_other_arg_sql_names.append("ClickLag")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.click_lag, ""))
            self.__func_other_arg_json_datatypes.append("DOUBLE PRECISION")
        
        if self.emit_null is not None and self.emit_null != False:
            self.__func_other_arg_sql_names.append("EmitNull")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.emit_null, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "Sessionize"
        # Create instance to generate SQLMR.
        self.__aqg_obj = AnalyticQueryGenerator(function_name, 
                self.__func_input_arg_sql_names, 
                self.__func_input_table_view_query, 
                self.__func_input_dataframe_type, 
                self.__func_input_distribution, 
                self.__func_input_partition_by_cols, 
                self.__func_input_order_by_cols, 
                self.__func_other_arg_sql_names, 
                self.__func_other_args, 
                self.__func_other_arg_json_datatypes, 
                self.__func_output_args_sql_names, 
                self.__func_output_args, 
                engine="ENGINE_SQL")
        # Invoke call to SQL-MR generation.
        self.sqlmr_query = self.__aqg_obj._gen_sqlmr_select_stmt_sql()
        
        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)
        
        # Set the algorithm name for Model Cataloging.
        self._algorithm_name = self.__aqg_obj._get_alias_name_for_function(function_name)
        
    def __execute(self):
        """
        Function to execute SQL-MR queries. 
        Create DataFrames for the required SQL-MR outputs.
        """
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        try:
            # Generate the output.
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
    def show_query(self):
        """
        Function to return the underlying SQL query.
        When model object is created using retrieve_model(), then None is returned.
        """
        return self.sqlmr_query
        
    def get_prediction_type(self):
        """
        Function to return the Prediction type of the algorithm.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._prediction_type
        
    def get_target_column(self):
        """
        Function to return the Target Column of the algorithm.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._target_column
        
    def get_build_time(self):
        """
        Function to return the build time of the algorithm in seconds.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._build_time
        
    def _get_algorithm_name(self):
        """
        Function to return the name of the algorithm.
        """
        return self._algorithm_name
        
    def _get_sql_specific_attributes(self):
        """
        Function to return the dictionary containing the SQL specific attributes of the algorithm.
        """
        return self._sql_specific_attributes
        
    @classmethod
    def _from_model_catalog(cls,
        result = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("result", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.result  = result 
        
        # Initialize the sqlmr_query class attribute.
        obj.sqlmr_query = None
        
        # Initialize the SQL specific Model Cataloging attributes.
        obj._sql_specific_attributes = None
        obj._target_column = target_column
        obj._prediction_type = prediction_type
        obj._algorithm_name = algorithm_name
        obj._build_time = build_time
        
        # Update output table data frames.
        obj._mlresults = []
        obj.result = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.result), source_type="table", database_name=UtilFuncs._extract_db_name(obj.result))
        obj._mlresults.append(obj.result)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a Sessionize class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
