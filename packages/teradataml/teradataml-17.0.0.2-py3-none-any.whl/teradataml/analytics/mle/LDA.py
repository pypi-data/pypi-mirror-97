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
# Function Version: 1.10
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

class LDA:
    
    def __init__(self,
        data = None,
        topic_num = None,
        docid_column = None,
        word_column = None,
        alpha = 0.1,
        eta = 0.1,
        count_column = None,
        maxiter = 50,
        convergence_delta = 1.0E-4,
        seed = None,
        out_topicnum = "all",
        out_topicwordnum = "none",
        initmodeltaskcount = None,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The LDA function uses training data and parameters to build a
            topic model, using an unsupervised method to estimate the correlation
            between the topics and words according to the topic number and other
            parameters. Optionally, the function generates the topic distributions
            for each training document. The function uses an iterative algorithm;
            therefore, applying it to large data sets with a large number of
            topics can be time-consuming.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame or view that contains
                the new documents.
            
            topic_num:
                Required Argument.
                Specifies the number of topics for all the documents in the
                teradataml DataFrame 'data', an int value in the range [2, 1000].
                Types: int
            
            docid_column:
                Required Argument.
                Specifies the name of the input column that contains the document
                identifiers.
                Types: str OR list of Strings (str)
            
            word_column:
                Required Argument.
                Specifies the name of the input column that contains the words (one
                word in each row).
                Types: str OR list of Strings (str)
            
            alpha:
                Optional Argument.
                Specifies a hyperparameter of the model, the prior smooth parameter
                for the topic distribution over documents. As alpha decreases,
                fewer topics are associated with each document.
                Default Value: 0.1
                Types: float
            
            eta:
                Optional Argument.
                Specifies a hyperparameter of the model, the prior smooth parameter
                for the word distribution over topics. As eta decreases, fewer
                words are associated with each topic.
                Default Value: 0.1
                Types: float
            
            count_column:
                Optional Argument.
                Specifies the name of the input column that contains the count
                 of the corresponding word in the row, a NUMERIC value.
                Types: str OR list of Strings (str)
            
            maxiter:
                Optional Argument.
                Specifies the maximum number of iterations to perform if the
                model does not converge, a positive int value.
                Default Value: 50
                Types: int
            
            convergence_delta:
                Optional Argument.
                Specifies the convergence delta of log perplexity, a NUMERIC
                value in the range [0.0,1.0].
                Default Value: 1.0E-4
                Types: float
            
            seed:
                Optional Argument.
                Specifies the seed with which to initialize the model, a int value.
                Given the same seed, cluster configuration, and data, the
                function generates the same model. By default, the function
                initializes the model randomly.
                Types: int
            
            out_topicnum:
                Optional Argument.
                Specifies the number of top-weighted topics and their weights to
                include in the output teradataml DataFrame for each training
                document. The value out_topicnum must be a positive int. The value,
                "all", specifies all topics and their weights.
                Default Value: "all"
                Types: str
            
            out_topicwordnum:
                Optional Argument.
                Specifies the number of top topic words and their topic identifiers
                to include in the output teradataml DataFrame for each training
                document. The value out_topicwordnum must be a positive int.
                The value "all" specifies all topic words and their topic
                identifiers. The value, "none", specifies no topic words or
                topic identifiers.
                Default Value: "none"
                Types: str
            
            initmodeltaskcount:
                Optional Argument.
                Specifies the number of vWorkers that are adopted to generate
                initialized model. By default, the function uses all the available
                vworkers to initialize the model.
                Note: This argument is available only when teradataml is connected to
                      Vantage 1.1.1 or later versions.
                Types: int
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of LDA.
            Output teradataml DataFrames can be accessed using attribute
            references, such as LDAObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_table
                2. doc_distribution_data
                3. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("LDA", "complaints_traintoken")
         
            # Create teradataml DataFrame objects.
            # The training table is log of vehicle complaints. The 'category'
            # column indicates whether the car has been in a crash.
            complaints_traintoken = DataFrame.from_table("complaints_traintoken")
         
            # Example 1 - Function uses training data and parameters to build a topic model.
            LDA_out = LDA(data = complaints_traintoken,
                                        topic_num = 5,
                                        docid_column = "doc_id",
                                        word_column = "token",
                                        count_column = "frequency",
                                        maxiter = 30,
                                        convergence_delta = 1e-3,
                                        seed = 2
                                        )
         
            # Print the result teradataml DataFrame
            print(LDA_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.topic_num  = topic_num 
        self.docid_column  = docid_column 
        self.word_column  = word_column 
        self.alpha  = alpha 
        self.eta  = eta 
        self.count_column  = count_column 
        self.maxiter  = maxiter 
        self.convergence_delta  = convergence_delta 
        self.seed  = seed 
        self.out_topicnum  = out_topicnum 
        self.out_topicwordnum  = out_topicwordnum 
        self.initmodeltaskcount  = initmodeltaskcount 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["topic_num", self.topic_num, False, (int)])
        self.__arg_info_matrix.append(["docid_column", self.docid_column, False, (str)])
        self.__arg_info_matrix.append(["word_column", self.word_column, False, (str)])
        self.__arg_info_matrix.append(["alpha", self.alpha, True, (float)])
        self.__arg_info_matrix.append(["eta", self.eta, True, (float)])
        self.__arg_info_matrix.append(["count_column", self.count_column, True, (str)])
        self.__arg_info_matrix.append(["maxiter", self.maxiter, True, (int)])
        self.__arg_info_matrix.append(["convergence_delta", self.convergence_delta, True, (float)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["out_topicnum", self.out_topicnum, True, (str)])
        self.__arg_info_matrix.append(["out_topicwordnum", self.out_topicwordnum, True, (str)])
        self.__arg_info_matrix.append(["initmodeltaskcount", self.initmodeltaskcount, True, (int)])
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
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.docid_column, "docid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.docid_column, "docid_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.word_column, "word_column")
        self.__awu._validate_dataframe_has_argument_columns(self.word_column, "word_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.count_column, "count_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_column, "count_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)

        if self.initmodeltaskcount is not None and self.initmodeltaskcount < 1:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT, "initmodeltaskcount",
                                                           "greater than"), MessageCodes.TDMLDF_POSITIVE_INT)
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_lda0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__doc_distribution_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_lda1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["ModelTable", "OutputTable"]
        self.__func_output_args = [self.__model_table_temp_tablename, self.__doc_distribution_data_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("DocIDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.docid_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("WordColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.word_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.count_column is not None:
            self.__func_other_arg_sql_names.append("CountColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.count_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("TopicNum")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.topic_num, "'"))
        self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.alpha is not None and self.alpha != 0.1:
            self.__func_other_arg_sql_names.append("Alpha")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.alpha, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.eta is not None and self.eta != 0.1:
            self.__func_other_arg_sql_names.append("Eta")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.eta, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.maxiter is not None and self.maxiter != 50:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.maxiter, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.convergence_delta is not None and self.convergence_delta != 1.0E-4:
            self.__func_other_arg_sql_names.append("ConvergenceDelta")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.convergence_delta, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.initmodeltaskcount is not None:
            self.__func_other_arg_sql_names.append("InitModelTaskCount")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.initmodeltaskcount, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.out_topicnum is not None and self.out_topicnum != "all":
            self.__func_other_arg_sql_names.append("OutputTopicNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.out_topicnum, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.out_topicwordnum is not None and self.out_topicwordnum != "none":
            self.__func_other_arg_sql_names.append("OutputTopicWordNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.out_topicwordnum, "'"))
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
        
        function_name = "LDA"
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
        self.model_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__model_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__model_table_temp_tablename))
        self.doc_distribution_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__doc_distribution_data_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__doc_distribution_data_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_table)
        self._mlresults.append(self.doc_distribution_data)
        self._mlresults.append(self.output)
        
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
        model_table = None,
        doc_distribution_data = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_table", None)
        kwargs.pop("doc_distribution_data", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_table  = model_table 
        obj.doc_distribution_data  = doc_distribution_data 
        obj.output  = output 
        
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
        obj.model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.model_table))
        obj.doc_distribution_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.doc_distribution_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.doc_distribution_data))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        obj._mlresults.append(obj.doc_distribution_data)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a LDA class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        repr_string="{}\n\n\n############ doc_distribution_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.doc_distribution_data)
        return repr_string
        
