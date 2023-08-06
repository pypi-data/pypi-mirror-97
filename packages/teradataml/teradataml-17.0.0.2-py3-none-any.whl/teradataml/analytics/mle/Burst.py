#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 2.5
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

class Burst:
    
    def __init__(self,
        data = None,
        time_data = None,
        time_column = None,
        value_columns = None,
        time_interval = None,
        time_datatype = None,
        value_datatype = None,
        start_time = None,
        end_time = None,
        num_points = None,
        values_before_first = None,
        values_after_last = None,
        split_criteria = "nosplit",
        seed = None,
        accumulate = None,
        data_sequence_column = None,
        time_data_sequence_column = None,
        data_partition_column = None,
        time_data_partition_column = None,
        data_order_column = None,
        time_data_order_column = None):
        """
        DESCRIPTION:
            The Burst function bursts (splits) a time interval into a series of
            shorter "burst" intervals and allocates values from the time
            intervals into the new, shorter subintervals. The Burst function is
            useful for allocating values from overlapping time intervals into
            user-defined time intervals (for example, when a cable company has
            customer data from overlapping time intervals, which it wants to
            analyze by dividing into uniform time intervals). The Burst function
            supports several allocation methods.


        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame name which contains time
                series.

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

            time_data:
                Optional Argument.
                Specifies the teradataml DataFrame name which contains time.

            time_data_partition_column:
                Optional Argument. Required if time_data is specified.
                Specifies Partition By columns for time_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)

            time_data_order_column:
                Optional Argument.
                Specifies Order By columns for time_data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)

            time_column:
                Required Argument.
                Specifies the names of the data teradataml DataFrame columns
                that contain the start and end times of the time interval to be
                burst.
                Types: str OR list of Strings (str)

            value_columns:
                Required Argument.
                Specifies the names of data teradataml DataFrame columns to
                copy to the output teradataml DataFrame.
                Types: str OR list of Strings (str)

            time_interval:
                Optional Argument.
                Specifies the length of each burst time interval.
                Note: Specify exactly one of time_data, time_interval, or
                      num_points.
                Types: float

            time_datatype:
                Optional Argument.
                Specifies the data type of the output columns that correspond to the
                input teradataml DataFrame columns that time_column specifies
                (start_time_column and end_time_column). If you omit this argument,
                then the function infers the data type of start_time_column and
                end_time_column from the input teradataml DataFrame and uses the
                inferred data type for the corresponding output teradataml DataFrame
                columns. If you specify this argument, then the function can
                transform the input data to the specified output data type only if
                both the input column data type and the specified output column data
                type are in this list: int, float.
                Types: str

            value_datatype:
                Optional Argument.
                Specifies the data types of the output columns that correspond
                to the input teradataml DataFrame columns that value_columns
                specifies. If you omit this argument, then the function infers
                the data type of each value_column from the input teradataml
                DataFrame and uses the inferred data type for the corresponding
                output teradataml DataFrame column. If you specify value_datatype,
                then it must be the same size as value_columns. That is, if
                value_columns specifies n columns, then value_datatype must
                specify n data types. For i in [1, n], value_column_i has
                value_type_i. However, value_type_i can be empty; for example:
                value_columns (c1, c2, c3), value_datatype (int, ,str).
                If you specify this argument, then the function can transform
                the input data to the specified output data type only if both
                the input column data type and the specified output column data
                type are in this list: int, float.
                Types: str

            start_time:
                Optional Argument.
                Specifies the start time for the time interval to be burst. The
                default is the value in start_time_column.
                Types: str

            end_time:
                Optional Argument.
                Specifies the end time for the time interval to be burst. The default
                is the value in end_time_column.
                Types: str

            num_points:
                Optional Argument.
                Specifies the number of data points in each burst time interval.
                Note: Specify exactly one of time_data, time_interval, or num_points.
                Types: int

            values_before_first:
                Optional Argument.
                Specifies the values to use if start_time is before start_time_column.
                Each of these values must have the same data type as its corresponding
                value_column. Values of data type str are case-insensitive.
                If you specify values_before_first, then it must be the same size as
                value_columns. That is, if value_columns specifies n columns,
                then values_before_first must specify n values. For i in [1,
                n], value_column_i has the value before_first_value_i. However,
                before_first_value_i can be empty; for example: value_columns (c1,
                c2, c3), values_before_first (1, ,"abc"). If before_first_value_i
                is empty, then value_column_i has the value NULL. If you do not
                specify values_before_first, then value_column_i has the value
                NULL for i in [1, n].
                Types: str

            values_after_last:
                Optional Argument.
                Specifies the values to use if end_time is after end_time_column.
                Each of these values must have the same data type as its
                corresponding value_column. Values of data type str are
                case-insensitive. If you specify values_after_last, then it
                must be the same size as value_columns. That is, if value_columns
                specifies n columns, then ValuesAfterLast must specify n values.
                For i in [1, n], value_column_i has the value after_last_value_i.
                However, after_last_value_i can be empty; for example:
                value.columns (c1, c2, c3), values_after_last (1, ,"abc").
                If after_last_value_i is empty, then value_column_i has the
                value NULL. If you do not specify values_after_last, then
                value_column_i has the value NULL for i in [1, n].
                Types: str

            split_criteria:
                Optional Argument.
                Specifies the split criteria of the value_columns.
                Default Value: "nosplit"
                Permitted Values: nosplit, proportional, random, gaussian, poisson
                Types: str

            seed:
                Optional Argument.
                Specifies the seed for the random number generator.
                Types: int

            accumulate:
                Optional Argument.
                Specifies the names of input_table columns (other than those
                specified by time_column and value_columns) to copy to the output
                teradataml DataFrame. By default, the function copies to the
                output teradataml DataFrame only the columns specified by
                time_column and value_columns.
                Types: str OR list of Strings (str)

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)

            time_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "time_data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of Burst.
            Output teradataml DataFrames can be accessed using attribute
            references, such as BurstObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("burst", ["burst_data", "finance_data", "time_table2"])

            # Create teradataml DataFrame objects.
            burst_data = DataFrame.from_table("burst_data")
            finance_data = DataFrame.from_table("finance_data")
            time_table2 = DataFrame.from_table("time_table2")

            # Example 1 - Use "time_interval" argument to burst the data for
            # a duration of 1 day (86400 seconds).
            Burst_out1 = Burst(data = burst_data,
                              data_partition_column = ["id"],
                              time_column = ["start_time_column", "end_time_column"],
                              value_columns = ["num_custs"],
                              time_interval = 86400.0,
                              start_time = "08/01/2010",
                              end_time = "08/10/2010",
                              split_criteria = "nosplit",
                              accumulate = ["id"]
                              )

            # Print the result DataFrame
            print(Burst_out1)

            # Example 2 - The "split_criteria" for the "value_column" used in
            # this example is proportional.
            Burst_out2 = Burst(data = burst_data,
                              data_partition_column = ["id"],
                              time_column = ["start_time_column", "end_time_column"],
                              value_columns = ["num_custs"],
                              time_interval = 86400.0,
                              start_time = "08/01/2010",
                              end_time = "08/10/2010",
                              split_criteria = "proportional",
                              accumulate = ["id"]
                              )

            # Print the result DataFrame
            print(Burst_out2.result)

            # Example 3 - The "split_criteria" for the "value_column" used in
            # this example is gaussian.
            Burst_out3 = Burst(data = burst_data,
                              data_partition_column = ["id"],
                              time_column = ["start_time_column", "end_time_column"],
                              value_columns = ["num_custs"],
                              time_interval = 86400.0,
                              start_time = "08/01/2010",
                              end_time = "08/10/2010",
                              split_criteria = "gaussian",
                              accumulate = ["id"]
                              )

            # Print the result DataFrame
            print(Burst_out3)

            # Example 4 - Uses a "time_data" argument, "values_before_first"
            # and "values"after_last". The "time_data" option allows the use of
            # different time intervals and partitions the data accordingly.
            Burst_out4 = Burst(data = finance_data,
                              data_partition_column = ["id"],
                              time_data = time_table2,
                              time_data_partition_column = ["id"],
                              time_column = ["start_time_column", "end_time_column"],
                              value_columns = ["expenditure", "income", "investment"],
                              start_time = "06/30/1967",
                              end_time = "07/10/1967",
                              values_before_first = ["NULL","NULL","NULL"],
                              values_after_last = ["NULL","NULL","NULL"],
                              accumulate = ["id"]
                              )

            # Print the result DataFrame
            print(Burst_out4)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.time_data  = time_data 
        self.time_column  = time_column 
        self.value_columns  = value_columns 
        self.time_interval  = time_interval 
        self.time_datatype  = time_datatype 
        self.value_datatype  = value_datatype 
        self.start_time  = start_time 
        self.end_time  = end_time 
        self.num_points  = num_points 
        self.values_before_first  = values_before_first 
        self.values_after_last  = values_after_last 
        self.split_criteria  = split_criteria 
        self.seed  = seed 
        self.accumulate  = accumulate 
        self.data_sequence_column  = data_sequence_column 
        self.time_data_sequence_column  = time_data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.time_data_partition_column  = time_data_partition_column 
        self.data_order_column  = data_order_column 
        self.time_data_order_column  = time_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["time_data", self.time_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["time_data_partition_column", self.time_data_partition_column, self.time_data is None, (str,list)])
        self.__arg_info_matrix.append(["time_data_order_column", self.time_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["time_column", self.time_column, False, (str,list)])
        self.__arg_info_matrix.append(["value_columns", self.value_columns, False, (str,list)])
        self.__arg_info_matrix.append(["time_interval", self.time_interval, True, (float)])
        self.__arg_info_matrix.append(["time_datatype", self.time_datatype, True, (str)])
        self.__arg_info_matrix.append(["value_datatype", self.value_datatype, True, (str,list)])
        self.__arg_info_matrix.append(["start_time", self.start_time, True, (str)])
        self.__arg_info_matrix.append(["end_time", self.end_time, True, (str)])
        self.__arg_info_matrix.append(["num_points", self.num_points, True, (int)])
        self.__arg_info_matrix.append(["values_before_first", self.values_before_first, True, (str,list)])
        self.__arg_info_matrix.append(["values_after_last", self.values_after_last, True, (str,list)])
        self.__arg_info_matrix.append(["split_criteria", self.split_criteria, True, (str)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["time_data_sequence_column", self.time_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.time_data, "time_data", None)
        
        # Check for permitted values
        split_criteria_permitted_values = ["NOSPLIT", "PROPORTIONAL", "RANDOM", "GAUSSIAN", "POISSON"]
        self.__awu._validate_permitted_values(self.split_criteria, split_criteria_permitted_values, "split_criteria")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.time_column, "time_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_column, "time_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.value_columns, "value_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.value_columns, "value_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_data_sequence_column, "time_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_data_sequence_column, "time_data_sequence_column", self.time_data, "time_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.time_data_partition_column, "time_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_data_partition_column, "time_data_partition_column", self.time_data, "time_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_data_order_column, "time_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_data_order_column, "time_data_order_column", self.time_data, "time_data", False)
        
        
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
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.time_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.value_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.time_interval is not None:
            self.__func_other_arg_sql_names.append("TimeInterval")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.time_interval, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.time_datatype is not None:
            self.__func_other_arg_sql_names.append("TimeDataType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.time_datatype, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.value_datatype is not None:
            self.__func_other_arg_sql_names.append("ValueDataType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.value_datatype, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.start_time is not None:
            self.__func_other_arg_sql_names.append("StartTime")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.start_time, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.end_time is not None:
            self.__func_other_arg_sql_names.append("EndTime")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.end_time, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.split_criteria is not None and self.split_criteria != "nosplit":
            self.__func_other_arg_sql_names.append("SplitCriteria")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.split_criteria, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.num_points is not None:
            self.__func_other_arg_sql_names.append("NumPoints")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_points, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.values_before_first is not None:
            self.__func_other_arg_sql_names.append("ValuesBeforeFirst")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_before_first, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.values_after_last is not None:
            self.__func_other_arg_sql_names.append("ValuesAfterLast")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_after_last, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input_table:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.time_data_sequence_column is not None:
            sequence_input_by_list.append("time_table:" + UtilFuncs._teradata_collapse_arglist(self.time_data_sequence_column, ""))
        
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
        self.__func_input_arg_sql_names.append("input_table")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process time_data
        if self.time_data is not None:
            self.time_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.time_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.time_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("time_table")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.time_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.time_data_order_column, "\""))
        
        function_name = "Burst"
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
        Returns the string representation for a Burst class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
