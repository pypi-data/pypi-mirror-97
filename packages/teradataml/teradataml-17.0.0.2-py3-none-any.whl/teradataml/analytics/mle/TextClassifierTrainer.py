#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# 
# Version: 1.2
# Function Version: 1.20
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
from teradataml.options.configure import configure
from teradataml.options.display import display

class TextClassifierTrainer:
    
    def __init__(self,
        data = None,
        text_column = None,
        category_column = None,
        classifier_type = 'maxEnt',
        classifier_parameters = None,
        nlp_parameters = None,
        feature_selection = None,
        model_file = None,
        data_sequence_column = None,
        to_lower_case=True,
        punctuation=None):
        """
        DESCRIPTION:
            The TextClassifierTrainer function trains a machine-learning
            classifier for text classification and installs the model file on
            the ML Engine. The model file can then be input to the function
            TextClassifier.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the
                documents to use to train the model.
         
            text_column:
                Required Argument.
                Specifies the name of the column that contains the text of the
                training documents.
                Types: str
         
            category_column:
                Required Argument.
                Specifies the name of the column that contains the category of
                the training documents.
                Types: str
         
            classifier_type:
                Optional Argument.
                Specifies the classifier type of the model, KNN algorithm or
                maximum entropy model.
                Default Value: "maxEnt"
                Permitted Values: maxEnt, knn
                Types: str
         
            classifier_parameters:
                Optional Argument.
                Applies only if the classifier type of the model is KNN.
                Specifies parameters for the classifier.
                Permitted Values:
                    * compress: The value must be in the range (0, 1). The n
                                training documents are clustered into value*n
                                groups and the model uses the center of each group as
                                the feature vector.
                                For example,
                                if there are 100 training documents, then
                                classifier_parameters ("compress:0.6") clusters
                                them into 60 groups.
                    * kvalues: The value must be int value in range
                               [1, max(classes, ceil(sqrt(rows)))],
                               where:
                               * 'classes' is number of classes in "data" teradataml
                                 Dataframe.
                               * 'rows' is number of rows in "data" teradataml
                                 Dataframe.
                               Value specifies number of nearest neighbors to
                               consider when deciding label of unseen document.
                               Function selects best specified value for deciding
                               label of unseen document.
                    * power: The value must be int value in range [0, 10]. The
                             value specifies power to apply to weight corresponding
                             to each vote considered when deciding label of unseen
                             document.
                Note:
                    All above listed parameter values can be used when teradataml
                    is connected to Vantage 1.3, otherwise only 'compress' value
                    is supported.
                Types: str OR list of strs
         
            nlp_parameters:
                Optional Argument.
                Specifies natural language processing (NLP) parameters for
                preprocessing the text data and produce tokens:
                    * tokenDictFile: token_file  - token_file is name of ML
                      Engine file in which each line contains a phrase, followed
                      by a space, followed by the token for the phrase (and
                      nothing else).
                    * stopwordsFile:stopword_file - stopword_file is the name
                      of an ML Engine file in which each line contains
                      exactly one stop word (a word to ignore during tokenization,
                      such as a, an, or the).
                    * useStem:{true|false} - Specifies whether the function
                      stems the tokens. The default value is "false".
                    * stemIgnoreFile:stem_ignore_file - stem_ignore_file is
                      the name of an ML Engine file in which each line
                      contains exactly one word to ignore during stemming.
                      Specifying this parameter with "useStem:false" causes an
                      exception.
                    * useBgram:{ true | false } - Specifies whether the function
                      uses Bigram, which considers the proximity of adjacent
                      tokens when analyzing them. The default value is "false".
                    * language:{ en | zh_CN | zh_TW } - Specifies the language
                      of the input text - English (en), Simplified Chinese (zh_CN),
                      or Traditional Chinese (zh_TW). The default value is en.
                      For the values zh_CN and zh_TW, the function ignores the
                      parameters useStem and stemIgnoreFile.
                Example: nlp_parameters("tokenDictFile:token_dict.txt",
                                        "stopwordsFile:fileName",
                                        "useStem:true",
                                        "stemIgnoreFile:fileName",
                                        "useBgram:true", "language:zh_CN")
                Types: str OR list of strs
         
            feature_selection:
                Optional Argument.
                Specifies the feature selection method, DF (document frequency).
                The values min and max must be in the range (0, 1). The function
                selects only the tokens that appear in at least min*n documents
                and at most max*n documents, where n is the number of training
                documents. For example, FeatureSelection ("DF:[0.1:0.9]") causes
                the function to select only the tokens that appear in at least
                10% but no more than 90% of the training documents. If min
                exceeds max, the function uses min as max and max as min.
                Types: str
         
            model_file:
                Required Argument.
                Specifies the name of the model file to be generated.
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            to_lower_case:
                Optional Argument.
                Specifies whether to convert input text to lowercase.
                Note:
                    "to_lower_case" argument support is only available when teradataml
                    is connected to Vantage 1.3 version.
                Default Value: True
                Types: bool

            punctuation:
                Optional Argument.
                Specifies a regular expression that represents the punctuation
                characters to remove from the input text.
                Note:
                    "punctuation" argument support is only available when teradataml
                    is connected to Vantage 1.3 version.
                Types: str

        RETURNS:
            Instance of TextClassifierTrainer.
            Output teradataml DataFrames can be accessed using attribute
            references, such as TextClassifierTrainerObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException, TypeError, ValueError
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("textclassifiertrainer", "texttrainer_input")
         
            # Create teradataml DataFrame objects.
            # The input table contains text of the training documents and the
            # category of the training documents.
            texttrainer_input = DataFrame.from_table("texttrainer_input")
         
            # Example 1 - The function outputs a binary file with the name
            # specified by "model_file" argument.
            TextClassifierTrainer_out1 = TextClassifierTrainer(data = texttrainer_input,
                                                              text_column = "content",
                                                              category_column = "category",
                                                              classifier_type = "knn",
                                                              classifier_parameters = ["compress:0.9"],
                                                              nlp_parameters = ["useStem:true", "stopwordsFile: stopwords.txt"],
                                                              feature_selection = "DF:[0.1:0.99]",
                                                              model_file = "knn.bin"
                                                              )
         
            # Print the result teradataml DataFrame
            print(TextClassifierTrainer_out1)

            # Example 2 - This example uses parameters 'kvalues' and 'power' as input
            # to argument "classifier_parameters" and outputs a binary file with the name
            # specified by "model_file" argument.
            # Note:
            #     This Example will work only when teradataml is connected
            #     to Vantage 1.3 or later.
            TextClassifierTrainer_out2 = TextClassifierTrainer(data = texttrainer_input,
                                                              text_column = "content",
                                                              category_column = "category",
                                                              classifier_type = "knn",
                                                              classifier_parameters = ["compress:0.9", "kvalues:{1,3}", "power:2"],
                                                              nlp_parameters = ["useStem:true", "stopwordsFile: stopwords.txt"],
                                                              feature_selection = "DF:[0.1:0.99]",
                                                              model_file = "knn.bin",
                                                              to_lower_case=False,
                                                              punctuation='[a-z]'
                                                              )

            # Print the result teradataml DataFrame
            print(TextClassifierTrainer_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.text_column  = text_column 
        self.category_column  = category_column 
        self.classifier_type  = classifier_type 
        self.classifier_parameters  = classifier_parameters 
        self.nlp_parameters  = nlp_parameters 
        self.feature_selection  = feature_selection 
        self.model_file  = model_file
        self.data_sequence_column  = data_sequence_column
        self.to_lower_case = to_lower_case
        self.punctuation = punctuation

        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["text_column", self.text_column, False, (str)])
        self.__arg_info_matrix.append(["category_column", self.category_column, False, (str)])
        self.__arg_info_matrix.append(["classifier_type", self.classifier_type, True, (str)])
        self.__arg_info_matrix.append(["classifier_parameters", self.classifier_parameters, True, (str,list)])
        self.__arg_info_matrix.append(["nlp_parameters", self.nlp_parameters, True, (str,list)])
        self.__arg_info_matrix.append(["feature_selection", self.feature_selection, True, (str)])
        self.__arg_info_matrix.append(["model_file", self.model_file, False, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["to_lower_case", self.to_lower_case, True, (bool)])
        self.__arg_info_matrix.append(["punctuation", self.punctuation, True, (str)])
        
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
        classifier_type_permitted_values = ["MAXENT", "KNN"]
        self.__awu._validate_permitted_values(self.classifier_type, classifier_type_permitted_values, "classifier_type")

        # Check for permitted values for argument classifier_parameters.
        if self.classifier_parameters is not None:
            __classifier_parameters = self.classifier_parameters
            classifier_parameters_permitted_values = ["compress"]
            if configure._vantage_version == "vantage1.3":
                classifier_parameters_permitted_values.extend(["kvalues", "power"])

            if isinstance(__classifier_parameters, str):
                __classifier_parameters = [__classifier_parameters]

            # Check for parameters supported or not.
            for __classifier_parameter in __classifier_parameters:
                __parameter = __classifier_parameter.split(":")[0]
                self.__awu._validate_permitted_values(__parameter, classifier_parameters_permitted_values, "classifier_parameters")

        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.text_column, "text_column")
        self.__awu._validate_dataframe_has_argument_columns(self.text_column, "text_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.category_column, "category_column")
        self.__awu._validate_dataframe_has_argument_columns(self.category_column, "category_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
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
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("CategoryColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.category_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        self.__func_other_arg_sql_names.append("ClassifierType")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.classifier_type, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("ModelFile")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model_file, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.classifier_parameters is not None:
            self.__func_other_arg_sql_names.append("ClassifierParameters")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.classifier_parameters, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.nlp_parameters is not None:
            self.__func_other_arg_sql_names.append("NlpParameters")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.nlp_parameters, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.feature_selection is not None:
            self.__func_other_arg_sql_names.append("FeatureSelectionMethod")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.feature_selection, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.to_lower_case is not None and self.to_lower_case != True:
            self.__func_other_arg_sql_names.append("ConvertToLowerCase")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.to_lower_case, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.punctuation is not None:
            self.__func_other_arg_sql_names.append("Punctuation")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.punctuation, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "TextClassifierTrainer"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        try:
            # Generate the output.
            UtilFuncs._create_table(sqlmr_stdout_temp_tablename, self.sqlmr_query)
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
        Returns the string representation for a TextClassifierTrainer class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
