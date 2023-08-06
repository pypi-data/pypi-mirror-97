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
# Function Version: 3.7
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
from teradataml.analytics.mle.SentimentTrainer import SentimentTrainer

class SentimentExtractor:
    
    def __init__(self,
        object = None,
        newdata = None,
        dict_data = None,
        text_column = None,
        language = "en",
        level = "DOCUMENT",
        high_priority = "NONE",
        filter = "ALL",
        accumulate = None,
        newdata_sequence_column = None,
        dict_data_sequence_column = None,
        newdata_order_column = None,
        dict_data_order_column = None):
        """
        DESCRIPTION:
            The SentimentExtractor function extracts the sentiment (positive,
            negative, or neutral) of each input document or sentence, using
            either a classification model output by the function SentimentTrainer
            or a dictionary model.
         
         
        PARAMETERS:
            object:
                Optional Argument.
                Specifies the model type and file. The default model type is
                dictionary. If you omit this argument or specify dictionary without
                dictionary file, then you must specify a dictionary teradataml DataFrame
                with the name dict_data. If you specify both dict and dictionary file, then
                whenever their words conflict, dict has higher priority. The
                dictionary file must be a text file in which each line contains only a
                sentiment word, a space, and the opinion score of the sentiment word.
                If you specify classification:model_file, model_file must be the name
                of a model file generated and installed on the database by the
                function SentimentTrainer.
                Note: Before running the function, add the location of dictionary file or
                      model_file to the user/session default search path.
                Types: str
         
            newdata:
                Required Argument.
                Specifies the teradataml DataFrame defining the input text.
         
            newdata_order_column:
                Optional Argument.
                Specifies Order By columns for newdata.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            dict_data:
                Optional Argument.
                Specifies the teradataml DataFrame defining the dictionary.
         
            dict_data_order_column:
                Optional Argument.
                Specifies Order By columns for dict_data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            text_column:
                Required Argument.
                Specifies the name of the input column that contains text from which
                to extract sentiments.
                Types: str
         
            language:
                Optional Argument.
                Specifies the language of the input text:
                    - en (English)
                    - zh_CN (Simplified Chinese)
                    - zh_TW (Traditional Chinese)
                Default Value: "en"
                Permitted Values: en, zh_CN, zh_TW
                Types: str
         
            level:
                Optional Argument.
                Specifies the level of analysis — whether to analyze each document or
                each sentence.
                Default Value: "DOCUMENT"
                Permitted Values: DOCUMENT, SENTENCE
                Types: str
         
            high_priority:
                Optional Argument.
                Specifies the highest priority when returning results:
                    - NEGATIVE_RECALL: Give highest priority to negative results, including
                                     those with lower confidence sentiment classifications
                                     (maximizes the number of negative results returned).
                    - NEGATIVE_PRECISION: Give highest priority to negative results with
                                        high-confidence sentiment classifications.
                    - POSITIVE_RECALL: Give highest priority to positive results, including
                                    those with lower confidence sentiment classifications
                                    (maximizes the number of positive results returned).
                    - POSITIVE_PRECISION: Give highest priority to positive results with
                                        high-confidence sentiment classifications.
                    NONE: Give all results the same priority.
                Default Value: "NONE"
                Permitted Values: NEGATIVE_RECALL, NEGATIVE_PRECISION,
                POSITIVE_RECALL, POSITIVE_PRECISION, NONE
                Types: str
         
            filter:
                Optional Argument.
                Specifies the kind of results to return:
                    - POSITIVE: Return only results with positive sentiments.
                    - NEGATIVE: Return only results with negative sentiments.
                    - ALL: Return all results.
                Default Value: "ALL"
                Permitted Values: POSITIVE, NEGATIVE, ALL
                Types: str
         
            accumulate:
                Optional Argument.
                Specifies the names of the input columns to copy to the output teradataml DataFrame.
                Types: str OR list of Strings (str)
         
            newdata_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "newdata". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            dict_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "dict_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of SentimentExtractor.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SentimentExtractorObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("sentimenttrainer", "sentiment_train")
            load_example_data("sentimentextractor", ["sentiment_extract_input", "sentiment_word"])
         
            # Create teradataml DataFrame objects.
            sentiment_train = DataFrame.from_table("sentiment_train")
            sentiment_extract_input = DataFrame.from_table("sentiment_extract_input")
            sentiment_word = DataFrame.from_table("sentiment_word")
         
            # Example 1 - This example uses the dictionary model file to analyze each document.
            SentimentExtractor_out1 = SentimentExtractor(object = "dictionary",
                                                        newdata = sentiment_extract_input,
                                                        text_column = "review",
                                                        level = "document",
                                                        accumulate = ["id","product"]
                                                        )
            # Print the results
            print(SentimentExtractor_out1)
         
            # Example 2 - This example uses the dictionary model file to analyze each sentence.
            SentimentExtractor_out2 = SentimentExtractor(object = "dictionary",
                                                        newdata = sentiment_extract_input,
                                                        text_column = "review",
                                                        level = "sentence",
                                                        accumulate = ["id","product"]
                                                        )
            # Print the results
            print(SentimentExtractor_out2)
         
            # Example 3 - This example uses a maximum entropy classification model file.
            SentimentExtractor_out3 = SentimentExtractor(object = "classification:default_sentiment_classification_model.bin",
                                                        newdata = sentiment_extract_input,
                                                        text_column = "review",
                                                        level = "document",
                                                        accumulate = ["id"]
                                                        )
            # Print the results
            print(SentimentExtractor_out3)
         
            # Example 4 - This example uses a model file output by the SentimentTrainer function.
            SentimentTrainer_out = SentimentTrainer(data = sentiment_train,
                                                    text_column = "review",
                                                    sentiment_column = "category",
                                                    model_file = "sentimentmodel1.bin"
                                                    )
         
            SentimentExtractor_out4 = SentimentExtractor(object = "classification:sentimentmodel1.bin",
                                                        newdata = sentiment_extract_input,
                                                        text_column = "review",
                                                        level = "document",
                                                        accumulate = ["id"]
                                                        )
            # Print the results
            print(SentimentExtractor_out4)
         
            # Example 5 - This example uses a dictionary instead of a model file.
            SentimentExtractor_out5 = SentimentExtractor(dict_data = sentiment_word,
                                                        newdata = sentiment_extract_input,
                                                        text_column = "review",
                                                        level = "document",
                                                        accumulate = ["id", "product"]
                                                        )
            # Print the results
            print(SentimentExtractor_out5)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.newdata  = newdata 
        self.dict_data  = dict_data 
        self.text_column  = text_column 
        self.language  = language 
        self.level  = level 
        self.high_priority  = high_priority 
        self.filter  = filter 
        self.accumulate  = accumulate 
        self.newdata_sequence_column  = newdata_sequence_column 
        self.dict_data_sequence_column  = dict_data_sequence_column 
        self.newdata_order_column  = newdata_order_column 
        self.dict_data_order_column  = dict_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, True, (str)])
        self.__arg_info_matrix.append(["newdata", self.newdata, False, (DataFrame)])
        self.__arg_info_matrix.append(["newdata_order_column", self.newdata_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["dict_data", self.dict_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["dict_data_order_column", self.dict_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["text_column", self.text_column, False, (str)])
        self.__arg_info_matrix.append(["language", self.language, True, (str)])
        self.__arg_info_matrix.append(["level", self.level, True, (str)])
        self.__arg_info_matrix.append(["high_priority", self.high_priority, True, (str)])
        self.__arg_info_matrix.append(["filter", self.filter, True, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["newdata_sequence_column", self.newdata_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["dict_data_sequence_column", self.dict_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.newdata, "newdata", None)
        self.__awu._validate_input_table_datatype(self.dict_data, "dict_data", None)
        
        # Check for permitted values
        language_permitted_values = ["EN", "ZH_CN", "ZH_TW"]
        self.__awu._validate_permitted_values(self.language, language_permitted_values, "language")
        
        level_permitted_values = ["DOCUMENT", "SENTENCE"]
        self.__awu._validate_permitted_values(self.level, level_permitted_values, "level")
        
        high_priority_permitted_values = ["NEGATIVE_RECALL", "NEGATIVE_PRECISION", "POSITIVE_RECALL", "POSITIVE_PRECISION", "NONE"]
        self.__awu._validate_permitted_values(self.high_priority, high_priority_permitted_values, "high_priority")
        
        filter_permitted_values = ["POSITIVE", "NEGATIVE", "ALL"]
        self.__awu._validate_permitted_values(self.filter, filter_permitted_values, "filter")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.text_column, "text_column")
        self.__awu._validate_dataframe_has_argument_columns(self.text_column, "text_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_sequence_column, "newdata_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_sequence_column, "newdata_sequence_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.dict_data_sequence_column, "dict_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.dict_data_sequence_column, "dict_data_sequence_column", self.dict_data, "dict_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_order_column, "newdata_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_order_column, "newdata_order_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.dict_data_order_column, "dict_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.dict_data_order_column, "dict_data_order_column", self.dict_data, "dict_data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("TextColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.text_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.language is not None and self.language != "en":
            self.__func_other_arg_sql_names.append("InputLanguage")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.language, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.object is not None:
            self.__func_other_arg_sql_names.append("ModelFile")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.object, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.level is not None and self.level != "DOCUMENT":
            self.__func_other_arg_sql_names.append("AnalysisType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.level, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.high_priority is not None and self.high_priority != "NONE":
            self.__func_other_arg_sql_names.append("Priority")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.high_priority, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.filter is not None and self.filter != "ALL":
            self.__func_other_arg_sql_names.append("OutputType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.filter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.newdata_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.newdata_sequence_column, ""))
        
        if self.dict_data_sequence_column is not None:
            sequence_input_by_list.append("dict:" + UtilFuncs._teradata_collapse_arglist(self.dict_data_sequence_column, ""))
        
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
        
        # Process newdata
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.newdata, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.newdata_order_column, "\""))
        
        # Process dict_data
        if self.dict_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.dict_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("dict")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.dict_data_order_column, "\""))
        
        function_name = "SentimentExtractor"
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
        Returns the string representation for a SentimentExtractor class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
