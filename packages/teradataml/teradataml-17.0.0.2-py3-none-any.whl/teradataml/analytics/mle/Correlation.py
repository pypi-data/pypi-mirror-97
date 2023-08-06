#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Bhavana N (bhavana.n@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.9
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

class Correlation:
    
    def __init__(self,
        data = None,
        group_by_columns = None,
        target_columns = None,
        key_name = None,
        data_sequence_column = None,
        data_partition_column = "ANY",
        data_order_column = None,
        reduce_partition_column = None):
        """
        DESCRIPTION:
            The Correlation function, which is composed of the Correlation Reduce and
            Correlation Map functions, computes global correlations between specified
            pairs of teradataml DataFrame columns. Measuring correlation lets you
            determine if the value of one variable is useful in predicting the
            value of another.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame that contains the Xi and Yi pairs.
         
            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
         
            reduce_partition_column:
                Required Argument.
                Specifies Partition By columns for data for Correlation Reduce.
                Values to this argument can be provided as list, if multiple columns
                are used for partition. If group_by_columns argument is provided,
                value must be [key_name, group_by_columns]. If group_by_columns
                is not provided, value must be key_name argument value.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            group_by_columns:
                Optional Argument.
                Specifies the names of the input columns that define the group for
                correlation calculation. By default, all input columns belong to a
                single group, for which the function calculates correlation. If group_by_columns
                is specified, columns provided to this argument should also appear in
                'data_partition_column' and 'reduce_partition_column'.
                Types: str OR list of Strings (str)
         
            target_columns:
                Required Argument.
                Specifies pairs of columns for which to calculate correlations. For
                each column pair, "col_name1:col_name2", the function calculates the
                correlation between col_name1 and col_name2. For each column range,
                "[col_index1:col_index2]", the function calculates the correlation
                between every pair of columns in the range. For example, if you
                specify "[1:3]", the function calculates the correlation between the
                pairs (1,2), (1,3), (2,3), (1,1), (2,2) and (3,3). The minimum value of
                col_index1 is 0, and col_index1 must be less than col_index2.
                Types: str OR list of strs
         
            key_name:
                Required Argument.
                Specifies the name for the Correlation output teradataml DataFrame
                column that contains the correlations, and by which the Correlation
                output teradataml DataFrame is partitioned.
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Correlation.
            Output teradataml DataFrames can be accessed using attribute
            references, such as CorrelationObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
         
            # Load the data to run the example.
            load_example_data("correlation","corr_input")
         
            # Create teradataml DataFrame
            corr_input = DataFrame.from_table("corr_input")
         
            # Example 1: Include PARTITION BY Clause and input columns that
            # define the group for correlation calculation
            correlation_output1 = Correlation(data=corr_input,
                                    data_partition_column='state',
                                    group_by_columns='state',
                                    key_name='test',
                                    target_columns='[2:3]',
                                    data_sequence_column='state',
                                    reduce_partition_column=['test', 'state']
                                    )
         
            # Print the result DataFrame
            print(correlation_output1.result)
         
            # Example 2: Specifying all input columns for correlation calculation.
            # By default, if group_by_columns is not mentioned all input columns belong to a single group,
            # for which the function calculates correlation
            correlation_output2 = Correlation(data=corr_input,
                                    key_name='test',
                                    target_columns='[2:3]',
                                    data_sequence_column='state',
                                    reduce_partition_column=['test']
                                    )
            # Print the result DataFrame
            print(correlation_output2.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.group_by_columns  = group_by_columns 
        self.target_columns  = target_columns 
        self.key_name  = key_name 
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column
        self.data_order_column = data_order_column
        self.reduce_partition_column = reduce_partition_column
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["group_by_columns", self.group_by_columns, True, (str,list)])
        self.__arg_info_matrix.append(["target_columns", self.target_columns, False, (str,list)])
        self.__arg_info_matrix.append(["key_name", self.key_name, False, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["reduce_partition_column", self.reduce_partition_column, False, (str, list)])
        
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
        self.__awu._validate_input_columns_not_empty(self.group_by_columns, "group_by_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.group_by_columns, "group_by_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
            self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)

        self.__awu._validate_input_columns_not_empty(self.reduce_partition_column, "reduce_partition_column")
        if isinstance(self.reduce_partition_column, str):
            self.reduce_partition_column = [self.reduce_partition_column]
            # key_name must be present in reduce_partition_column and key name can be any string
            # So checking only for other value present in reduce_partition_column
            self.__awu._validate_dataframe_has_argument_columns(
                list(set(self.reduce_partition_column) - set([self.key_name])),
                "reduce_partition_column", self.data, "data", True)

        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.key_name, "key_name")
        
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
        
        if self.group_by_columns is not None:
            self.__func_other_arg_sql_names.append("GroupByColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.group_by_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.target_columns, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("KeyName")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.key_name, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self.__func_other_args.append(sequence_input_by_arg_value)
            self.__func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
            self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "CorrelationMap"
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
                engine="ENGINE_ML")
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.reduce_partition_column = UtilFuncs._teradata_collapse_arglist(self.reduce_partition_column,"\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__aqg_obj._gen_sqlmr_invocation_sql())
        self.__func_input_dataframe_type.append("TABLE")
        self.__func_input_partition_by_cols.append(self.reduce_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))

        function_name = "CorrelationReduce"
        # Create instance for mapreduce SQLMR.
        self.__aqg_obj = AnalyticQueryGenerator(function_name,
                self.__func_input_arg_sql_names, 
                self.__func_input_table_view_query, 
                self.__func_input_dataframe_type, 
                self.__func_input_distribution, 
                self.__func_input_partition_by_cols, 
                self.__func_input_order_by_cols, 
                [], 
                [], 
                [], 
                self.__func_output_args_sql_names, 
                self.__func_output_args, 
                engine="ENGINE_ML")
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
        Returns the string representation for a Correlation class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
