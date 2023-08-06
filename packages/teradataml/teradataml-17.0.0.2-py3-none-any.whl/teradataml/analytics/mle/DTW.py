#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Adithya Avvaru (adithya.avvaru@teradata.com)
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

class DTW:
    
    def __init__(self,
        data = None,
        template_data = None,
        mapping_data = None,
        input_columns = None,
        template_columns = None,
        timeseries_id = None,
        template_id = None,
        radius = 10,
        dist_method = "EuclideanDistance",
        warp_path = False,
        data_sequence_column = None,
        template_data_sequence_column = None,
        mapping_data_sequence_column = None,
        data_partition_column = None,
        mapping_data_partition_column = None,
        data_order_column = None,
        template_data_order_column = None,
        mapping_data_order_column = None):
        """
        DESCRIPTION:
            The DTW function performs dynamic time warping (DTW), which
            measures the similarity (warp distance) between two time series
            that vary in time or speed. You can use DTW to analyze any data
            that can be represented linearly - for example, video, audio, and
            graphics.
            For example:
                • In two videos, DTW can detect similarities in walking
                  patterns, even if in one video the person is walking slowly
                  and in another, the same person is walking fast.
                • In audio, DTW can detect similarities in different speech
                  speeds (and is therefore very useful in speech recognition
                  applications).
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the time
                series information.
         
            data_partition_column:
                Required Argument.
                Specifies Partition By columns for "data".
                Values to this argument can be provided as list, if multiple
                columns are used for partition.
                Note: When teradataml is connected to Vantage 1.3 or later
                      versions, this argument accepts only one column which
                      is specified using the "timeseries_id" argument.
                Types: str OR list of Strings (str)
         
            data_order_column:
                Required Argument.
                Specifies Order By columns for "data".
                Values to this argument can be provided as list, if multiple
                columns are used for ordering.
                Note: When teradataml is connected to Vantage 1.3 or later
                      versions, this argument accepts only one column containing
                      timestamp values in the "data" teradataml DataFrame.
                Types: str OR list of Strings (str)
         
            template_data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the template
                information.
         
            template_data_order_column:
                Required Argument.
                Specifies Order By columns for "template_data".
                Values to this argument can be provided as list, if multiple
                columns are used for ordering.
                Note: When teradataml is connected to Vantage 1.3 or later
                      versions, this argument must include the column specified
                      using the "template_id" argument following the name of the
                      column containing timestamp values in "template_data".
                Types: str OR list of Strings (str)
         
            mapping_data:
                Optional Argument. Required if teradataml is connected to Vantage 1.1.1
                or earlier versions.
                Specifies the teradataml DataFrame that contains the mapping
                between the rows in "data" teradataml DataFrame and the rows in
                the "template_data" teradataml DataFrame.
         
            mapping_data_partition_column:
                Optional Argument. Required when "mapping_data" is used.
                Specifies Partition By columns for "mapping_data".
                Values to this argument can be provided as list, if multiple
                columns are used for partition.
                Note: When teradataml is connected to Vantage 1.3 or later
                      versions, this argument accepts only one column containing
                      a unique ID for a time series in "mapping_data".
                Types: str OR list of Strings (str)
         
            mapping_data_order_column:
                Optional Argument.
                Specifies Order By columns for "mapping_data".
                Values to this argument can be provided as list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            input_columns:
                Required Argument.
                Specifies the names of the "data" columns that contain the
                values and timestamps of the time series , in that order.
                Note: If these columns contain NaN or infinity values, then
                      those should be removed.
                Types: list of Strings (str)
         
            template_columns:
                Required Argument.
                Specifies the names of the "template_data" columns that contain
                the values and timestamps of the time series, in that order.
                Note: If these columns contain NaN or infinity values, then
                      those should be removed.
                Types: list of Strings (str)
         
            timeseries_id:
                Required Argument.
                Specifies the name of the column by which the "data" is
                partitioned. This column must comprise the unique ID for a time
                series in "data".
                Types: str
         
            template_id:
                Required Argument.
                Specifies the name of the column by which the "template_data"
                is ordered. This column must comprise the unique ID for a time
                series in "template_data".
                Types: str
         
            radius:
                Optional Argument.
                Specifies the integer value that determines the projected warp
                path from a previous resolution.
                Default Value: 10
                Types: int
         
            dist_method:
                Optional Argument.
                Specifies the metric for computing the warping distance.
                Note: These values are case-sensitive.
                Default Value: "EuclideanDistance"
                Permitted Values: EuclideanDistance, BinaryDistance,
                                  ManhattanDistance
                Types: str
         
            warp_path:
                Optional Argument.
                Determines whether to output the warping path.
                Default Value: False
                Types: bool
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to
                ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)
         
            template_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "template_data". The argument is used
                to ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)
         
            mapping_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "mapping_data". The argument is used
                to ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of DTW.
            Output teradataml DataFrames can be accessed using attribute
            references, such as DTWObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # This example compares a time series to a common template and
            # vice-versa. Time series represents stock prices (in table
            # 'timeseriesdata') and the template represents a series of stock
            # index prices (in table 'templatedata'). The mapping of
            # 'timeseriesdata' and 'templatedata' is given in table
            # 'mappingdata'.
         
            # Load example data.
            load_example_data("dtw", ["timeseriesdata", "templatedata", "mappingdata"])
         
            # Create teradataml DataFrame objects.
            timeseriesdata = DataFrame.from_table("timeseriesdata")
            templatedata = DataFrame.from_table("templatedata")
            mappingdata = DataFrame.from_table("mappingdata")
         
            # Example 1 : DTW compares "stockprice" in 'timeseriesdata'
            #             DataFrame with "indexprice" of 'templatedata'
            #             DataFrame using mapping information and generates
            #             the result DataFrame containing mapping information
            #             along with "wrap_distance" which indicates the
            #             similarity between the two columns' timeseries
            #             information.
         
            DTW_out = DTW(data = timeseriesdata,
                          data_partition_column = ["timeseriesid"],
                          data_order_column = ["timestamp1"],
                          template_data = templatedata,
                          template_data_order_column = ["timestamp2", "templateid"],
                          mapping_data = mappingdata,
                          mapping_data_partition_column = ["timeseriesid"],
                          input_columns = ["stockprice", "timestamp1"],
                          template_columns = ["indexprice", "timestamp2"],
                          timeseries_id = "timeseriesid",
                          template_id = "templateid"
                          )
            # Print the results
            print(DTW_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.template_data  = template_data 
        self.mapping_data  = mapping_data 
        self.input_columns  = input_columns 
        self.template_columns  = template_columns 
        self.timeseries_id  = timeseries_id 
        self.template_id  = template_id 
        self.radius  = radius 
        self.dist_method  = dist_method 
        self.warp_path  = warp_path 
        self.data_sequence_column  = data_sequence_column 
        self.template_data_sequence_column  = template_data_sequence_column 
        self.mapping_data_sequence_column  = mapping_data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.mapping_data_partition_column  = mapping_data_partition_column 
        self.data_order_column  = data_order_column 
        self.template_data_order_column  = template_data_order_column 
        self.mapping_data_order_column  = mapping_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["template_data", self.template_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["template_data_order_column", self.template_data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["mapping_data", self.mapping_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["mapping_data_partition_column", self.mapping_data_partition_column, self.mapping_data is None, (str,list)])
        self.__arg_info_matrix.append(["mapping_data_order_column", self.mapping_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, False, (str, list)])
        self.__arg_info_matrix.append(["template_columns", self.template_columns, False, (str, list)])
        self.__arg_info_matrix.append(["timeseries_id", self.timeseries_id, False, (str)])
        self.__arg_info_matrix.append(["template_id", self.template_id, False, (str)])
        self.__arg_info_matrix.append(["radius", self.radius, True, (int)])
        self.__arg_info_matrix.append(["dist_method", self.dist_method, True, (str)])
        self.__arg_info_matrix.append(["warp_path", self.warp_path, True, (bool)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["template_data_sequence_column", self.template_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["mapping_data_sequence_column", self.mapping_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.template_data, "template_data", None)
        self.__awu._validate_input_table_datatype(self.mapping_data, "mapping_data", None)
        
        # Check for permitted values
        dist_method_permitted_values = ["EUCLIDEANDISTANCE", "BINARYDISTANCE", "MANHATTANDISTANCE"]
        self.__awu._validate_permitted_values(self.dist_method, dist_method_permitted_values, "dist_method")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.template_columns, "template_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.template_columns, "template_columns", self.template_data, "template_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.timeseries_id, "timeseries_id")
        self.__awu._validate_dataframe_has_argument_columns(self.timeseries_id, "timeseries_id", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.template_id, "template_id")
        self.__awu._validate_dataframe_has_argument_columns(self.template_id, "template_id", self.template_data, "template_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.template_data_sequence_column, "template_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.template_data_sequence_column, "template_data_sequence_column", self.template_data, "template_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.mapping_data_sequence_column, "mapping_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.mapping_data_sequence_column, "mapping_data_sequence_column", self.mapping_data, "mapping_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.mapping_data_partition_column, "mapping_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.mapping_data_partition_column, "mapping_data_partition_column", self.mapping_data, "mapping_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.template_data_order_column, "template_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.template_data_order_column, "template_data_order_column", self.template_data, "template_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.mapping_data_order_column, "mapping_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.mapping_data_order_column, "mapping_data_order_column", self.mapping_data, "mapping_data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("TemplateColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.template_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TimeseriesId")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.timeseries_id, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TemplateId")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.template_id, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.radius is not None and self.radius != 10:
            self.__func_other_arg_sql_names.append("Radius")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.radius, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.dist_method is not None and self.dist_method != "EuclideanDistance":
            self.__func_other_arg_sql_names.append("DistanceMethod")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.dist_method, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.warp_path is not None and self.warp_path != False:
            self.__func_other_arg_sql_names.append("WarpPath")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.warp_path, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("inputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.template_data_sequence_column is not None:
            sequence_input_by_list.append("templateTable:" + UtilFuncs._teradata_collapse_arglist(self.template_data_sequence_column, ""))
        
        if self.mapping_data_sequence_column is not None:
            sequence_input_by_list.append("mappingTable:" + UtilFuncs._teradata_collapse_arglist(self.mapping_data_sequence_column, ""))
        
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
        self.__func_input_arg_sql_names.append("inputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process template_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.template_data, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("templateTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.template_data_order_column, "\""))
        
        # Process mapping_data
        if self.mapping_data is not None:
            self.mapping_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.mapping_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.mapping_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("mappingTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.mapping_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.mapping_data_order_column, "\""))
        
        function_name = "DTW"
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
        Returns the string representation for a DTW class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
