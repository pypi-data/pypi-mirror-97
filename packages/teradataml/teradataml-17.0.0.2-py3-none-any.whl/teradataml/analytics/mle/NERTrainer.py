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

class NERTrainer:
    
    def __init__(self,
                 data=None,
                 text_coloumn=None,
                 extractor_jar=None,
                 feature_template=None,
                 model_file=None,
                 language="en",
                 max_iter_num=1000,
                 eta=1.0E-4,
                 min_occur_num=0,
                 data_sequence_column=None):
        """
        DESCRIPTION:
            The NERTrainer function takes training data and outputs a CRF model
            (a binary file) that can be specified in the function NERExtractor
            and NEREvaluator.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies an input teradataml DataFrame containing training data.
         
            text_coloumn:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the text to analyze.
                Types: str
         
            extractor_jar:
                Optional Argument.
                Specifies the name of the JAR file that contains the Java classes
                that extract features. The function includes the predefined extractor
                classes described in the file provided in the argument feature_template.
                Note:
                    1. The name of the JAR file is case-sensitive.
                    2. The ML Engine does not support the creation of new extractor classes.
                       However, it does support existing JAR files—for installation instructions,
                       see Teradata Vantage User Guide.
                Types: str
         
            feature_template:
                Required Argument.
                Specifies the name of the file that specifies how to generate
                features when training the model. This file is pre-installed
                in ML Engine under the name "template_1.txt".
                Types: str
         
            model_file:
                Required Argument.
                Specifies the name of the model file that is generated and installed
                in the ML Engine by the function.
                Types: str
         
            language:
                Optional Argument.
                Specifies the language of the input text:
                    * en - English
                    * zh_CN - Simplified Chinese
                    * zh_TW - Traditional Chinese
                Default Value: "en"
                Permitted Values: en, zh_CN, zh_TW
                Types: str
         
            max_iter_num:
                Optional Argument.
                Specifies the maximum number of iterations.
                Types: int
         
            eta:
                Optional Argument.
                Specifies the tolerance of the termination criterion. Defines the
                differences of the values of the loss function between two sequential
                epochs. When training a model, the function performs n-times
                iterations. At the end of each epoch, the function calculates the
                loss or cost function on the training samples. If the loss function
                value change is very small between two sequential epochs, the
                function considers the training process to have converged.
                The function defines eta as:
                    Eta=(f(n)-f(n-1))/f(n-1), where f(n) is the loss function value of the nth epoch.
                Default Value: 1.0E-4
                Types: float
         
            min_occur_num:
                Optional Argument.
                Specifies the minimum number of times that a feature must occur in the
                input text before the function uses the feature to construct the
                model.
                Default Value: 0
                Types: int
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of NERTrainer.
            Output teradataml DataFrames can be accessed using attribute
            references, such as NERTrainerObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example
            load_example_data("nertrainer","ner_sports_train")
         
            # Create teradataml DataFrame object.
            ner_sports_train = DataFrame.from_table("ner_sports_train")
         
            # Run the NERTrain function to generated a trained model file which is used in NERExtractor or NEREvaluator
            nertrainer_train = NERTrainer(data=ner_sports_train,
                                          text_coloumn='content',
                                          model_file='ner_model.bin',
                                          feature_template='template_1.txt',
                                          language='en',
                                          eta=0.0001,
                                          max_iter_num=1000,
                                          min_occur_num=0,
                                          extractor_jar=' ')
         
            # Print the result DataFrame
            print(nertrainer_train.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.text_coloumn  = text_coloumn 
        self.extractor_jar  = extractor_jar 
        self.feature_template  = feature_template 
        self.model_file  = model_file 
        self.language  = language 
        self.max_iter_num  = max_iter_num 
        self.eta  = eta 
        self.min_occur_num  = min_occur_num 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["text_coloumn", self.text_coloumn, False, (str)])
        self.__arg_info_matrix.append(["extractor_jar", self.extractor_jar, True, (str)])
        self.__arg_info_matrix.append(["feature_template", self.feature_template, False, (str)])
        self.__arg_info_matrix.append(["model_file", self.model_file, False, (str)])
        self.__arg_info_matrix.append(["language", self.language, True, (str)])
        self.__arg_info_matrix.append(["max_iter_num", self.max_iter_num, True, (int)])
        self.__arg_info_matrix.append(["eta", self.eta, True, (float)])
        self.__arg_info_matrix.append(["min_occur_num", self.min_occur_num, True, (int)])
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
        language_permitted_values = ["EN", "ZH_CN", "ZH_TW"]
        self.__awu._validate_permitted_values(self.language, language_permitted_values, "language")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.text_coloumn, "text_coloumn")
        self.__awu._validate_dataframe_has_argument_columns(self.text_coloumn, "text_coloumn", self.data, "data", False)
        
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
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.text_coloumn, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")

        self.__func_other_arg_sql_names.append("ModelFileName")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.model_file, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("FeatureTemplate")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.feature_template, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.language is not None and self.language != "en":
            self.__func_other_arg_sql_names.append("InputLanguage")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.language, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.eta is not None and self.eta != 1.0E-4:
            self.__func_other_arg_sql_names.append("Eta")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.eta, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.max_iter_num is not None and self.max_iter_num != 1000:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_iter_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.min_occur_num is not None and self.min_occur_num != 0:
            self.__func_other_arg_sql_names.append("MinOccurNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.min_occur_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.extractor_jar is not None:
            self.__func_other_arg_sql_names.append("ExtractorJar")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.extractor_jar, "'"))
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("1")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "NERTrainer"
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
        Returns the string representation for a NERTrainer class instance.
        """
        repr_string = "############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string, self.result)
        return repr_string

