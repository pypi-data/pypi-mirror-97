#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Khurd (rohit.khurd@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 2.3
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
from teradataml.analytics.mle.TF import TF

class TFIDF:
    
    def __init__(self,
        object = None,
        doccount_data = None,
        docperterm_data = None,
        idf_data = None,
        object_partition_column = None,
        docperterm_data_partition_column = None,
        idf_data_partition_column = None,
        object_order_column = None,
        doccount_data_order_column = None,
        docperterm_data_order_column = None,
        idf_data_order_column = None):
        """
        DESCRIPTION:
            TF-IDF stands for "term frequency-inverse document frequency", a
            technique for evaluating the importance of a specific term in a
            specific document in a document set. Term frequency (tf) is the
            number of times that the term appears in the document and inverse
            document frequency (idf) is the number of times that the term appears
            in the document set. The TF-IDF score for a term is tf * idf. A term
            with a high TF-IDF score is especially relevant to the specific
            document.

            The TFIDF function can do either of the following:
            • Take any document set and output the inverse document frequency (IDF)
              and term frequency - inverse document frequency (TF-IDF) scores
              for each term.
            • Use the output of a previous run of the TFIDF function on a
              training document set to predict TF-IDF scores of an input (test)
              document set.


        PARAMETERS:
            object:
                Required Argument.
                Specifies the teradataml DataFrame that contains the tf values
                or instance of TF.

            object_partition_column:
                Required Argument.
                Specifies Partition By columns for object.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)

            object_order_column:
                Optional Argument.
                Specifies Order By columns for object.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            doccount_data:
                Optional Argument.
                Required if running the function to output IDF and TF-IDF score
                for each term in the document set.
                Specifies the teradataml DataFrame that contains the total
                number of documents.

            doccount_data_order_column:
                Optional Argument.
                Specifies Order By columns for doccount_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            docperterm_data:
                Optional if running the function to output IDF and TF-IDF values
                for each term in the document set.
                Specifies the teradataml DataFrame that contains the total
                number of documents that each term appears in.
                If you omit this input, the function creates it by processing the
                entire document set, which can require a large amount of memory.
                If there is not enough memory to process the entire document set,
                then the docperterm teradataml DataFrame is required.

            docperterm_data_partition_column:
                Optional Argument.
                Required when the docperterm_data teradataml DataFrame is used.
                Specifies Partition By columns for docperterm_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)

            docperterm_data_order_column:
                Optional Argument.
                Specifies Order By columns for docperterm_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            idf_data:
                Optional Argument.
                Required if running the function to predict TF-IDF scores.
                Specifies the teradataml DataFrame that contains the idf values
                that the predict process outputs.

            idf_data_partition_column:
                Optional Argument.
                Required when the idf_data teradataml DataFrame is used.
                Specifies Partition By columns for idf_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for partition.
                Types: str OR list of Strings (str)

            idf_data_order_column:
                Optional Argument.
                Specifies Order By columns for idf_data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of TFIDF.
            Output teradataml DataFrames can be accessed using attribute
            references, such as TFIDFObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load the data to run the example.
            load_example_data("TFIDF", ["tfidf_train", "idf_table", "docperterm_table"])

            # Create teradataml DataFrame.
            tfidf_train = DataFrame.from_table("tfidf_train")
            idf_tbl =  DataFrame.from_table("idf_table")
            docperterm_table = DataFrame.from_table("docperterm_table")

            # Create Tokenized Training Document Set
            ngrams_out = NGrams(data=tfidf_train,
                                text_column='content',
                                delimiter = " ",
                                grams = "1",
                                overlapping = False,
                                punctuation = "\\\\[.,?\\\\!\\\\]",
                                reset = "\\\\[.,?\\\\!\\\\]",
                                to_lower_case=True,
                                total_gram_count=True,
                                accumulate="docid")

            # store the output of td_ngrams functions into a table.
            tfidf_input_tbl = copy_to_sql(ngrams_out.result, table_name="tfidf_input_table")

            tfidf_input = DataFrame.from_query('select docid, ngram as term, frequency as "count" from tfidf_input_table')

            # create doccount table that contains the total number of documents
            doccount_tbl = DataFrame.from_query("select cast(count(distinct(docid)) as integer) as \"count\" from tfidf_input_table")

            # Run TF function to create Input for TFIDF Function
            tf_out = TF (data = tfidf_input,
                         formula = "normal",
                         data_partition_column = "docid")

            # Example 1 -
            tfidf_result1 = TFIDF(object = tf_out,
                                  doccount_data = doccount_tbl,
                                  object_partition_column = 'term')

            # Print the result DataFrame
            print(tfidf_result1.result)

            # Example 2 -
            tfidf_result2 = TFIDF(object = tf_out,
                                  docperterm_data = docperterm_table,
                                  idf_data = idf_tbl,
                                  object_partition_column = 'term',
                                  docperterm_data_partition_column = 'term',
                                  idf_data_partition_column = 'token')

            # Print the result DataFrame
            print(tfidf_result2.result)

        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.doccount_data  = doccount_data 
        self.docperterm_data  = docperterm_data 
        self.idf_data  = idf_data 
        self.object_partition_column  = object_partition_column 
        self.docperterm_data_partition_column  = docperterm_data_partition_column 
        self.idf_data_partition_column  = idf_data_partition_column 
        self.object_order_column  = object_order_column 
        self.doccount_data_order_column  = doccount_data_order_column 
        self.docperterm_data_order_column  = docperterm_data_order_column 
        self.idf_data_order_column  = idf_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["object_partition_column", self.object_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["object_order_column", self.object_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["doccount_data", self.doccount_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["doccount_data_order_column", self.doccount_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["docperterm_data", self.docperterm_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["docperterm_data_partition_column", self.docperterm_data_partition_column, self.docperterm_data is None, (str,list)])
        self.__arg_info_matrix.append(["docperterm_data_order_column", self.docperterm_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["idf_data", self.idf_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["idf_data_partition_column", self.idf_data_partition_column, self.idf_data is None, (str,list)])
        self.__arg_info_matrix.append(["idf_data_order_column", self.idf_data_order_column, True, (str,list)])
        
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
        if isinstance(self.object, TF):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.object, "object", TF)
        self.__awu._validate_input_table_datatype(self.doccount_data, "doccount_data", None)
        self.__awu._validate_input_table_datatype(self.docperterm_data, "docperterm_data", None)
        self.__awu._validate_input_table_datatype(self.idf_data, "idf_data", None)
        
        self.__awu._validate_input_columns_not_empty(self.object_partition_column, "object_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_partition_column, "object_partition_column", self.object, "object", True)
        
        self.__awu._validate_input_columns_not_empty(self.docperterm_data_partition_column, "docperterm_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.docperterm_data_partition_column, "docperterm_data_partition_column", self.docperterm_data, "docperterm_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.idf_data_partition_column, "idf_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.idf_data_partition_column, "idf_data_partition_column", self.idf_data, "idf_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.object_order_column, "object_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_order_column, "object_order_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.doccount_data_order_column, "doccount_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.doccount_data_order_column, "doccount_data_order_column", self.doccount_data, "doccount_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.docperterm_data_order_column, "docperterm_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.docperterm_data_order_column, "docperterm_data_order_column", self.docperterm_data, "docperterm_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.idf_data_order_column, "idf_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.idf_data_order_column, "idf_data_order_column", self.idf_data, "idf_data", False)
        
        
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
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process object
        self.object_partition_column = UtilFuncs._teradata_collapse_arglist(self.object_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("tf")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.object_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.object_order_column, "\""))
        
        # Process doccount_data
        if self.doccount_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.doccount_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("doccount")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.doccount_data_order_column, "\""))

        # Process docperterm_data
        if self.docperterm_data is not None:
            self.docperterm_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.docperterm_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.docperterm_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("docperterm")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.docperterm_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.docperterm_data_order_column, "\""))
        
        # Process idf_data
        if self.idf_data is not None:
            self.idf_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.idf_data_partition_column, "\"")
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.idf_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("idf")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.idf_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.idf_data_order_column, "\""))
        
        function_name = "TFIDF"
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
        Returns the string representation for a TFIDF class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
