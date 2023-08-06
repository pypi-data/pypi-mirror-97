#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.2
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

class Interpolator:
    
    def __init__(self,
        data = None,
        time_data = None,
        count_rownumber = None,
        time_column = None,
        value_columns = None,
        time_interval = None,
        interpolation_type = None,
        aggregation_type = None,
        time_datatype = None,
        value_datatype = None,
        start_time = None,
        end_time = None,
        values_before_first = None,
        values_after_last = None,
        duplicate_rows_count = None,
        accumulate = None,
        data_sequence_column = None,
        time_data_sequence_column = None,
        count_rownumber_sequence_column = None,
        data_partition_column = None,
        count_rownumber_partition_column = None,
        data_order_column = None,
        time_data_order_column = None,
        count_rownumber_order_column = None):
        """
        DESCRIPTION:
            The Interpolator function calculates missing values in a time series, 
            using either interpolation or aggregation. Interpolation estimates 
            missing values between known values. Aggregation combines known 
            values to produce an aggregate value.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the input data.
            
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
            
            time_data:
                Optional Argument.
                Specifies the teradataml DataFrame name which contains time.
                If you specify time_data then the function calculates an interpolated
                value for each time point.
                Note:
                    If you omit time_data, you must specify the time_interval
                    argument.
            
            time_data_order_column:
                Optional Argument.
                Specifies Order By columns for time_data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            count_rownumber:
                Optional Argument.
                Specifies the teradataml DataFrame name which contains proportion
                of time points.
                Note:
                    It is only used with interpolation_type.
                    ("loess"(weights ({constant | tricube}), degree ({0 | 1 | 2}), span(m))),
                    where m is between (x+1)/n and 1.
            
            count_rownumber_partition_column:
                Optional Argument.
                Specifies Partition By columns for count_rownumber.
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Types: str OR list of Strings (str)
            
            count_rownumber_order_column:
                Optional Argument.
                Specifies Order By columns for count_rownumber.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            time_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame data column that
                contains the time points of the time series whose missing values are
                to be calculated.
                Types: str
            
            value_columns:
                Required Argument.
                Specifies the names of input teradataml DataFrame data columns to
                interpolate to the output teradataml DataFrame.
                Types: str OR list of Strings (str)
            
            time_interval:
                Optional Argument. Required when time_data is not provided.
                Specifies the length of time, in seconds, between calculated values.
                If you specify time_interval then the function calculates an
                interpolated value for a time point only if the value is missing
                in the original time series; otherwise, the function copies the original value.
                Note:
                    1. If you specify aggregation_type, the function ignores time_data or
                       time_interval and calculates the aggregated value for each point in the
                       time series.
                    2. Specify exactly one of time_data or time_interval.
                Types: int or float
            
            interpolation_type:
                Optional Argument.
                Specifies interpolation types for the columns that value_columns
                specifies. If you specify interpolation_type, then it must be the
                same size as value_columns. That is, if value_columns specifies n
                columns, then interpolation_type must specify n interpolation types.
                For i in [1, n], value_column_i has interpolation_type_i. However, 
                interpolation_type_i can be empty;
                for example:
                    value_columns (c1, c2, c3)
                    interpolation_type ("linear", ,"constant")
                An empty interpolation_type has the default value.
                The function calculates the value for each missing time point using a
                low-degree polynomial based on a set of nearest neighbors.
                The possible values of interpolation_type are as follows.
                    * "linear" (default): The value for each missing time point is
                      determined using linear interpolation between the two nearest points.
                    * "constant": The value for each missing time point is set
                      to the nearest value.
                      You must use this option if value_column has SQL data type CHARACTER,
                      CHARACTER(n), or VARCHAR.
                    * "spline[(type(cubic))]": The value for each missing time point is
                      determined by fitting a cubic spline to the nearest three points.
                    * "median[(window(n))]": The value for each missing time point is set
                      to the median value of the nearest n time points.
                      n must be greater than or equal to 2.
                      The default value of n is 5.
                    * "loess[(weights({constant | tricube}), degree ({0 |1 |2}),
                      span(m))]":
                        * weights:
                            * constant: All time points are equally weighted.
                            * ricube: Time points closer to missing data point are more heavily
                              weighted than those farther away.
                          The default value is constant.
                        * degree: Degree of polynomial.
                          The default value is 1.
                        * m: Two choices:
                            * It is either an integer greater than 1 (which specifies the number of
                              neighboring points)
                            * Specifies proportion of time points to use in each fit.
                              You must provide count_rownumber, and m must be between (x+1)/n and 1,
                              where x is specified degree and n is number of rows in partition).
                          The default value of m is 5.
                Note:
                    1. Specify only one of interpolation_type or aggregation_type.
                    2. If you omit both syntax elements, the function uses interpolation_type
                       with its default value, 'linear'.
                    3. For SQL data types CHARACTER, CHARACTER(n), and VARCHAR, you cannot use
                       aggregation_type. You must use interpolation_type, and interpolation_type
                       must be 'constant'.
                    4. In interpolation_type syntax, brackets do not indicate optional
                       elements - you must include them.
                Types: str OR list of strs
            
            aggregation_type:
                Optional Argument.
                Specifies the aggregation types of the columns that value_columns
                specifies. If you specify aggregation_type, then it must be the same
                size as value_columns. That is, if value_columns specifies n columns,
                then aggregation_type must specify n aggregation types. For i in [1,
                n], value_column_i has aggregation_type_i. However, aggregation_type_i
                can be empty.
                for example:
                    value_columns (c1, c2, c3)
                    aggregation_type (min, ,max)
                An empty aggregation_type has the default value.
                The syntax of aggregation_type is:
                    { min | max | mean | mode | sum } [(window(n))]
                The function calculates the aggregate value as the minimum, maximum,
                mean, mode, or sum within a sliding window of length n. n must be 
                greater than or equal to 2.
                The default value of n is 5.
                The default aggregation method is min.
                The Interpolator function can calculate the aggregates of values of
                these SQL data types:
                    * int
                    * BIGINT
                    * SMALLINT
                    * float
                    * DECIMAL(n,n)
                    * DECIMAL
                    * NUMERIC
                    * NUMERIC(n,n)
                Note:
                    1. Specify only one of aggregation_type or interpolation_type.
                    2. If you omit both syntax elements, the function uses interpolation_type
                       with its default value, 'linear'.
                    3. Aggregation calculations ignore the values in time_interval or in the
                       time_data. The function calculates the aggregated value for each value
                       in the time series.
                    4. In aggregation_type syntax, brackets do not indicate optional
                       elements - you must include them.
                Types: str OR list of strs
            
            time_datatype:
                Optional Argument.
                Specifies the data type of the output column that corresponds to the 
                input teradataml DataFrame data column that time_column specifies
                (time_column).
                If you omit this argument, then the function infers the data type of
                time_column from the input teradataml DataFrame data and uses the inferred
                data type for the corresponding output teradataml DataFrame column.
                If you specify this argument, then the function can transform the input
                data to the specified output data type only if both the input column
                data type and the specified output column data type are in this list:
                    * int
                    * BIGINT
                    * SMALLINT
                    * float
                    * DECIMAL(n,n)
                    * DECIMAL
                    * NUMERIC
                    * NUMERIC(n,n)
                Types: str
            
            value_datatype:
                Optional Argument.
                Specifies the data types of the output columns that correspond to
                the input teradataml DataFrame data columns that value_columns specifies.
                If you omit this argument, then the function infers the data type of 
                each time_column from the input teradataml DataFrame data and uses the
                inferred data type for the corresponding output teradataml DataFrame 
                column.
                If you specify value_datatype, then it must be the same size as
                value_columns. That is, if value_columns specifies n columns, then
                value_datatype must specify n data types. For i in [1, n], value_column_i
                has value_type_i. However, value_type_i can be empty;
                for example:
                    value_columns (c1, c2, c3)
                    value_datatype (int, ,VARCHAR)
                If you specify this argument, then the function can transform the
                input data to the specified output data type only if both the input
                column data type and the specified output column data type are
                in this list:
                    * int
                    * BIGINT
                    * SMALLINT
                    * float
                    * DECIMAL(n,n)
                    * DECIMAL
                    * NUMERIC
                    * NUMERIC(n,n)
                Types: str OR list of strs
            
            start_time:
                Optional Argument.
                Specifies the start time for the time series.
                The default value is the start time of the time series in input
                teradataml DataFrame.
                Types: str
            
            end_time:
                Optional Argument.
                Specifies the end time for the time series.
                The default value is the end time of the time series in input
                teradataml DataFrame.
                Types: str
            
            values_before_first:
                Optional Argument.
                Specifies the values to use if start_time is before the start time of 
                the time series in input teradataml DataFrame. Each of these values
                must have the same data type as its corresponding value_column. Values
                of data type VARCHAR are case-insensitive.
                If value_columns specifies n columns, then values_before_first must
                specify n values. For in [1, n], value_column_i has the value
                before_first_value_i. However, before_first_value_i can be empty;
                for example:
                    value_columns (c1, c2, c3)
                    values_before_first (1, ,"abc")
                If before_first_value_i is empty, then value_column_i has the value NULL.
                If you do not specify values_before_first, then value_column_i has the
                value NULL for i in [1, n].
                Types: str OR list of strs
            
            values_after_last:
                Optional Argument.
                Specifies the values to use if end_time is after the end time of the 
                time series in input teradataml DataFrame. Each of these values must
                have the same data type as its corresponding value_column. Values of
                data type VARCHAR are case-insensitive.
                If value_columns specifies n columns, then values_after_last must
                specify n values. For i in [1, n], value_column_i has the value
                after_last_value_i. However, after_last_value_i can be empty;
                for example:
                    value_columns (c1, c2, c3)
                    values_after_last (1, ,"abc")
                If after_last_value_i is empty, then value_column_i has the value NULL.
                If you do not specify values_after_last, then value_column_i has the
                value NULL for i in [1, n].
                Types: str OR list of strs
            
            duplicate_rows_count:
                Optional Argument.
                Specifies the number of rows to duplicate across split boundaries if 
                you use the SeriesSplitter function.
                If you specify only value1, then the function duplicates value1 rows
                from the previous partition and value1 rows from the next partition.
                If you specify both value1 and value2, then the function duplicates value1
                rows from the previous partition and value2 rows from the next partition.
                Each argument value must be non-negative int. Both value1 and value2 must
                exceed the number of time points that the function needs for every
                specified interpolation or aggregation method. For aggregation, the
                number of time points required is determined by the value of n in window(n)
                specified by aggregation_type.
                The interpolation methods and the number of time points that the function
                needs for them are:
                    * "linear": 1
                    * "constant": 1
                    * "spline": 2
                    * "median [(window(n))]": n/2
                    * "loess [(weights ({constant | tricube}), degree ({0 | 1 | 2}), span(m))]":
                        * m > 1: m-1
                        * m < 1: (m * n)-1
                      where n is total number of data rows, found in column n of the
                      count_rownumber DataFrame.
                Types: int OR list of ints
            
            accumulate:
                Optional Argument.
                Specifies the names of input teradataml DataFrame columns (other than those
                specified by time_column and value_columns) to copy to the output table.
                By default, the function copies to the output teradataml DataFrame only
                the columns specified by time_column and value_columns.
                Types: str OR list of Strings (str)
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
            
            time_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "time_data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
            
            count_rownumber_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "count_rownumber". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Interpolator.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as InterpolatorObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("Interpolator", ["ibm_stock1", "time_table1"])
         
            # Create teradataml DataFrame.
            ibm_stock1 = DataFrame.from_table("ibm_stock1")
            time_table1 = DataFrame.from_table("time_table1")
         
            # Example 1 : Running Interpolator function with aggregation_type min.
            interpolator_out1 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                  time_data=time_table1,
                                  time_data_order_column='period',
                                  time_column='period',
                                  value_columns='stockprice',
                                  accumulate='id',
                                  aggregation_type='min[(window(2))]',
                                  values_before_first='0',
                                  values_after_last='0',
                                  data_sequence_column='period'
                                  )
         
            # Print the result DataFrame.
            print(interpolator_out1.result)
         
            # Example 2 : Running Interpolator function with constant interpolation.
            interpolator_out2 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                  time_column='period',
                                  value_columns='stockprice',
                                  accumulate='id',
                                  time_interval=86400.0,
                                  interpolation_type='constant',
                                  values_before_first='0',
                                  values_after_last='0'
                                  )
         
            # Print the result DataFrame.
            print(interpolator_out2.result)
         
            # Example 3 : Running Interpolator function with linear interpolation.
            interpolator_out3 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                   time_column='period',
                                   value_columns='stockprice',
                                   accumulate='id',
                                   time_interval=86400.0,
                                   interpolation_type='linear',
                                   values_before_first='0',
                                   values_after_last='0'
                                   )
         
            # Print the result DataFrame.
            print(interpolator_out3.result)
         
            # Example 4 : Running Interpolator function with median interpolation.
            interpolator_out4 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                  time_column='period',
                                  value_columns='stockprice',
                                  accumulate='id',
                                  time_interval=86400.0,
                                  interpolation_type='median[(window(4))]',
                                  values_before_first='0',
                                  values_after_last='0'
                                  )
         
            # Print the result DataFrame.
            print(interpolator_out4.result)
         
            # Example 5 : Running Interpolator function with spline interpolation.
            interpolator_out5 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                  time_column='period',
                                  value_columns='stockprice',
                                  accumulate='id',
                                  time_interval=86400.0,
                                  interpolation_type='spline[(type(cubic))]',
                                  values_before_first='0',
                                  values_after_last='0'
                                  )
         
            # Print the result DataFrame.
            print(interpolator_out5.result)
         
            # Example 6 : Running Interpolator function with loess interpolation.
            interpolator_out6 = Interpolator(data=ibm_stock1,
                                  data_partition_column='id',
                                  data_order_column='period',
                                  time_column='period',
                                  value_columns='stockprice',
                                  accumulate='id',
                                  time_interval=86400.0,
                                  interpolation_type='loess[(weights(constant),degree(2),span(4))]',
                                  values_before_first='0',
                                  values_after_last='0'
                                  )
         
            # Print the result DataFrame.
            print(interpolator_out6)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.time_data  = time_data 
        self.count_rownumber  = count_rownumber 
        self.time_column  = time_column 
        self.value_columns  = value_columns 
        self.time_interval  = time_interval 
        self.interpolation_type  = interpolation_type 
        self.aggregation_type  = aggregation_type 
        self.time_datatype  = time_datatype 
        self.value_datatype  = value_datatype 
        self.start_time  = start_time 
        self.end_time  = end_time 
        self.values_before_first  = values_before_first 
        self.values_after_last  = values_after_last 
        self.duplicate_rows_count  = duplicate_rows_count 
        self.accumulate  = accumulate 
        self.data_sequence_column  = data_sequence_column 
        self.time_data_sequence_column  = time_data_sequence_column 
        self.count_rownumber_sequence_column  = count_rownumber_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.count_rownumber_partition_column  = count_rownumber_partition_column 
        self.data_order_column  = data_order_column 
        self.time_data_order_column  = time_data_order_column 
        self.count_rownumber_order_column  = count_rownumber_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["time_data", self.time_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["time_data_order_column", self.time_data_order_column, self.time_data is None, (str,list)])
        self.__arg_info_matrix.append(["count_rownumber", self.count_rownumber, True, (DataFrame)])
        self.__arg_info_matrix.append(["count_rownumber_partition_column", self.count_rownumber_partition_column, self.count_rownumber is None, (str,list)])
        self.__arg_info_matrix.append(["count_rownumber_order_column", self.count_rownumber_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["time_column", self.time_column, False, (str)])
        self.__arg_info_matrix.append(["value_columns", self.value_columns, False, (str,list)])
        self.__arg_info_matrix.append(["time_interval", self.time_interval, True, (int,float)])
        self.__arg_info_matrix.append(["interpolation_type", self.interpolation_type, True, (str,list)])
        self.__arg_info_matrix.append(["aggregation_type", self.aggregation_type, True, (str,list)])
        self.__arg_info_matrix.append(["time_datatype", self.time_datatype, True, (str)])
        self.__arg_info_matrix.append(["value_datatype", self.value_datatype, True, (str,list)])
        self.__arg_info_matrix.append(["start_time", self.start_time, True, (str)])
        self.__arg_info_matrix.append(["end_time", self.end_time, True, (str)])
        self.__arg_info_matrix.append(["values_before_first", self.values_before_first, True, (str,list)])
        self.__arg_info_matrix.append(["values_after_last", self.values_after_last, True, (str,list)])
        self.__arg_info_matrix.append(["duplicate_rows_count", self.duplicate_rows_count, True, (int,list)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["time_data_sequence_column", self.time_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["count_rownumber_sequence_column", self.count_rownumber_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.count_rownumber, "count_rownumber", None)
        
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
        
        self.__awu._validate_input_columns_not_empty(self.count_rownumber_sequence_column, "count_rownumber_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_rownumber_sequence_column, "count_rownumber_sequence_column", self.count_rownumber, "count_rownumber", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.count_rownumber_partition_column, "count_rownumber_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_rownumber_partition_column, "count_rownumber_partition_column", self.count_rownumber, "count_rownumber", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.time_data_order_column, "time_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.time_data_order_column, "time_data_order_column", self.time_data, "time_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.count_rownumber_order_column, "count_rownumber_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_rownumber_order_column, "count_rownumber_order_column", self.count_rownumber, "count_rownumber", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("ValueColumns")
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
        
        if self.interpolation_type is not None:
            self.__func_other_arg_sql_names.append("InterpolationType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.interpolation_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.aggregation_type is not None:
            self.__func_other_arg_sql_names.append("AggregationType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.aggregation_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
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
        
        if self.values_before_first is not None:
            self.__func_other_arg_sql_names.append("ValuesBeforeFirst")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_before_first, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.values_after_last is not None:
            self.__func_other_arg_sql_names.append("ValuesAfterLast")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.values_after_last, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.duplicate_rows_count is not None:
            self.__func_other_arg_sql_names.append("DuplicateRowsCount")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.duplicate_rows_count, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input_table:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.time_data_sequence_column is not None:
            sequence_input_by_list.append("time_table:" + UtilFuncs._teradata_collapse_arglist(self.time_data_sequence_column, ""))
        
        if self.count_rownumber_sequence_column is not None:
            sequence_input_by_list.append("count_row_number:" + UtilFuncs._teradata_collapse_arglist(self.count_rownumber_sequence_column, ""))
        
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
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.time_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("time_table")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.time_data_order_column, "\""))
        
        # Process count_rownumber
        self.count_rownumber_partition_column = UtilFuncs._teradata_collapse_arglist(self.count_rownumber_partition_column, "\"")
        if self.count_rownumber is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.count_rownumber, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("count_row_number")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.count_rownumber_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.count_rownumber_order_column, "\""))
        
        function_name = "Interpolator"
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
        Returns the string representation for a Interpolator class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
