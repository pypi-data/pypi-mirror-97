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

class Attribution:
    
    def __init__(self,
        data = None,
        data_optional = None,
        conversion_data = None,
        excluding_data = None,
        optional_data = None,
        model1_type = None,
        model2_type = None,
        event_column = None,
        timestamp_column = None,
        window_size = None,
        data_partition_column = None,
        data_optional_partition_column = None,
        data_order_column = None,
        data_optional_order_column = None,
        conversion_data_order_column = None,
        excluding_data_order_column = None,
        optional_data_order_column = None,
        model1_type_order_column = None,
        model2_type_order_column = None):
        """
        DESCRIPTION:
            The Attribution function is used in web page analysis, where it lets 
            companies assign weights to pages before certain events, such as 
            buying a product.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the click stream data,
                which the function uses to compute attributions.
         
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
         
            data_optional:
                Optional Argument.
                Specifies the teradataml DataFrame that contains the click stream data,
                which the function uses to compute attributions.
         
            data_optional_partition_column:
                Optional Argument.
                Required if the data_optional teradataml DataFrame is used.
                Specifies Partition By columns for data_optional.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)
         
            data_optional_order_column:
                Optional Argument.
                Required if the data_optional teradataml DataFrame is used.
                Specifies Order By columns for data_optional.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            conversion_data:
                Required Argument.
                Specifies the teradataml DataFrame that contains one varchar column
                (conversion_events) containing conversion event values.
         
            conversion_data_order_column:
                Optional Argument.
                Specifies Order By columns for conversion_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            excluding_data:
                Optional Argument.
                Specifies the teradataml DataFrame that contains one varchar column
                (excluding_events) containing excluding cause event values.
         
            excluding_data_order_column:
                Optional Argument.
                Specifies Order By columns for excluding_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            optional_data:
                Optional Argument.
                Specifies the teradataml DataFrame that contains one varchar column
                (optional_events) containing optional cause event values.
         
            optional_data_order_column:
                Optional Argument.
                Specifies Order By columns for optional_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            model1_type:
                Required Argument.
                Specifies the teradataml DataFrame that defines the type and
                specification of the first model.
                For example:
                    model1_data ("EVENT_REGULAR", "email:0.19:LAST_CLICK:NA",
                    "impression:0.81:WEIGHTED:0.4,0.3,0.2,0.1")
         
            model1_type_order_column:
                Optional Argument.
                Specifies Order By columns for model1_type.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            model2_type:
                Optional Argument.
                Specifies the teradataml DataFrame that defines the type and
                distributions of the second model.
                For example:
                    model2_data ("EVENT_OPTIONAL", "OrganicSearch:0.5:UNIFORM:NA",
                    "Direct:0.3:UNIFORM:NA", "Referral:0.2:UNIFORM:NA")
         
            model2_type_order_column:
                Optional Argument.
                Specifies Order By columns for model2_type.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            event_column:
                Required Argument.
                Specifies the name of the input column that contains the clickstream
                events.
                Types: str
         
            timestamp_column:
                Required Argument.
                Specifies the name of the input column that contains the timestamps
                of the clickstream events.
                Types: str
         
            window_size:
                Required Argument.
                Specifies how to determine the maximum window size for the
                attribution calculation:
                    rows:K :
                        Consider the maximum number of events to be attributed,
                        excluding events of types specified in excluding_data,
                        which means assigning attributions to at most K effective
                        events before the current impact event.
                    seconds:K :
                        Consider the maximum time difference between the current
                        impact event and the earliest effective event to be attributed.
                    rows:K&seconds:K2 :
                        Consider both constraints and comply with the stricter one.
                Types: str
         
        RETURNS:
            Instance of Attribution.
            Output teradataml DataFrames can be accessed using attribute
            references, such as AttributionObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example
            load_example_data("attribution", ["attribution_sample_table1",
            "attribution_sample_table2" , "conversion_event_table",
            "optional_event_table", "model1_table", "model2_table"])
         
            # Create teradataml DataFrame objects
            attribution_sample_table1 = DataFrame.from_table("attribution_sample_table1")
            attribution_sample_table2 = DataFrame.from_table("attribution_sample_table2")
            conversion_event_table = DataFrame.from_table("conversion_event_table")
            optional_event_table = DataFrame.from_table("optional_event_table")
            model1_table = DataFrame.from_table("model1_table")
            model2_table = DataFrame.from_table("model2_table")
         
            # Execute function
            attribution_out = Attribution(data=attribution_sample_table1,
                                          data_partition_column="user_id",
                                          data_order_column="time_stamp",
                                          data_optional=attribution_sample_table2,
                                          data_optional_partition_column='user_id',
                                          data_optional_order_column='time_stamp',
                                          event_column="event",
                                          conversion_data=conversion_event_table,
                                          optional_data=optional_event_table,
                                          timestamp_column = "time_stamp",
                                          window_size = "rows:10&seconds:20",
                                          model1_type=model1_table,
                                          model2_type=model2_table
                                          )
         
            # Print the results
            print(attribution_out.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data  
        self.data_optional  = data_optional 
        self.conversion_data  = conversion_data 
        self.excluding_data  = excluding_data 
        self.optional_data  = optional_data 
        self.model1_type  = model1_type 
        self.model2_type  = model2_type 
        self.event_column  = event_column 
        self.timestamp_column  = timestamp_column
        self.window_size  = window_size
        self.data_partition_column  = data_partition_column 
        self.data_optional_partition_column  = data_optional_partition_column
        self.data_order_column  = data_order_column 
        self.data_optional_order_column  = data_optional_order_column 
        self.conversion_data_order_column  = conversion_data_order_column 
        self.excluding_data_order_column  = excluding_data_order_column 
        self.optional_data_order_column  = optional_data_order_column 
        self.model1_type_order_column  = model1_type_order_column 
        self.model2_type_order_column  = model2_type_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, False, (str,list)])
        self.__arg_info_matrix.append(["data_optional", self.data_optional, True, (DataFrame)])
        self.__arg_info_matrix.append(["data_optional_partition_column", self.data_optional_partition_column, self.data_optional is None, (str,list)])
        self.__arg_info_matrix.append(["data_optional_order_column", self.data_optional_order_column, self.data_optional is None, (str,list)])
        self.__arg_info_matrix.append(["conversion_data", self.conversion_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["conversion_data_order_column", self.conversion_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["excluding_data", self.excluding_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["excluding_data_order_column", self.excluding_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["optional_data", self.optional_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["optional_data_order_column", self.optional_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["model1_type", self.model1_type, False, (DataFrame)])
        self.__arg_info_matrix.append(["model1_type_order_column", self.model1_type_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["model2_type", self.model2_type, True, (DataFrame)])
        self.__arg_info_matrix.append(["model2_type_order_column", self.model2_type_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["event_column", self.event_column, False, (str)])
        self.__arg_info_matrix.append(["timestamp_column", self.timestamp_column, False, (str)])
        self.__arg_info_matrix.append(["window_size", self.window_size, False, (str)])

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
        self.__awu._validate_input_table_datatype(self.data_optional, "data_optional", None)
        self.__awu._validate_input_table_datatype(self.conversion_data, "conversion_data", None)
        self.__awu._validate_input_table_datatype(self.excluding_data, "excluding_data", None)
        self.__awu._validate_input_table_datatype(self.optional_data, "optional_data", None)
        self.__awu._validate_input_table_datatype(self.model1_type, "model1_type", None)
        self.__awu._validate_input_table_datatype(self.model2_type, "model2_type", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.event_column, "event_column")
        self.__awu._validate_dataframe_has_argument_columns(self.event_column, "event_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.timestamp_column, "timestamp_column")
        self.__awu._validate_dataframe_has_argument_columns(self.timestamp_column, "timestamp_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_optional_partition_column, "data_optional_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_optional_partition_column, "data_optional_partition_column", self.data_optional, "data_optional", True)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_optional_order_column, "data_optional_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_optional_order_column, "data_optional_order_column", self.data_optional, "data_optional", False)
        
        self.__awu._validate_input_columns_not_empty(self.conversion_data_order_column, "conversion_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.conversion_data_order_column, "conversion_data_order_column", self.conversion_data, "conversion_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.excluding_data_order_column, "excluding_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.excluding_data_order_column, "excluding_data_order_column", self.excluding_data, "excluding_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.optional_data_order_column, "optional_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.optional_data_order_column, "optional_data_order_column", self.optional_data, "optional_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.model1_type_order_column, "model1_type_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.model1_type_order_column, "model1_type_order_column", self.model1_type, "model1_type", False)
        
        self.__awu._validate_input_columns_not_empty(self.model2_type_order_column, "model2_type_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.model2_type_order_column, "model2_type_order_column", self.model2_type, "model2_type", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("EventColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.event_column, "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TimestampColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.timestamp_column, "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("WindowSize")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_size, "'"))
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process data_optional
        if self.data_optional is not None:
            self.data_optional_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_optional_partition_column,"\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data_optional, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("input2")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.data_optional_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_optional_order_column, "\""))
        
        # Process conversion_data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.conversion_data, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("conversion")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.conversion_data_order_column, "\""))
        
        # Process excluding_data
        if self.excluding_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.excluding_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("excluding")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.excluding_data_order_column, "\""))
        
        # Process optional_data
        if self.optional_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.optional_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("optional")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.optional_data_order_column, "\""))
        
        # Process model1_type
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.model1_type, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("model1")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.model1_type_order_column, "\""))
        
        # Process model2_type
        if self.model2_type is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.model2_type, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("model2")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.model2_type_order_column, "\""))
        
        function_name = "Attribution"
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
        Returns the string representation for a Attribution class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
