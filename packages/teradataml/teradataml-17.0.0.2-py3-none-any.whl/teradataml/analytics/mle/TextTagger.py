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

class TextTagger:
    
    def __init__(self,
        data = None,
        rules_data = None,
        language = "en",
        rules = None,
        tokenize = False,
        outputby_tag = False,
        tag_delimiter = ",",
        accumulate = None,
        data_sequence_column = None,
        rules_data_sequence_column = None,
        data_order_column = None,
        rules_data_order_column = None):
        """
        DESCRIPTION:
            The TextTagger function tags text documents according to user-defined
            rules that use text-processing and logical operators.


        PARAMETERS:
            data:
                Required Argument.
                The input teradataml DataFrame that contains the texts.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            rules_data:
                Optional Argument.
                The input teradataml DataFrame that contains the rules.

            rules_data_order_column:
                Optional Argument.
                Specifies Order By columns for rules_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            language:
                Optional Argument.
                Specifies the language of the input text:  "en": English (default),
                "zh_cn": Simple Chinese,  "zh_tw": Traditional Chinese, If Tokenize
                specifies "true", then the function uses the value of Language to
                create the word tokenizer.
                Default Value: "en"
                Permitted Values: en, zh_CN, zh_TW
                Types: str

            rules:
                Optional Argument.
                Specifies the tag names and tagging rules. Use this argument if and
                only if you do not specify a rules table. For information about
                defining tagging rules, refer to "Defining Tagging Rules" in function documentation.
                Types: str OR list of Strings (str)

            tokenize:
                Optional Argument.
                Specifies whether the function tokenizes the input text before
                evaluating the rules and tokenizes the text string parameter in the
                rule definition when parsing a rule. If you specify "True", then you
                must also specify the Language argument.
                Default Value: False
                Types: bool

            outputby_tag:
                Optional Argument.
                Specifies whether the function outputs a tuple when a text document
                matches multiple tags. which means that one tuple in the output
                stands for one document and the matched tags are listed in the output
                column tag.
                Default Value: False
                Types: bool

            tag_delimiter:
                Optional Argument.
                Specifies the delimiter that separates multiple tags in the output
                column tag if outputby.tag has the value "False" (the default). The
                default value is the comma (,). If outputby.tag has the value "True",
                specifying this argument causes an error.
                Default Value: ","
                Types: str

            accumulate:
                Optional Argument.
                Specifies the names of text teradataml DataFrame columns to copy to
                the output table.
                Note: Do not use the name "tag" for an accumulate_column, because the
                      function uses that name for the output teradataml DataFrame column
                      that contains the tags.
                Types: str OR list of Strings (str)

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            rules_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "rules_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of TextTagger.
            Output teradataml DataFrames can be accessed using attribute
            references, such as TextTaggerObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load the data to run the example.
            load_example_data("TextTagger",["text_inputs","rule_inputs"])

            # Create teradataml DataFrame objects.
            text_inputs = DataFrame("text_inputs")
            rule_inputs = DataFrame("rule_inputs")

            # Example 1:
            # Passing rules through 'rules_data' argument as teradataml dataframe.
            result = TextTagger(data=text_inputs,
                                rules_data=rule_inputs,
                                accumulate='id',
                                language='en',
                                tokenize=False,
                                outputby_tag=False,
                                tag_delimiter=',',
                                data_sequence_column='id',
                                rules_data_sequence_column='tagname')
            # Print the result
            print(result.result)

            # Example 2:
            # Passing rules through 'rules' argument as List of strings
            result = TextTagger(data=text_inputs,
                                accumulate='id',
                                rules=[
                                    'contain(content,"floods",1,) or contain(content,"tsunamis",1,) AS Natural-Disaster',
                                    'contain(content,"Roger",1,) and contain(content,"Nadal",1,) AS Tennis-Rivalry',
                                    'contain(titles,"Tennis",1,) and contain(content,"Roger",1,)  AS Tennis-Greats',
                                    'contain(content,"India",1,) and contain(content,"Pakistan",1,) AS Cricket-Rivalry',
                                    'contain(content,"Australia",1,) and contain(content,"England",1,) AS The-Ashes'],
                                language='en',
                                tokenize=False,
                                outputby_tag=False,
                                tag_delimiter=',',
                                data_sequence_column='id')
            # Print the result
            print(result.result)

            # Example 3 - Specify dictionary file in rules argument
            result = TextTagger(data = text_inputs,
                                rules=['dict(content, "keywords.txt", 1,) and equal(titles, "Chennai Floods") AS Natural-Disaster',
                                       'dict(content, "keywords.txt", 2,) and equal(catalog, "sports") AS Great-Sports-Rivalry '],
                                accumulate = ["id"])

            # Print the result
            print(result.result)

            # Example 4 - Specify superdist in rules argument
            result = TextTagger(data = text_inputs,
                                rules=['superdist(content,"Chennai","floods",sent,,) AS Chennai-Flood-Disaster',
                                        'superdist(content,"Roger","titles",para, "Nadal",para) AS Roger-Champion',
                                        'superdist(content,"Roger","Nadal",para,,) AS Tennis-Rivalry',
                                        'contain(content,regex"[A|a]shes",2,) AS Aus-Eng-Cricket',
                                        'superdist(content,"Australia","won",nw5,,) AS Aus-victory'],
                                accumulate = ["id"]
                                )
            # Print the result
            print(result.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.rules_data  = rules_data 
        self.language  = language 
        self.rules  = rules 
        self.tokenize  = tokenize 
        self.outputby_tag  = outputby_tag 
        self.tag_delimiter  = tag_delimiter 
        self.accumulate  = accumulate 
        self.data_sequence_column  = data_sequence_column 
        self.rules_data_sequence_column  = rules_data_sequence_column 
        self.data_order_column  = data_order_column 
        self.rules_data_order_column  = rules_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["rules_data", self.rules_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["rules_data_order_column", self.rules_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["language", self.language, True, (str)])
        self.__arg_info_matrix.append(["rules", self.rules, True, (str,list)])
        self.__arg_info_matrix.append(["tokenize", self.tokenize, True, (bool)])
        self.__arg_info_matrix.append(["outputby_tag", self.outputby_tag, True, (bool)])
        self.__arg_info_matrix.append(["tag_delimiter", self.tag_delimiter, True, (str)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["rules_data_sequence_column", self.rules_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.rules_data, "rules_data", None)
        
        # Check for permitted values
        language_permitted_values = ["EN", "ZH_CN", "ZH_TW"]
        self.__awu._validate_permitted_values(self.language, language_permitted_values, "language")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.rules_data_sequence_column, "rules_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.rules_data_sequence_column, "rules_data_sequence_column", self.rules_data, "rules_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.rules_data_order_column, "rules_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.rules_data_order_column, "rules_data_order_column", self.rules_data, "rules_data", False)
        
        
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
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.rules is not None:
            self.__func_other_arg_sql_names.append("TaggingRules")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.rules, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.language is not None and self.language != "en":
            self.__func_other_arg_sql_names.append("InputLanguage")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.language, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.tokenize is not None and self.tokenize != False:
            self.__func_other_arg_sql_names.append("Tokenize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.tokenize, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.outputby_tag is not None and self.outputby_tag != False:
            self.__func_other_arg_sql_names.append("OutputbyTag")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.outputby_tag, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.tag_delimiter is not None and self.tag_delimiter != ",":
            self.__func_other_arg_sql_names.append("TagDelimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.tag_delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.rules_data_sequence_column is not None:
            sequence_input_by_list.append("rules:" + UtilFuncs._teradata_collapse_arglist(self.rules_data_sequence_column, ""))
        
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process rules_data
        if self.rules_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.rules_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("rules")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.rules_data_order_column, "\""))
        
        function_name = "TextTagger"
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
        Returns the string representation for a TextTagger class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
