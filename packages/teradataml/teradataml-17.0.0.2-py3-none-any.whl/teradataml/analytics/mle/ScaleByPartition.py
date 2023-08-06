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
# Function Version: 1.7
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

class ScaleByPartition:
    
    def __init__(self,
        data = None,
        method = None,
        miss_value = "KEEP",
        input_columns = None,
        scale_global = False,
        accumulate = None,
        multiplier = 1.0,
        intercept = "0",
        data_sequence_column = None,
        data_partition_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The ScaleByPartition function scales the sequences in each partition
            independently, using the same formula as the function Scale.


        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame for ScaleByPartition function.

            data_partition_column:
                Required Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            method:
                Required Argument.
                Specifies one or more statistical methods to use to scale the data
                set. If you specify multiple methods, the output teradataml DataFrame includes
                the column scalemethod (which contains the method name) and a row for each
                input-row/method combination.
                Permitted Values: MEAN, SUM, USTD, STD, RANGE, MIDRANGE, MAXABS
                Types: str or list of Strings (str)

            miss_value:
                Optional Argument.
                Specifies how the ScaleByPartition function processes NULL
                values in input:
                    KEEP: Keep NULL values.
                    OMIT: Ignore any row that has a NULL value.
                    ZERO: Replace each NULL value with zero.
                    LOCATION: Replace each NULL value with its location value.
                Default Value: "KEEP"
                Permitted Values: KEEP, OMIT, ZERO, LOCATION
                Types: str

            input_columns:
                Required Argument.
                Specifies the input teradataml DataFrame columns that contain the
                attribute values of the samples to be scaled. The attribute values must be numeric
                values between -1e308 and 1e308. If a value is outside this range,
                the function treats it as infinity.
                Types: str OR list of Strings (str)

            scale_global:
                Optional Argument.
                Specifies whether all columns specified in input_columns are scaled to the same location
                and scale. (Each input column is scaled separately).
                Default Value: False
                Types: bool

            accumulate:
                Optional Argument.
                Specifies the input teradataml DataFrame columns to copy to the
                output teradataml DataFrame. By default, the function copies no input teradataml
                DataFrame columns to the output teradataml DataFrame.
                Tip: To identify the sequences in the output, specify the
                partition columns in this argument.
                Types: str OR list of Strings (str)

            multiplier:
                Optional Argument.
                Specifies one or more multiplying factors to apply to the input
                variables (multiplier in the following formula):
                    X" = intercept + multiplier * (X - location)/scale
                If you specify only one multiplier, it applies to all columns specified
                by the input_columns argument. If you specify multiple multiplying factor,
                each multiplier applies to the corresponding input column. For example,
                the first multiplier applies to the first column specified by the input_columns argument,
                the second multiplier applies to the second input column, and so on.
                Default Value: 1.0
                Types: float OR list of floats

            intercept:
                Optional Argument.
                Specifies one or more addition factors incrementing the scaled
                results-intercept in the following formula:
                    X' = intercept + multiplier * (X - location)/scale
                If you specify only one intercept, it applies to all columns specified
                by the input_columns argument. If you specify multiple addition factors,
                each intercept applies to the corresponding input column.
                The syntax of intercept is:
                    [-]{number | min | mean | max }
                where min, mean, and max are the global minimum,
                maximum, mean values in the corresponding columns.
                The function scales the values of min, mean, and max.
                The formula for computing the scaled global minimum is:
                    scaledmin = (minX - location)/scale
                The formulas for computing the scaled global mean and maximum
                are analogous to the preceding formula.
                For example, if intercept is "- min" and multiplier is 1,
                the scaled result is transformed to a nonnegative sequence according
                to this formula, where scaledmin is the scaled value:
                    X' = -scaledmin + 1 * (X - location)/scale.
                Default Value: "0"
                Types: str or list of Strings (str)

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of ScaleByPartition.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ScaleByPartitionObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            # The table 'scale_housing' contains house properties
            # like the number of bedrooms, lot size, the number of bathrooms, number of stories etc.
            load_example_data("scalebypartition", "scale_housing")

            # Create teradataml DataFrame objects.
            scale_housing = DataFrame.from_table("scale_housing")

            # Example 1 - This function scales the sequences on partition cloumn 'lotsize, using
            # the same formula as the function.
            scale_by_partition_out = ScaleByPartition(data=scale_housing,
                                               data_partition_column ="lotsize",
                                               input_columns = ["id","price", "lotsize", "bedrooms", "bathrms"],
                                               method = "maxabs",
                                               accumulate = "types"
                                              )
            # Print the result DataFrame
            print(scale_by_partition_out)

        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.method  = method 
        self.miss_value  = miss_value 
        self.input_columns  = input_columns 
        self.scale_global  = scale_global
        self.accumulate  = accumulate 
        self.multiplier  = multiplier 
        self.intercept  = intercept 
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
        self.__arg_info_matrix.append(["method", self.method, False, (str,list)])
        self.__arg_info_matrix.append(["miss_value", self.miss_value, True, (str)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, False, (str,list)])
        self.__arg_info_matrix.append(["scale_global", self.scale_global, True, (bool)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["multiplier", self.multiplier, True, (float,list)])
        self.__arg_info_matrix.append(["intercept", self.intercept, True, (str,list)])
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
        
        # Check for permitted values
        method_permitted_values = ["MEAN", "SUM", "USTD", "STD", "RANGE", "MIDRANGE", "MAXABS"]
        self.__awu._validate_permitted_values(self.method, method_permitted_values, "method")
        
        miss_value_permitted_values = ["KEEP", "OMIT", "ZERO", "LOCATION"]
        self.__awu._validate_permitted_values(self.miss_value, miss_value_permitted_values, "miss_value")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
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
        
        self.__func_other_arg_sql_names.append("TargetColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.input_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ScaleMethod")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.method, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.miss_value is not None and self.miss_value != "KEEP":
            self.__func_other_arg_sql_names.append("MissValue")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.miss_value, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.scale_global is not None and self.scale_global != False:
            self.__func_other_arg_sql_names.append("GlobalScale")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.scale_global, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.multiplier is not None and self.multiplier != 1.0:
            self.__func_other_arg_sql_names.append("Multiplier")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.multiplier, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.intercept is not None and self.intercept != "0":
            self.__func_other_arg_sql_names.append("Intercept")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.intercept, "'"))
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
        self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "ScaleByPartition"
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
        Returns the string representation for a ScaleByPartition class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
