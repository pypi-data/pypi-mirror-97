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

class Pivot:
    
    def __init__(self,
        data = None,
        partition_columns = None,
        target_columns = None,
        pivot_column = None,
        pivot_keys = None,
        numeric_pivotkey = False,
        num_rows = None,
        data_sequence_column = None,
        data_partition_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The Pivot function pivots data that is stored in rows into columns.
            It outputs a teradataml DataFrame whose columns are based on the
            individual values from an input teradataml DataFrame column. The schema
            of the output teradataml DataFrame depends on the arguments of the
            function. The function handles missing or NULL values automatically.


        PARAMETERS:
            data:
                Required Argument.
                The teradataml DataFrame containing the data to be pivoted.

            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)

            partition_columns:
                Required Argument.
                Specifies the same columns as the data_partition_column clause (in
                any order).
                Types: str OR list of Strings (str)

            target_columns:
                Required Argument.
                Specifies the names of the input columns that contain the values
                to pivot.
                Types: str OR list of Strings (str)

            pivot_column:
                Optional Argument.
                Specifies the name of the column that contains the pivot keys.
                If the pivot_column argument contains numeric values, then the
                function casts them to VARCHAR. If you omit the num_rows
                argument, then you must specify this argument.
                Note: If you specify the pivot_column argument, then you must
                      order the input data; otherwise, the output teradataml DataFrame
                      column content is non-deterministic.
                Types: str

            pivot_keys:
                Optional Argument.
                If you specify the pivot_column argument, then this argument
                specifies the names of the pivot keys. Do not use this argument
                without the pivot_column argument. If pivot_column contains a value
                that is not specified as a pivot_keys, then the function ignores the
                row containing that value. pivot_keys is required when pivot_column
                is used.
                Types: str OR list of Strings (str)

            numeric_pivotkey:
                Optional Argument.
                Indicates whether the pivot key values are numeric values.
                Default Value: False
                Types: bool

            num_rows:
                Optional Argument.
                Specifies the maximum number of rows in any partition. If a
                partition has fewer than num_rows rows, then the function adds
                NULL values; if a partition has more than num_rows rows, then
                the function omits the extra rows. If you omit this argument,
                then you must specify the pivot_column argument.
                Note: With this argument, the data_order_column is optional. If
                      omitted, the order of values can vary. The function adds NULL
                      values at the end.
                Types: int

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of Pivot.
            Output teradataml DataFrames can be accessed using attribute
            references, such as PivotObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data('Pivot', "pivot_input")

            # Create teradataml DataFrame objects.
            pivot_input = DataFrame.from_table("pivot_input")

            # Example 1 - This example specifies the pivot_column argument and
            # with the pivot_keys argument, which specifies the values from the
            # pivot_column to use as pivot keys. Because pivot_keys does not
            # include 'dewpoint', the function ignores rows that include 'dewpoint'.
            pivot_out1 = Pivot(data=pivot_input,
                        data_partition_column=['sn','city','week'],
                        partition_columns=['sn','city','week'],
                        target_columns='value1',
                        pivot_column='attribute',
                        pivot_keys=['temp','pressure'],
                        numeric_pivotkey=False,
                        data_sequence_column='sn')

            # Print the result.
            print(pivot_out1)

            # Example 2 - Specify the num.rows argument instead of specifying
            # the pivot.column argument.
            pivot_out2 = Pivot(data=pivot_input,
                        data_partition_column=['sn','city','week'],
                        partition_columns=['sn','city','week'],
                        target_columns='value1',
                        num_rows=3,
                        numeric_pivotkey=False)

            # Print the result.
            print(pivot_out2.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.partition_columns  = partition_columns 
        self.target_columns  = target_columns 
        self.pivot_column  = pivot_column 
        self.pivot_keys  = pivot_keys 
        self.numeric_pivotkey  = numeric_pivotkey 
        self.num_rows  = num_rows 
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, False, (str,list)])
        self.__arg_info_matrix.append(["target_columns", self.target_columns, False, (str,list)])
        self.__arg_info_matrix.append(["pivot_column", self.pivot_column, True, (str)])
        self.__arg_info_matrix.append(["pivot_keys", self.pivot_keys, True, (str,list)])
        self.__arg_info_matrix.append(["numeric_pivotkey", self.numeric_pivotkey, True, (bool)])
        self.__arg_info_matrix.append(["num_rows", self.num_rows, True, (int)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.target_columns, "target_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.target_columns, "target_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.pivot_column, "pivot_column")
        self.__awu._validate_dataframe_has_argument_columns(self.pivot_column, "pivot_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
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
        
        self.__func_other_arg_sql_names.append("PartitionColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.pivot_column is not None:
            self.__func_other_arg_sql_names.append("PivotColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.pivot_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.num_rows is not None:
            self.__func_other_arg_sql_names.append("NumberOfRows")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_rows, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.pivot_keys is not None:
            self.__func_other_arg_sql_names.append("PivotKeys")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.pivot_keys, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.numeric_pivotkey is not None and self.numeric_pivotkey != False:
            self.__func_other_arg_sql_names.append("NumericPivotKey")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.numeric_pivotkey, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
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
        self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "Pivoting"
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
        Returns the string representation for a Pivot class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
