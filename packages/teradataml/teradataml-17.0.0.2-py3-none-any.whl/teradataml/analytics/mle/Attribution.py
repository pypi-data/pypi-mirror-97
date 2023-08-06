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
# Function Version: 2.10
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
        conversion_events = None,
        excluding_data = None,
        optional_data = None,
        model1_type = None,
        model2_type = None,
        model1_name = None,
        model2_name = None,
        event_column = None,
        timestamp_column = None,
        window_size = None,
        conversion_data = None,
        optional_events = None,
        exclude_events = None,
        data_sequence_column = None,
        data_optional_sequence_column = None,
        conversion_data_sequence_column = None,
        excluding_data_sequence_column = None,
        optional_data_sequence_column = None,
        model1_type_sequence_column = None,
        model2_type_sequence_column = None,
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

            The function calculates attributions with a choice of distribution
            models and has two versions:
                • Multiple-input: Accepts one or more input tables and gets many
                parameters from other dimension tables.
                • Single-input: Accepts only one input table and gets all parameters
                from argments.

            Note: This function is available only when teradataml is connected to
                  Vantage 1.1 or later versions.


        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame that contains the click stream
                data, which the function uses to compute attributions.

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
                Specifies the teradataml DataFrame that contains additional click
                stream data, which cogroup attributes from all specified teradataml
                DataFrame.

            data_optional_partition_column:
                Optional Argument. Required when 'data_optional' is used.
                Specifies Partition By columns for data_optional.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)

            data_optional_order_column:
                Optional Argument. Required when 'data_optional' is used.
                Specifies Order By columns for data_optional.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            conversion_events:
                Optional Argument. "conversion_events" is a required argument if
                "conversion_data" is not provided.
                Specifies the conversion event value. Each conversion_event is
                a string or integer.
                Types: str OR list of Strings (str)

            excluding_data:
                Optional Argument.
                Specifies the teradataml DataFrame that contains one varchar
                column (excluding_events) containing excluding cause event values.

            excluding_data_order_column:
                Optional Argument.
                Specifies Order By columns for excluding_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            optional_data:
                Optional Argument.
                Specifies the teradataml DataFrame that contains one varchar
                column (optional_events) containing optional cause event values.

            optional_data_order_column:
                Optional Argument.
                Specifies Order By columns for optional_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            model1_type:
                Optional Argument. "model1_type" is a required argument if
                "model1_name" is not provided.
                Specifies the teradataml DataFrame that defines the type and
                specification of the first model.
                For example:
                    model1 data ("EVENT_REGULAR", "email:0.19:LAST_CLICK:NA",
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
                    model2 data ("EVENT_OPTIONAL", "OrganicSearch:0.5:UNIFORM:NA",
                    "Direct:0.3:UNIFORM:NA", "Referral:0.2:UNIFORM:NA")

            model2_type_order_column:
                Optional Argument.
                Specifies Order By columns for model2_type.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            model1_name:
                Optional Argument. "model1_name" is a required argument if
                "model1_type" is not provided.
                Specifies the type and specifcation of the first model.

                For example:
                    Model1 ('EVENT_REGULAR', 'email:0.19:LAST_CLICK:NA',
                        'impression:0.81:WEIGHTED:0.4,0.3,0.2,0.1')
                Types: str OR list of Strings (str)

            model2_name:
                Optional Argument.
                Specifies the type and distributions of the second model.
                For example:
                    Model2 ('EVENT_OPTIONAL', 'OrganicSearch:0.5:UNIFORM:NA',
                            'Direct:0.3:UNIFORM:NA', 'Referral:0.2:UNIFORM:NA')
                Types: str OR list of Strings (str)

            event_column:
                Required Argument.
                Specifies the name of an input teradataml DataFrame column that
                contains the clickstream events.
                Types: str

            timestamp_column:
                Required Argument.
                Specifies the name of an input teradataml DataFrame column that
                contains the timestamps of the clickstream events.
                Types: str

            window_size:
                Required Argument.
                Specifies how to determine the maximum window size for the
                attribution calculation:
                    • rows:K: Consider the maximum number of events to be attributed,
                      excluding events of types specified in excluding_event_table,
                      which means assigning attributions to atmost K effective
                      events before the current impact event.
                    • seconds:K: Consider the maximum time difference between the
                      current impact event and the earliest effective event to
                      be attributed.
                    • rows:K&seconds:K2: Consider both constraints and comply with
                      the stricter one.
                Types: str

            conversion_data:
                Optional Argument. "conversion_data" is a required argument if
                "conversion_events" is not provided.
                Specifies the teradataml DataFrame that contains one varchar
                column (conversion_events) containing conversion event values.


            conversion_data_order_column:
                Optional Argument.
                Specifies Order By columns for conversion_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            optional_events:
                Optional Argument.
                Specifies the optional events. Each optional_event is a string or
                integer. An optional_event cannot be a conversion_event or
                exclude_event. The function attributes a conversion event to an
                optional event only if it cannot attribute it to a regular event.
                Types: str OR list of Strings (str)

            exclude_events:
                Optional Argument.
                Specifies the events to exclude from the attribution calculation.
                Each exclude_event is a string or integer. An exclude_event
                cannot be a conversion_event.
                Types: str OR list of Strings (str)

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            data_optional_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data_optional". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            conversion_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "conversion_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            excluding_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "excluding_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            optional_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "optional_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            model1_type_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "model1_type". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            model2_type_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "model2_type". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        Note:
            • The Multiple-input Attribution takes data from multiple teradataml
              DataFrames ("data_optional", "conversion_data", "excluding_data",
              "optional_data", "model1_type" and "model2_type").
              For Multiple-input Attribution, inputs "data", "conversion_data" and
              "model1_type" are required, where as other inputs are optional.
              The arguments "data_optional", "conversion_data", "excluding_data",
              "optional_data", "model1_type" and "model2_type" should be mentioned
              together and should not be used with arguments "conversion_events",
              "model1_name", "optional_events", "exclude_events" and "model2_name".
              For example,
                  attribution = Attribution(data=< table | view | (query) >,
                                 data_partition_column='partition_column',
                                 data_order_column='order_column',
                                 data_optional=< table | view | (query) >,
                                 conversion_data=< table | view | (query) >,
                                 excluding_data=< table | view | (query) >,
                                 optional_data=< table | view | (query) >,
                                 model1_type=< table | view | (query) >,
                                 model2_type=< table | view | (query) >,
                                 event_column='event_column',
                                 timestamp_column='timestamp_column',
                                 window_size='rows:K | seconds:K | rows:K&seconds:K'
                                 )

            • The Single-input Attribution takes data from single teradataml
              DataFrame ("data") and parameters come from arguments ("conversion_events",
              "model1_name", "optional_events", "exclude_events" and "model2_name"),
              not input teradataml DataFrames.
              For Single-input Attribution arguments "conversion_events" and "model1_name"
              are required, where as other single input syntax arguments are optional.
              The arguments "conversion_events", "model1_name", "optional_events",
              "exclude_events" and "model2_name" should be used together and
              should not be used with arguments "data_optional", "conversion_data",
              "excluding_data", "optional_data", "model1_type" and "model2_type".
              For example,
                  attribution = Attribution(data=< table | view | (query) >,
                                          conversion_events = ['conversion_event', ...],
                                          timestamp_column=''timestamp_column'',
                                          model1_name = ['type',  'K' | 'EVENT:WEIGHT:MODEL:PARAMETERS', ...],
                                          model2_name = ['type',  'K' | 'EVENT:WEIGHT:MODEL:PARAMETERS', ...],
                                          event_column = "event_column"
                                          window_size = 'rows:K | seconds:K | rows:K&seconds:K',
                                          optional_events = ["organicsearch", "direct", "referral"],
                                          data_order_column='order_by_column'
                                          )


        RETURNS:
            Instance of Attribution.
            Output teradataml DataFrames can be accessed using attribute
            references, such as AttributionObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("attribution", ["attribution_sample_table",
            "attribution_sample_table1", "attribution_sample_table2" ,
            "conversion_event_table", "optional_event_table", "excluding_event_table",
            "model1_table", "model2_table"])

            # Create TeradataML DataFrame objects.
            attribution_sample_table = DataFrame.from_table("attribution_sample_table")
            attribution_sample_table1 = DataFrame.from_table("attribution_sample_table1")
            attribution_sample_table2 = DataFrame.from_table("attribution_sample_table2")
            conversion_event_table = DataFrame.from_table("conversion_event_table")
            optional_event_table = DataFrame.from_table("optional_event_table")
            model1_table = DataFrame.from_table("model1_table")
            model2_table = DataFrame.from_table("model2_table")
            excluding_event_table = DataFrame("excluding_event_table")

            # Example 1 - One Regular Model, Multiple Optional Models.
            # This example specifes one distribution model for regular events
            # and one distribution model for each type of optional event.
            attribution_out1 = Attribution(data=attribution_sample_table,
                                          data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["EVENT_REGULAR",
                                          "email:0.19:LAST_CLICK:NA","impression:0.81:UNIFORM:NA"],
                                          model2_name = ["EVENT_OPTIONAL",
                                          "organicsearch:0.5:UNIFORM:NA","direct:0.3:UNIFORM:NA",
                                          "referral:0.2:UNIFORM:NA"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          optional_events = ["organicsearch", "direct", "referral"],
                                          data_order_column='time_stamp'
                                          )

            # Print the result
            print(attribution_out1.result)

            # Example 2 - Multiple Regular Models, One Optional Model.
            # This example specifes one distribution model for each type of regular
            # event and one distribution model for optional events.
            attribution_out2 = Attribution(data=attribution_sample_table,
                                          data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["EVENT_REGULAR",
                                          "email:0.19:LAST_CLICK:NA","impression:0.81:UNIFORM:NA"],
                                          model2_name = ["EVENT_OPTIONAL", "ALL:1:EXPONENTIAL:0.5,ROW"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          optional_events = ["organicsearch", "direct", "referral"],
                                          data_order_column='time_stamp'
                                          )
            # Print the result
            print(attribution_out2)

            # Example 3 - # This example uses Dynamic Weighted Distribution
            # Models Input.
            attribution_out3 = Attribution(data=attribution_sample_table,
                                          data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["EVENT_REGULAR",
                                          "email:0.19:LAST_CLICK:NA","impression:0.81:WEIGHTED:0.4,0.3,0.2,0.1"],
                                          model2_name = ["EVENT_OPTIONAL", "ALL:1:WEIGHTED:0.4,0.3,0.2,0.1"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          optional_events = ["organicsearch", "direct", "referral"],
                                          data_order_column='time_stamp'
                                          )

            # Print the result
            print(attribution_out3.result)

            # Example 4 - This example uses Window Models.
            attribution_out4 = Attribution(data=attribution_sample_table,
                                           data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["SEGMENT_ROWS",
                                          "3:0.5:EXPONENTIAL:0.5,ROW","4:0.3:WEIGHTED:0.4,0.3,0.2,0.1",
                                          "3:0.2:FIRST_CLICK:NA"],
                                          model2_name = ["SEGMENT_SECONDS", "6:0.5:UNIFORM:NA",
                                          "8:0.3:LAST_CLICK:NA","6:0.2:FIRST_CLICK:NA"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          optional_events = ["organicsearch", "direct", "referral"],
                                          exclude_events = ["email"],
                                          data_order_column='time_stamp'
                                          )

            # Print the result
            print(attribution_out4.result)

            # Example 5 - This example uses Single-Window Model.
            attribution_out5 = Attribution(data=attribution_sample_table,
                                           data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["SIMPLE", "UNIFORM:NA"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          exclude_events = ["email"],
                                          data_order_column='time_stamp'
                                          )

            # Print the result
            print(attribution_out5.result)


            # Example 6 - This example uses Unused Segment Windows.
            attribution_out6 = Attribution(data=attribution_sample_table,
                                          data_partition_column='user_id',
                                          conversion_events = ["socialnetwork", "paidsearch"],
                                          timestamp_column='time_stamp',
                                          model1_name = ["SEGMENT_ROWS",
                                          "3:0.5:EXPONENTIAL:0.5,ROW","4:0.3:WEIGHTED:0.4,0.3,0.2,0.1",
                                          "3:0.2:FIRST_CLICK:NA"],
                                          model2_name = ["SEGMENT_SECONDS",
                                          "6:0.5:UNIFORM:NA","8:0.3:LAST_CLICK:NA", "6:0.2:FIRST_CLICK:NA"],
                                          event_column = "event",
                                          window_size = "rows:10&seconds:20",
                                          data_order_column='time_stamp'
                                          )

            # Print the result
            print(attribution_out6.result)

            # Example 7 - This example uses Multiple Inputs which takes data
            # and parameters from multiple tables and outputs attributions.
            attribution_out7 = Attribution(data=attribution_sample_table1,
                                 data_partition_column='user_id',
                                 data_order_column='time_stamp',
                                 data_optional=attribution_sample_table2,
                                 data_optional_partition_column='user_id',
                                 data_optional_order_column='time_stamp',
                                 conversion_data=conversion_event_table,
                                 excluding_data=excluding_event_table,
                                 optional_data=optional_event_table,
                                 model1_type=model1_table,
                                 model2_type=model2_table,
                                 event_column='event',
                                 timestamp_column='time_stamp',
                                 window_size='rows:10&seconds:20'
                                 )
            # Print the result
            print(attribution_out7.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.data_optional  = data_optional 
        self.conversion_events  = conversion_events 
        self.excluding_data  = excluding_data 
        self.optional_data  = optional_data 
        self.model1_type  = model1_type 
        self.model2_type  = model2_type 
        self.model1_name  = model1_name 
        self.model2_name  = model2_name 
        self.event_column  = event_column 
        self.timestamp_column  = timestamp_column 
        self.window_size  = window_size 
        self.conversion_data  = conversion_data 
        self.optional_events  = optional_events 
        self.exclude_events  = exclude_events 
        self.data_sequence_column  = data_sequence_column 
        self.data_optional_sequence_column  = data_optional_sequence_column 
        self.conversion_data_sequence_column  = conversion_data_sequence_column 
        self.excluding_data_sequence_column  = excluding_data_sequence_column 
        self.optional_data_sequence_column  = optional_data_sequence_column 
        self.model1_type_sequence_column  = model1_type_sequence_column 
        self.model2_type_sequence_column  = model2_type_sequence_column 
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
        self.__arg_info_matrix.append(["conversion_events", self.conversion_events, True, (str,list)])
        self.__arg_info_matrix.append(["excluding_data", self.excluding_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["excluding_data_order_column", self.excluding_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["optional_data", self.optional_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["optional_data_order_column", self.optional_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["model1_type", self.model1_type, True, (DataFrame)])
        self.__arg_info_matrix.append(["model1_type_order_column", self.model1_type_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["model2_type", self.model2_type, True, (DataFrame)])
        self.__arg_info_matrix.append(["model2_type_order_column", self.model2_type_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["model1_name", self.model1_name, True, (str,list)])
        self.__arg_info_matrix.append(["model2_name", self.model2_name, True, (str,list)])
        self.__arg_info_matrix.append(["event_column", self.event_column, False, (str)])
        self.__arg_info_matrix.append(["timestamp_column", self.timestamp_column, False, (str)])
        self.__arg_info_matrix.append(["window_size", self.window_size, False, (str)])
        self.__arg_info_matrix.append(["conversion_data", self.conversion_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["conversion_data_order_column", self.conversion_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["optional_events", self.optional_events, True, (str,list)])
        self.__arg_info_matrix.append(["exclude_events", self.exclude_events, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_optional_sequence_column", self.data_optional_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["conversion_data_sequence_column", self.conversion_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["excluding_data_sequence_column", self.excluding_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["optional_data_sequence_column", self.optional_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["model1_type_sequence_column", self.model1_type_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["model2_type_sequence_column", self.model2_type_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.data_optional, "data_optional", None)
        self.__awu._validate_input_table_datatype(self.conversion_data, "conversion_data", None)
        self.__awu._validate_input_table_datatype(self.excluding_data, "excluding_data", None)
        self.__awu._validate_input_table_datatype(self.optional_data, "optional_data", None)
        self.__awu._validate_input_table_datatype(self.model1_type, "model1_type", None)
        self.__awu._validate_input_table_datatype(self.model2_type, "model2_type", None)

        # Make sure either multi-input arguments (data_optional, conversion_data,
        # excluding_data, optional_data, model1_type and model2_type ) or single-input
        # arguments (conversion_events, model1_name, optional_events, exclude_events
        # model2_name) syntax is being used.
        # To do so, let's define some flags and let's based on those.
        # List of Multi-syntax arguments
        multi_input_syntax_args=[self.data_optional, self.conversion_data, self.model1_type, self.model2_type, self.optional_data, self.excluding_data]
        # Flag to see if all Multi-input required arguments are not None
        all_multiple_input_reqd_syntax_args_not_none = all([self.conversion_data, self.model1_type])
        # Flag to see if any Multi-input arguments is not None
        any_multiple_input_syntax_args_not_none = any(multi_input_syntax_args)
        # List of Multi-syntax arguments
        single_input_syntax_args=[self.conversion_events, self.model1_name, self.model2_name, self.optional_events, self.exclude_events]
        # Flag to see if all Single-input required arguments are not None
        all_single_input_reqd_syntax_args_not_none = all([self.conversion_events, self.model1_name])
        # Flag to see if any Single-input arguments is not None
        any_single_input_syntax_args_not_none = any(single_input_syntax_args)

        # We shall raise error for all of the following cases:
        #       1. Case when none of the syntax arguments are provided.
        #          Condition:
        #               not (any_multiple_input_syntax_args_not_none or any_single_input_syntax_args_not_none)
        #       2. Case when mix of multiple syntax and single syntax arguments are provided.
        #          Condition:
        #               (any_multiple_input_syntax_args_not_none and any_single_input_syntax_args_not_none)
        #       3. Case when any of multiple syntax args is provided but one of required multiple
        #          syntax argument is missing.
        #          Condition:
        #               not (any_multiple_input_syntax_args_not_none and all_multiple_input_reqd_syntax_args_not_none)
        #       4. Case when any of multiple syntax args is provided but one of required multiple
        #          syntax argument is missing.
        #          Condition:
        #               not (any_single_input_syntax_args_not_none and all_single_input_reqd_syntax_args_not_none)
        if (any_multiple_input_syntax_args_not_none and any_single_input_syntax_args_not_none) \
                or (not (any_multiple_input_syntax_args_not_none or any_single_input_syntax_args_not_none)) \
                or (any_multiple_input_syntax_args_not_none and not all_multiple_input_reqd_syntax_args_not_none) \
                or (any_single_input_syntax_args_not_none and not all_single_input_reqd_syntax_args_not_none):
            raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "Multi-input syntax (data_optional, conversion_data (Required), excluding_data, optional_data, model1_type (Required) and model2_type)",
                                                           "Single-input syntax (conversion_events (Required), model1_name (Required), optional_events, exclude_events and model2_name)"),
                                      MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.event_column, "event_column")
        self.__awu._validate_dataframe_has_argument_columns(self.event_column, "event_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.timestamp_column, "timestamp_column")
        self.__awu._validate_dataframe_has_argument_columns(self.timestamp_column, "timestamp_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_optional_sequence_column, "data_optional_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_optional_sequence_column, "data_optional_sequence_column", self.data_optional, "data_optional", False)
        
        self.__awu._validate_input_columns_not_empty(self.conversion_data_sequence_column, "conversion_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.conversion_data_sequence_column, "conversion_data_sequence_column", self.conversion_data, "conversion_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.excluding_data_sequence_column, "excluding_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.excluding_data_sequence_column, "excluding_data_sequence_column", self.excluding_data, "excluding_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.optional_data_sequence_column, "optional_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.optional_data_sequence_column, "optional_data_sequence_column", self.optional_data, "optional_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.model1_type_sequence_column, "model1_type_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.model1_type_sequence_column, "model1_type_sequence_column", self.model1_type, "model1_type", False)
        
        self.__awu._validate_input_columns_not_empty(self.model2_type_sequence_column, "model2_type_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.model2_type_sequence_column, "model2_type_sequence_column", self.model2_type, "model2_type", False)
        
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
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.event_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("TimestampColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.timestamp_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("WindowSize")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.window_size, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.conversion_events is not None:
            self.__func_other_arg_sql_names.append("ConversionEvents")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.conversion_events, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.exclude_events is not None:
            self.__func_other_arg_sql_names.append("ExcludeEvents")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.exclude_events, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.optional_events is not None:
            self.__func_other_arg_sql_names.append("OptionalEvents")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.optional_events, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.model1_name is not None:
            self.__func_other_arg_sql_names.append("FirstModel")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model1_name, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.model2_name is not None:
            self.__func_other_arg_sql_names.append("SecondModel")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model2_name, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.data_optional_sequence_column is not None:
            sequence_input_by_list.append("input2:" + UtilFuncs._teradata_collapse_arglist(self.data_optional_sequence_column, ""))
        
        if self.conversion_data_sequence_column is not None:
            sequence_input_by_list.append("conversion:" + UtilFuncs._teradata_collapse_arglist(self.conversion_data_sequence_column, ""))
        
        if self.excluding_data_sequence_column is not None:
            sequence_input_by_list.append("excluding:" + UtilFuncs._teradata_collapse_arglist(self.excluding_data_sequence_column, ""))
        
        if self.optional_data_sequence_column is not None:
            sequence_input_by_list.append("optional:" + UtilFuncs._teradata_collapse_arglist(self.optional_data_sequence_column, ""))
        
        if self.model1_type_sequence_column is not None:
            sequence_input_by_list.append("model1:" + UtilFuncs._teradata_collapse_arglist(self.model1_type_sequence_column, ""))
        
        if self.model2_type_sequence_column is not None:
            sequence_input_by_list.append("model2:" + UtilFuncs._teradata_collapse_arglist(self.model2_type_sequence_column, ""))
        
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process data_optional
        if self.data_optional is not None:
            self.data_optional_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_optional_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data_optional)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("input2")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.data_optional_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_optional_order_column, "\""))
        
        # Process conversion_data
        if self.conversion_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.conversion_data)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("conversion")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.conversion_data_order_column, "\""))
        
        # Process excluding_data
        if self.excluding_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.excluding_data)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("excluding")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.excluding_data_order_column, "\""))
        
        # Process optional_data
        if self.optional_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.optional_data)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("optional")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.optional_data_order_column, "\""))
        
        # Process model1_type
        if self.model1_type is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.model1_type)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("model1")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.model1_type_order_column, "\""))
        
        # Process model2_type
        if self.model2_type is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.model2_type)
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
        Function to generate AED nodes for output tables.
        This makes a call aed_ml_query() and then output table dataframes are created.
        """
        # Create a list of input node ids contributing to a query.
        self.__input_nodeids = []
        self.__input_nodeids.append(self.data._nodeid)
        if self.data_optional is not None:
            self.__input_nodeids.append(self.data_optional._nodeid)
        if self.conversion_data is not None:
            self.__input_nodeids.append(self.conversion_data._nodeid)
        if self.excluding_data is not None:
            self.__input_nodeids.append(self.excluding_data._nodeid)
        if self.optional_data is not None:
            self.__input_nodeids.append(self.optional_data._nodeid)
        if self.model1_type is not None:
            self.__input_nodeids.append(self.model1_type._nodeid)
        if self.model2_type is not None:
            self.__input_nodeids.append(self.model2_type._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "Attribution", self.__aqg_obj._multi_query_input_nodes)
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
            
        stdout_column_info_name.append("attribution")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        stdout_column_info_name.append("time_to_conversion")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
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
        Returns the string representation for a Attribution class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
