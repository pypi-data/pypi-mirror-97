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
# Function Version: 1.14
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

class VarMax:
    
    def __init__(self,
        data = None,
        response_columns = None,
        exogenous_columns = None,
        partition_columns = None,
        orders = None,
        seasonal_orders = None,
        period = None,
        exogenous_order = None,
        lag = 0,
        include_mean = False,
        max_iter_num = 100,
        step_ahead = None,
        method = "SSE",
        data_orders = None,
        include_drift = False,
        order_p = None,
        order_d = None,
        order_q = None,
        seasonal_order_p = None,
        seasonal_order_d = None,
        seasonal_order_q = None,
        data_sequence_column = None,
        data_orders_sequence_column = None,
        data_partition_column = "1",
        data_orders_partition_column = "1",
        data_order_column = None,
        data_orders_order_column = None):
        """
        DESCRIPTION:
            VarMax (Vector Autoregressive Moving Average model with eXogenous
            variables) extends the ARMA/ARIMA model in two ways.
         
         
        PARAMETERS:
            data:
                Required Argument.
                The teradataml DataFrame that stores the input sequence.
         
            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Default Value: 1
                Types: str OR list of Strings (str)
         
            data_order_column:
                Required Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            response_columns:
                Required Argument.
                Specifies the columns containing the response data. Null values are
                acceptable at the end of the series. If step_ahead is specified, the
                function will report predicted values for the missing values, taking
                into account values from the predictor columns for those time periods.
                Types: str OR list of Strings (str)
         
            exogenous_columns:
                Optional Argument.
                Specifies the columns containing the independent (exogenous)
                predictors. If not specified, the model will be calculated without
                exogenous vectors.
                Types: str OR list of Strings (str)
         
            partition_columns:
                Optional Argument.
                Specifies the partition columns that will be passed to the output. If
                not specified, the output will not contain partition columns.
                Types: str OR list of Strings (str)
         
            orders:
                Optional Argument.
                Specifies the parameters p, d, q for VarMax model. This argument
                consists of 3 non-negative int values separated by commas. The p and q
                must be an integer between 0 and 10, inclusive. The d must be between
                0 and 1, inclusive.
                Types: str
         
            seasonal_orders:
                Optional Argument.
                Specifies seasonal parameters sp, sd, sq for VarMax model. This argument
                consists of 3 non-negative integer values separated by commas. The sp
                and sq must be an integer between 0 and 10, inclusive. The sd must be
                between 0 and 3, inclusive. If not specified, the model will be
                treated as a non-seasonal model. If the seasonal_orders argument is
                used, the period argument should also be present.
                Types: str
         
            period:
                Optional Argument.
                Specifies the period of each season. Must be a positive integer
                value. If the period argument is used, the seasonal_orders argument
                must also be present. If not specified, the model will be treated as
                a non-seasonal model.
                Types: int
         
            exogenous_order:
                Optional Argument.
                Specifies the order of exogenous variables. If the current time is t
                and exogenous_order isb, the following values of the exogenous time
                series will be used in calculating the response: Xt Xt-1 ... Xt-b+1.
                If not specified, the model will be calculated without exogenous
                vectors.
                Types: int
         
            lag:
                Optional Argument.
                Specifies the lag in the effect of the exogenous variables on the
                response variables. For example, if lag = 3, and exogenous_order is
                b, Yi will be predicted based on Xi-3 to Xi-b-2.
                Default Value: 0
                Types: int
         
            include_mean:
                Optional Argument.
                Specifies whether mean vector of the response data series (constant c
                in the formula) is added in the VarMax model.
                Note: If this argument is True, the difference parameters d (in the orders
                      argument) and sd (in the seasonal_orders argument) should be 0.
                Default Value: False
                Types: bool
         
            max_iter_num:
                Optional Argument.
                A positive integer value. The maximum number of iterations performed.
                Default Value: 100
                Types: int
         
            step_ahead:
                Optional Argument.
                A positive integer value. The number of steps to forecast after the
                end of the time series. If not provided, no forecast values are
                calculated.
                Types: int
         
            method:
                Optional Argument.
                Specifies the method for fitting the model parameters: SSE (Default):
                Sum of squared error. ML: Maximum likelihood
                Default Value: "SSE"
                Permitted Values: SSE, ML
                Types: str
         
            data_orders:
                Optional Argument.
                It is the output teradataml DataFrame from TimeSeriesParameters.
         
            data_orders_partition_column:
                Optional Argument.
                Specifies Partition By columns for data_orders.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Default Value: 1
                Types: str OR list of Strings (str)
         
            data_orders_order_column:
                Optional Argument.
                Specifies Order By columns for data_orders.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            include_drift:
                Optional Argument.
                Specifies whether drift term is included in the VarMax model.
                Note: This argument can only be True when d is non-zero and less than 2.
                Default Value: False
                Types: bool
         
            order_p:
                Optional Argument.
                The p value of the non-seasonal order parameter. The p value must be
                an integer between 0 and 10, inclusive.
                Note: "order_p" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            order_d:
                Optional Argument.
                The d value of the non-seasonal order parameter. The d value must be
                an integer between 0 and 1, inclusive.
                Note: "order_d" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            order_q:
                Optional Argument.
                The q value of the non-seasonal order parameter. The q value must be
                an integer between 0 and 10, inclusive.
                Note: "order_q" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            seasonal_order_p:
                Optional Argument.
                The sp value of the seasonal order parameter. The sp value must be an
                integer between 0 and 10, inclusive.
                Note: "seasonal_order_p" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            seasonal_order_d:
                Optional Argument.
                The sd value of the seasonal order parameter. The sd value must be an
                integer between 0 and 3, inclusive.
                Note: "seasonal_order_d" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            seasonal_order_q:
                Optional Argument.
                The sq value of the seasonal order parameter. The sq value must be an
                integer between 0 and 10, inclusive.
                Note: "seasonal_order_q" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Types: int
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            data_orders_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data_orders". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of VarMax.
            Output teradataml DataFrames can be accessed using attribute
            references, such as VarMaxObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("VarMax",["finance_data3","orders_ex"])
         
            # Create teradataml DataFrame objects.
            finance_data3 = DataFrame.from_table("finance_data3")
            orders_ex = DataFrame.from_table("orders_ex")
         
            # Example 1 -
            varmax_out1 = VarMax(data = finance_data3,
                                 data_partition_column = ["id"],
                                 data_order_column = ["period"],
                                 response_columns = ["expenditure","income","investment"],
                                 partition_columns = ["id"],
                                 orders = "1,1,1",
                                 include_mean = False,
                                 step_ahead = 3
                                 )
            # Print the results.
            print(varmax_out1.result)
         
            # Example 2 -
            varmax_out2 = VarMax(data = finance_data3,
                                 data_partition_column = ["id"],
                                 data_order_column = ["period"],
                                 response_columns = ["expenditure"],
                                 exogenous_columns = ["income","investment"],
                                 partition_columns = ["id"],
                                 orders = "1,1,1",
                                 exogenous_order = 3,
                                 lag = 3,
                                 include_mean = False,
                                 step_ahead = 3
                                 )
            # Print the results.
            print(varmax_out2.result)
         
            # Example 3 -
            varmax_out3 = VarMax(data = finance_data3,
                                 data_partition_column = ["id"],
                                 data_order_column = ["period"],
                                 response_columns = ["expenditure"],
                                 exogenous_columns = ["income","investment"],
                                 partition_columns = ["id"],
                                 orders = "1,1,1",
                                 seasonal_orders = "1,0,0",
                                 period = 4,
                                 exogenous_order = 3,
                                 lag = 3,
                                 include_mean = False,
                                 step_ahead = 3
                                 )
            # Print the results.
            print(varmax_out3.result)
         
            # Example 4 -
            varmax_out4 = VarMax(data = finance_data3,
                                 data_partition_column = ["id"],
                                 data_order_column = ["period"],
                                 response_columns = ["expenditure"],
                                 partition_columns = ["id"],
                                 max_iter_num = 1000,
                                 method = "ML",
                                 data_orders = orders_ex,
                                 data_orders_partition_column = ["id"]
                                 )
            # Print the results.
            print(varmax_out4.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data
        self.response_columns  = response_columns 
        self.exogenous_columns  = exogenous_columns 
        self.partition_columns  = partition_columns 
        self.orders  = orders 
        self.seasonal_orders  = seasonal_orders 
        self.period  = period 
        self.exogenous_order  = exogenous_order 
        self.lag  = lag 
        self.include_mean  = include_mean 
        self.max_iter_num  = max_iter_num 
        self.step_ahead  = step_ahead 
        self.method  = method 
        self.data_orders  = data_orders 
        self.include_drift  = include_drift 
        self.order_p  = order_p 
        self.order_d  = order_d 
        self.order_q  = order_q 
        self.seasonal_order_p  = seasonal_order_p 
        self.seasonal_order_d  = seasonal_order_d 
        self.seasonal_order_q  = seasonal_order_q 
        self.data_sequence_column  = data_sequence_column 
        self.data_orders_sequence_column  = data_orders_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_orders_partition_column  = data_orders_partition_column 
        self.data_order_column  = data_order_column 
        self.data_orders_order_column  = data_orders_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["response_columns", self.response_columns, False, (str,list)])
        self.__arg_info_matrix.append(["exogenous_columns", self.exogenous_columns, True, (str,list)])
        self.__arg_info_matrix.append(["partition_columns", self.partition_columns, True, (str,list)])
        self.__arg_info_matrix.append(["orders", self.orders, True, (str)])
        self.__arg_info_matrix.append(["seasonal_orders", self.seasonal_orders, True, (str)])
        self.__arg_info_matrix.append(["period", self.period, True, (int)])
        self.__arg_info_matrix.append(["exogenous_order", self.exogenous_order, True, (int)])
        self.__arg_info_matrix.append(["lag", self.lag, True, (int)])
        self.__arg_info_matrix.append(["include_mean", self.include_mean, True, (bool)])
        self.__arg_info_matrix.append(["max_iter_num", self.max_iter_num, True, (int)])
        self.__arg_info_matrix.append(["step_ahead", self.step_ahead, True, (int)])
        self.__arg_info_matrix.append(["method", self.method, True, (str)])
        self.__arg_info_matrix.append(["data_orders", self.data_orders, True, (DataFrame)])
        self.__arg_info_matrix.append(["data_orders_partition_column", self.data_orders_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_orders_order_column", self.data_orders_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["include_drift", self.include_drift, True, (bool)])
        self.__arg_info_matrix.append(["order_p", self.order_p, True, (int)])
        self.__arg_info_matrix.append(["order_d", self.order_d, True, (int)])
        self.__arg_info_matrix.append(["order_q", self.order_q, True, (int)])
        self.__arg_info_matrix.append(["seasonal_order_p", self.seasonal_order_p, True, (int)])
        self.__arg_info_matrix.append(["seasonal_order_d", self.seasonal_order_d, True, (int)])
        self.__arg_info_matrix.append(["seasonal_order_q", self.seasonal_order_q, True, (int)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_orders_sequence_column", self.data_orders_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.data_orders, "data_orders", None)
        
        # Check for permitted values
        method_permitted_values = ["SSE", "ML"]
        self.__awu._validate_permitted_values(self.method, method_permitted_values, "method")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.response_columns, "response_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.response_columns, "response_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.exogenous_columns, "exogenous_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.exogenous_columns, "exogenous_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.partition_columns, "partition_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.partition_columns, "partition_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_orders_sequence_column, "data_orders_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_orders_sequence_column, "data_orders_sequence_column", self.data_orders, "data_orders", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        if self.__awu._is_default_or_not(self.data_partition_column, "1"):
            self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_orders_partition_column, "data_orders_partition_column")
        if self.__awu._is_default_or_not(self.data_orders_partition_column, "1"):
            self.__awu._validate_dataframe_has_argument_columns(self.data_orders_partition_column, "data_orders_partition_column", self.data_orders, "data_orders", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_orders_order_column, "data_orders_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_orders_order_column, "data_orders_order_column", self.data_orders, "data_orders", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("ResponseColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.response_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.exogenous_columns is not None:
            self.__func_other_arg_sql_names.append("ExogenousColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.exogenous_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.partition_columns is not None:
            self.__func_other_arg_sql_names.append("PartitionColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.partition_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.orders is not None:
            self.__func_other_arg_sql_names.append("PDQ")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.orders, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.method is not None and self.method != "SSE":
            self.__func_other_arg_sql_names.append("Method")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.method, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.seasonal_orders is not None:
            self.__func_other_arg_sql_names.append("SeasonalPDQ")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seasonal_orders, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.period is not None:
            self.__func_other_arg_sql_names.append("Period")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.period, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.exogenous_order is not None:
            self.__func_other_arg_sql_names.append("ExogenousOrder")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.exogenous_order, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.include_mean is not None and self.include_mean != False:
            self.__func_other_arg_sql_names.append("IncludeMean")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.include_mean, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.include_drift is not None and self.include_drift != False:
            self.__func_other_arg_sql_names.append("IncludeDrift")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.include_drift, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.lag is not None and self.lag != 0:
            self.__func_other_arg_sql_names.append("Lag")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.lag, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.max_iter_num is not None and self.max_iter_num != 100:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.step_ahead is not None:
            self.__func_other_arg_sql_names.append("StepAhead")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.step_ahead, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.order_p is not None:
            self.__func_other_arg_sql_names.append("OrderP")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.order_p, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.order_d is not None:
            self.__func_other_arg_sql_names.append("OrderD")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.order_d, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.order_q is not None:
            self.__func_other_arg_sql_names.append("OrderQ")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.order_q, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.seasonal_order_p is not None:
            self.__func_other_arg_sql_names.append("SeasonalOrderP")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seasonal_order_p, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.seasonal_order_d is not None:
            self.__func_other_arg_sql_names.append("SeasonalOrderD")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seasonal_order_d, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.seasonal_order_q is not None:
            self.__func_other_arg_sql_names.append("SeasonalOrderQ")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seasonal_order_q, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("data:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.data_orders_sequence_column is not None:
            sequence_input_by_list.append("orders:" + UtilFuncs._teradata_collapse_arglist(self.data_orders_sequence_column, ""))
        
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
        if self.__awu._is_default_or_not(self.data_partition_column, "1"):
            self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("data")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process data_orders
        if self.data_orders is not None:
            if self.__awu._is_default_or_not(self.data_orders_partition_column, "1"):
                self.data_orders_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_orders_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data_orders, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("orders")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.data_orders_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_orders_order_column, "\""))
        
        function_name = "VARMAX"
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
        Returns the string representation for a VarMax class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
