#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Bhavana N (bhavana.n@teradata.com)
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

class MovingAverage:
    
    def __init__(self,
        data = None,
        target_columns = None,
        alpha = 0.1,
        start_rows = 2,
        window_size = 10,
        include_first = False,
        mavgtype = "C",
        data_partition_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The MovingAverage function calculates the moving average of the 
            target columns based on the moving average types ("mvgtype").
            Possible moving average types:
                'C' Cumulative moving average.
                'E' Exponential moving average.
                'M' Modified moving average.
                'S' Simple moving average.
                'T' Triangular moving average.
                'W' Weighted moving average.
            
            Note: This function is only available when teradataml is connected
                  to Vantage 1.1 or later versions.
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the 
                columns.
            
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Types: str OR list of Strings (str)
            
            data_order_column:
                Required Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            target_columns:
                Optional Argument.
                Specifies the input column names for which the moving average is to 
                be computed. If you omit this argument, then the function copies 
                every input column to the output teradataml DataFrame but does not 
                compute moving average.
                Types: str OR list of Strings (str)
            
            alpha:
                Optional Argument.
                Specifies the damping factor, a value in the range [0, 1], which 
                represents a percentage in the range [0, 100]. For example, if alpha 
                is 0.2, then the damping factor is 20%. A higher alpha discounts 
                older observations faster. Only used if "mavgtype" is E.
                For other moving average types this value will be ignored.
                Default Value: 0.1
                Types: float
            
            start_rows:
                Optional Argument.
                Specifies the number of rows at the beginning of the time series that 
                the function skips before it begins the calculation of the 
                exponential moving average. The function uses the arithmetic average 
                of these rows as the initial value of the exponential moving average.
                Only used if "mavgtype" is E. For other moving average types 
                this value will be ignored.
                Default Value: 2
                Types: int
            
            window_size:
                Optional Argument.
                Specifies the number of previous values to include in the computation 
                of the moving average if "mavgtype" is M, S, T, and W.
                For other moving average types this value will be ignored.
                Default Value: 10
                Types: int
            
            include_first:
                Optional Argument.
                Specifies whether the first START_ROWS rows should be included in the 
                output or not. Only used if "mavgtype" is S, M, W, E, T. 
                For cumulative moving average types this value will be ignored.
                Default Value: False
                Types: bool
            
            mavgtype:
                Optional Argument.
                Specify the moving average type that needs to be used for computing 
                moving averages of "target_columns".
                Following are the different type of averages calculated by MovingAverage function:
                    S: The MovingAverage function computes the simple moving average of points in a
                       series.
                    W: The MovingAverage function computes the weighted moving average the average of
                       points in a time series, applying weights to older values. The 
                       weights for the older values decrease arithmetically.
                    E: The MovingAverage function computes the exponential moving average
                       of the points in a time series, exponentially decreasing the
                       weights of older values.
                    C: The MovingAverage function computes the cumulative moving average of a value
                       from the beginning of a series.
                    M: The MovingAverage function computes moving average of points in series.
                    T: The MovingAverage function computes double-smoothed average of points in series.
                Default Value: "C"
                Permitted Values: C, S, M, W, E, T
                Types: str
         
        RETURNS:
            Instance of MovingAverage.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as MovingAverageObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("movavg", "ibm_stock")
            
            # Create teradataml DataFrame objects.
            ibm_stock = DataFrame.from_table("ibm_stock")
         
            # Example1 - Calculating the cumulative moving average for data in 
            # the stockprice column.
            movingaverage_cmavg =  MovingAverage(data=ibm_stock,
                                            data_order_column='name',
                                            data_partition_column='name',
                                            target_columns='stockprice',
                                            mavgtype='C'
                                            )
            
            # Print the results.
            print(movingaverage_cmavg.result)
         
            # Example2 - Calculating the exponential moving average for data in 
            # the stockprice column.
            movingaverage_emavg =  MovingAverage(data=ibm_stock,
                                            data_partition_column='name',
                                            data_order_column='name',
                                            target_columns='stockprice',
                                            include_first=False,
                                            alpha=0.1,
                                            start_rows=10,
                                            mavgtype='E'
                                            )
            # Print the results.
            print(movingaverage_emavg.result)
         
            # Example3 - Calculating the simple moving average for data in 
            # the stockprice column.
            movingaverage_smavg =  MovingAverage(data=ibm_stock,
                                            data_partition_column='name',
                                            data_order_column='name',
                                            target_columns='stockprice',
                                            include_first=False,
                                            window_size=6,
                                            mavgtype='S'
                                            )
            # Print the results.
            print(movingaverage_smavg.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.target_columns  = target_columns 
        self.alpha  = alpha 
        self.start_rows  = start_rows 
        self.window_size  = window_size 
        self.include_first  = include_first 
        self.mavgtype  = mavgtype 
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
        self.__arg_info_matrix.append(["target_columns", self.target_columns, True, (str,list)])
        self.__arg_info_matrix.append(["alpha", self.alpha, True, (float)])
        self.__arg_info_matrix.append(["start_rows", self.start_rows, True, (int)])
        self.__arg_info_matrix.append(["window_size", self.window_size, True, (int)])
        self.__arg_info_matrix.append(["include_first", self.include_first, True, (bool)])
        self.__arg_info_matrix.append(["mavgtype", self.mavgtype, True, (str)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Process output table schema
            self.__process_output_column_info()
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
        
        # Check for permitted values
        mavgtype_permitted_values = ["C", "S", "M", "W", "E", "T"]
        self.__awu._validate_permitted_values(self.mavgtype, mavgtype_permitted_values, "mavgtype")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.target_columns, "target_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.target_columns, "target_columns", self.data, "data", False)
        
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
        
        if self.target_columns is not None:
            self.__func_other_arg_sql_names.append("TargetColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.target_columns, "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.include_first is not None and self.include_first != False:
            self.__func_other_arg_sql_names.append("IncludeFirst")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.include_first, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.alpha is not None and self.alpha != 0.1:
            self.__func_other_arg_sql_names.append("Alpha")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.alpha, ""))
            self.__func_other_arg_json_datatypes.append("DOUBLE PRECISION")
        
        if self.start_rows is not None and self.start_rows != 2:
            self.__func_other_arg_sql_names.append("StartRows")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.start_rows, ""))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.window_size is not None and self.window_size != 10:
            self.__func_other_arg_sql_names.append("WindowSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_size, ""))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.mavgtype is not None and self.mavgtype != "C":
            self.__func_other_arg_sql_names.append("MavgType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mavgtype, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "MovingAverage"
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
        Function to generate AED nodes for output tables.
        This makes a call aed_ml_query() and then output table dataframes are created.
        """
        # Create a list of input node ids contributing to a query.
        self.__input_nodeids = []
        self.__input_nodeids.append(self.data._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "MovingAverage", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)
        
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.result)
        
    def __process_output_column_info(self):
        """ 
        Function to process the output schema for all the ouptut tables.
        This function generates list of column names and column types
        for each generated output tables, which can be used to create metaexpr.
        """
        # Collecting STDOUT output column information.
        stdout_column_info_name = []
        stdout_column_info_type = []
        for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=None, columns=None):
            stdout_column_info_name.append(column_name)
            stdout_column_info_type.append(column_type)
            
        if self.mavgtype == "C":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_cmavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        if self.mavgtype == "S":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_smavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        if self.mavgtype == "E":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_emavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        if self.mavgtype == "W":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_wmavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        if self.mavgtype == "M":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_mmavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        if self.mavgtype == "T":
            if self.target_columns is not None:
                for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.data, parameter=self.target_columns, columns=None):
                    stdout_column_info_name.append(column_name + "_tmavg")
                    stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("double precision"))
                    
        
        self.__stdout_column_info = zip(stdout_column_info_name, stdout_column_info_type)
        
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
        Returns the string representation for a MovingAverage class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
