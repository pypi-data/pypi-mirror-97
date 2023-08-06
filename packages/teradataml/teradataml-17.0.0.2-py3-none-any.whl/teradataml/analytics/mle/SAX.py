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

class SAX:
    
    def __init__(self,
        data = None,
        meanstats_data = None,
        stdevstats_data = None,
        value_columns = None,
        time_column = None,
        window_type = "global",
        output = "string",
        mean = None,
        st_dev = None,
        window_size = None,
        output_frequency = 1,
        points_persymbol = 1,
        symbols_perwindow = None,
        alphabet_size = 4,
        bitmap_level = 2,
        print_stats = False,
        accumulate = None,
        data_sequence_column = None,
        meanstats_data_sequence_column = None,
        stdevstats_data_sequence_column = None,
        data_partition_column = None,
        meanstats_data_partition_column = None,
        stdevstats_data_partition_column = None,
        data_order_column = None,
        meanstats_data_order_column = None,
        stdevstats_data_order_column = None):
        """
        DESCRIPTION:
            The SAX (Symbolic Aggregate approXimation) function transforms a time
            series data item into a smaller sequence of symbols, which are more
            suitable for additional types of manipulation, because of their smaller
            size and the relative ease with which patterns can be identified and
            compared. Input and output formats allow it to be analyzed using NPath
            or Shapelet Functions, or by other hashing or regular-expression pattern
            matching algorithms.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame containing timeseries data.
         
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Required Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            meanstats_data:
                Optional Argument.
                Specifies teradataml DataFrame that contains the global means of each
                value_column of the input teradataml DataFrame.
         
            meanstats_data_partition_column:
                Optional Argument. Required if 'meanstats_data' is used.
                Specifies Partition By columns for meanstats_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            meanstats_data_order_column:
                Optional Argument.
                Specifies Order By columns for meanstats_data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            stdevstats_data:
                Optional Argument.
                Specifies teradataml DataFrame that contains the global standard deviations
                of each value_column of the input teradataml DataFrame.
         
            stdevstats_data_partition_column:
                Optional Argument. Required if 'stdevstats_data' is used.
                Specifies Partition By columns for stdevstats_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            stdevstats_data_order_column:
                Optional Argument.
                Specifies Order By columns for stdevstats_data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            value_columns:
                Required Argument.
                Specifies the names of the input teradataml DataFrame columns that
                contain the time series data to be transformed.
                Types: str OR list of Strings (str)
         
            time_column:
                Optional Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the time axis of the data.
                Types: str
         
            window_type:
                Optional Argument.
                Determines how much data the function processes at one time:
                    "global": The function computes the SAX code using a single
                              mean and standard deviation for the entire data set.
                    "sliding": The function recomputes the mean and standard
                               deviation for a sliding window of the data set.
                Default Value: "global"
                Permitted Values: sliding, global
                Types: str
         
            output:
                Optional Argument.
                Determines how the function outputs the results:
                    "string": The function outputs a list of SAX codes for each window.
                    "bytes": The function outputs the list of SAX codes as compact
                             byte arrays (which are not "human-readable").
                    "bitmap": The function outputs a JSON representation of a SAX bitmap.
                    "characters": The function outputs one character for each line.
                Default Value: "string"
                Permitted Values: STRING, BITMAP, BYTES, CHARACTERS
                Types: str
         
            mean:
                Optional Argument.
                Specifies the global mean values that the function uses to calculate
                the SAX code for every partition. A mean value has the data type
                float. If mean specifies only one value and value_columns specifies
                multiple columns, then the specified value applies to every
                value_column. If mean specifies multiple values, then it must specify
                a value for each value_column. The nth mean value corresponds to the
                nth value_column.
                Tip: To specify a different global mean value for each partition,
                use the multiple-input syntax and put the values in the meanstats
                teradataml DataFrame.
                Types: float OR list of floats
         
            st_dev:
                Optional Argument.
                Specifies the global standard deviation values that the function uses
                to calculate the SAX code for every partition. A stdev value has the
                data type float and its value must be greater than 0. If Stdev
                specifies only one value and value_columns specifies multiple
                columns, then the specified value applies to every value_column. If
                Stdev specifies multiple values, then it must specify a value for
                each value_column. The nth stdev value corresponds to the nth
                value_column.
                Tip: To specify a different global standard deviation value for each
                partition, use the multiple-input syntax and put the values in the
                stdevstats teradataml DataFrame.
                Types: float OR list of floats
         
            window_size:
                Required if window_type is 'sliding', disallowed otherwise.
                Specifies the size of the sliding window. The value must be an
                integer greater than 0.
                Types: int
         
            output_frequency:
                Optional Argument.
                Specifies the number of data points that the window slides between
                successive outputs. The value must be an integer greater than 0.
                Note: window_type value must be "sliding" and Output value cannot be
                      "characters". If window_type is "sliding" and Output value is
                      "characters", then output_frequency is automatically set to the value
                      of window_size, to ensure that a single character is assigned to each
                      time point. If the number of data points in the time series is not an
                      integer multiple of the window size, then the function ignores the
                      leftover parts.
                Default Value: 1
                Types: int
         
            points_persymbol:
                Optional Argument.
                Specifies the number of data points to be converted into one SAX
                symbol. Each value must be an integer greater than 0.
                Note: window_type value must be "global".
                Default Value: 1
                Types: int
         
            symbols_perwindow:
                Optional Argument.
                Specifies the number of SAX symbols to be generated for each window.
                Each value must be an integer greater than 0. The default value is
                the value of window_size.
                Note: window_type value must be "sliding".
                Types: int
         
            alphabet_size:
                Optional Argument.
                Specifies the number of symbols in the SAX alphabet. The value must
                be an integer in the range [2, 20].
                Default Value: 4
                Types: int
         
            bitmap_level:
                Optional Argument.
                Specifies the number of consecutive symbols to be converted to one
                symbol on a bitmap. For bitmap level 1, the bitmap contains the
                symbols "a", "b", "c", and so on; for bitmap level 2, the bitmap
                contains the symbols "aa", "ab", "ac", and so on. The input value
                must be an integer in the range [1, 4].
                Note: Output value must be "bitmap".
                Default Value: 2
                Types: int
         
            print_stats:
                Optional Argument.
                Specifies whether the function prints the mean and standard
                deviation.
                Note: Output value must be "string".
                Default Value: False
                Types: bool
         
            accumulate:
                Optional Argument.
                The names of the input teradataml DataFrame columns that are to
                appear in the output teradataml DataFrame. For each sequence in the
                input teradataml DataFrame, SAX choose the value corresponding to
                the first time point in the sequence to output as the accumulate value.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            meanstats_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "meanstats_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            stdevstats_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "stdevstats_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of SAX.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SAXObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("sax", "finance_data3")
         
            # Create teradataml DataFrame objects
            finance_data3 = DataFrame.from_table("finance_data3")
         
            # Example 1 - This example uses window_type as global and default output value.
            SAX_Out = SAX(data = finance_data3,
                         data_partition_column = ["id"],
                         data_order_column = ["period"],
                         value_columns = ["expenditure","income","investment"],
                         time_column = "period",
                         window_type = "global",
                         print_stats = True,
                         accumulate = ["id"]
                        )
            # Print the results
            print(SAX_Out)
         
            # Example 2 - This example uses window_type as sliding and default output value.
            #           window_size should also be specified when window_type is set as sliding.
            SAX_Out2 = SAX(data = finance_data3,
                          data_partition_column = ["id"],
                          data_order_column = ["period"],
                          value_columns = ["expenditure"],
                          time_column = "period",
                          window_type = "sliding",
                          window_size = 20,
                          print_stats = True,
                          accumulate = ["id"]
                         )
            # Print the results
            print(SAX_Out2)
         
            # Example 3 - This example uses the multiple-input version, where the
            #               mean and standard deviation statistics are applied globally with
            #               meanstats and the stdevstats tables.
            meanstats = DataFrame.from_table("finance_data3").groupby("id").mean()
            meanstats = meanstats.assign(drop_columns=True, id=meanstats.id, expenditure=meanstats.mean_expenditure,
                                         income=meanstats.mean_income, investment=meanstats.mean_investment)
            stdevstats = DataFrame.from_table("finance_data3").groupby("id").std()
            stdevstats = stdevstats.assign(drop_columns=True, id=stdevstats.id, expenditure=stdevstats.std_expenditure,
                                         income=stdevstats.std_income, investment=stdevstats.std_investment)
         
            SAX_Out3 = SAX(data = finance_data3,
                          data_partition_column = ["id"],
                          data_order_column = ["id"],
                          meanstats_data = meanstats,
                          meanstats_data_partition_column = ["id"],
                          stdevstats_data = stdevstats,
                          stdevstats_data_partition_column = ["id"],
                          value_columns = ["expenditure","income","investment"],
                          time_column = "period",
                          window_type = "global",
                          accumulate = ["id"]
                         )
            # Print the results
            print(SAX_Out3)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.meanstats_data  = meanstats_data 
        self.stdevstats_data  = stdevstats_data 
        self.value_columns  = value_columns 
        self.time_column  = time_column 
        self.window_type  = window_type 
        self.output  = output 
        self.mean  = mean 
        self.st_dev  = st_dev 
        self.window_size  = window_size 
        self.output_frequency  = output_frequency 
        self.points_persymbol  = points_persymbol 
        self.symbols_perwindow  = symbols_perwindow 
        self.alphabet_size  = alphabet_size 
        self.bitmap_level  = bitmap_level 
        self.print_stats  = print_stats 
        self.accumulate  = accumulate 
        self.data_sequence_column  = data_sequence_column 
        self.meanstats_data_sequence_column  = meanstats_data_sequence_column 
        self.stdevstats_data_sequence_column  = stdevstats_data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.meanstats_data_partition_column  = meanstats_data_partition_column 
        self.stdevstats_data_partition_column  = stdevstats_data_partition_column 
        self.data_order_column  = data_order_column 
        self.meanstats_data_order_column  = meanstats_data_order_column 
        self.stdevstats_data_order_column  = stdevstats_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["meanstats_data", self.meanstats_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["meanstats_data_partition_column", self.meanstats_data_partition_column, self.meanstats_data is None, (str,list)])
        self.__arg_info_matrix.append(["meanstats_data_order_column", self.meanstats_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["stdevstats_data", self.stdevstats_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["stdevstats_data_partition_column", self.stdevstats_data_partition_column, self.stdevstats_data is None, (str,list)])
        self.__arg_info_matrix.append(["stdevstats_data_order_column", self.stdevstats_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["value_columns", self.value_columns, False, (str,list)])
        self.__arg_info_matrix.append(["time_column", self.time_column, True, (str)])
        self.__arg_info_matrix.append(["window_type", self.window_type, True, (str)])
        self.__arg_info_matrix.append(["output", self.output, True, (str)])
        self.__arg_info_matrix.append(["mean", self.mean, True, (float,list)])
        self.__arg_info_matrix.append(["st_dev", self.st_dev, True, (float,list)])
        self.__arg_info_matrix.append(["window_size", self.window_size, True, (int)])
        self.__arg_info_matrix.append(["output_frequency", self.output_frequency, True, (int)])
        self.__arg_info_matrix.append(["points_persymbol", self.points_persymbol, True, (int)])
        self.__arg_info_matrix.append(["symbols_perwindow", self.symbols_perwindow, True, (int)])
        self.__arg_info_matrix.append(["alphabet_size", self.alphabet_size, True, (int)])
        self.__arg_info_matrix.append(["bitmap_level", self.bitmap_level, True, (int)])
        self.__arg_info_matrix.append(["print_stats", self.print_stats, True, (bool)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["meanstats_data_sequence_column", self.meanstats_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["stdevstats_data_sequence_column", self.stdevstats_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.meanstats_data, "meanstats_data", None)
        self.__awu._validate_input_table_datatype(self.stdevstats_data, "stdevstats_data", None)
        
        # Check for permitted values
        window_type_permitted_values = ["SLIDING", "GLOBAL"]
        self.__awu._validate_permitted_values(self.window_type, window_type_permitted_values, "window_type")
        
        output_permitted_values = ["STRING", "BITMAP", "BYTES", "CHARACTERS"]
        self.__awu._validate_permitted_values(self.output, output_permitted_values, "output")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.value_columns, "value_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.value_columns, "value_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_column, "time_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_column, "time_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.meanstats_data_sequence_column, "meanstats_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.meanstats_data_sequence_column, "meanstats_data_sequence_column", self.meanstats_data, "meanstats_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.stdevstats_data_sequence_column, "stdevstats_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stdevstats_data_sequence_column, "stdevstats_data_sequence_column", self.stdevstats_data, "stdevstats_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.meanstats_data_partition_column, "meanstats_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.meanstats_data_partition_column, "meanstats_data_partition_column", self.meanstats_data, "meanstats_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.stdevstats_data_partition_column, "stdevstats_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stdevstats_data_partition_column, "stdevstats_data_partition_column", self.stdevstats_data, "stdevstats_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.meanstats_data_order_column, "meanstats_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.meanstats_data_order_column, "meanstats_data_order_column", self.meanstats_data, "meanstats_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.stdevstats_data_order_column, "stdevstats_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stdevstats_data_order_column, "stdevstats_data_order_column", self.stdevstats_data, "stdevstats_data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.value_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.time_column is not None:
            self.__func_other_arg_sql_names.append("TimeColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.time_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.window_type is not None and self.window_type != "global":
            self.__func_other_arg_sql_names.append("WindowType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.output is not None and self.output != "string":
            self.__func_other_arg_sql_names.append("OutputType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.mean is not None:
            self.__func_other_arg_sql_names.append("Mean")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mean, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.st_dev is not None:
            self.__func_other_arg_sql_names.append("StDev")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.st_dev, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.window_size is not None:
            self.__func_other_arg_sql_names.append("WindowSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.output_frequency is not None and self.output_frequency != 1:
            self.__func_other_arg_sql_names.append("OutputFrequency")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_frequency, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.points_persymbol is not None and self.points_persymbol != 1:
            self.__func_other_arg_sql_names.append("PointsPerSymbol")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.points_persymbol, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.symbols_perwindow is not None:
            self.__func_other_arg_sql_names.append("SymbolsPerWindow")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.symbols_perwindow, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.alphabet_size is not None and self.alphabet_size != 4:
            self.__func_other_arg_sql_names.append("AlphabetSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.alphabet_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.bitmap_level is not None and self.bitmap_level != 2:
            self.__func_other_arg_sql_names.append("BitmapLevel")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.bitmap_level, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.print_stats is not None and self.print_stats != False:
            self.__func_other_arg_sql_names.append("OutputStats")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.print_stats, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.meanstats_data_sequence_column is not None:
            sequence_input_by_list.append("meanstats:" + UtilFuncs._teradata_collapse_arglist(self.meanstats_data_sequence_column, ""))
        
        if self.stdevstats_data_sequence_column is not None:
            sequence_input_by_list.append("stdevstats:" + UtilFuncs._teradata_collapse_arglist(self.stdevstats_data_sequence_column, ""))
        
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
        
        # Process meanstats_data
        if self.meanstats_data is not None:
            self.meanstats_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.meanstats_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.meanstats_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("meanstats")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.meanstats_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.meanstats_data_order_column, "\""))
        
        # Process stdevstats_data
        if self.stdevstats_data is not None:
            self.stdevstats_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.stdevstats_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.stdevstats_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("stdevstats")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.stdevstats_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.stdevstats_data_order_column, "\""))
        
        function_name = "SAX"
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
        Returns the string representation for a SAX class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
