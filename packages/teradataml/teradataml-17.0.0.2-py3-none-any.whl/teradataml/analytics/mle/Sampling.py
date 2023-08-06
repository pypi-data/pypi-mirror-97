#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.5
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

class Sampling:
    
    def __init__(self,
        data = None,
        summary_data = None,
        stratum_column = None,
        strata = None,
        sample_fraction = None,
        approx_sample_size = None,
        seed = 0,
        data_sequence_column = None,
        summary_data_sequence_column = None,
        data_partition_column = "ANY",
        data_order_column = None,
        summary_data_order_column = None):
        """
        DESCRIPTION:
            The Sample function draws rows randomly from the teradataml DataFrame.
            The function offers two sampling schemes:
                • A simple Bernoulli (Binomial) sampling on a row-by-row basis
                  with given sample rates
                • Sampling without replacement that selects a given number of
                  rows.
            Sampling can be either unconditional or conditional. Unconditional
            sampling applies to all input data and always uses the same random
            number generator. Conditional sampling applies only to input data
            that meets specified conditions and uses a dierent random number
            generator for each condition.
         
            Note: The Sampling function does not guarantee the exact sizes of
                  samples. If each sample must have an exact number of rows, use the
                  RandomSample function.
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the teradataml DataFrame containing the data to be
                sampled.
         
            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as list, if multiple
                columns are used for partition.
                Default Value: ANY
                Types: str OR list of Strings (str)
         
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            summary_data:
                Optional Argument.
                Specifies the teradataml DataFrame containing the stratum count
                information.
                Note: summary_data argument is only available when teradataml is
                      connected to Vantage 1.1 or later versions.
         
            summary_data_order_column:
                Optional Argument.
                Specifies Order By columns for summary_data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            stratum_column:
                Optional Argument.
                Specifies the name of the column that contains the sample conditions.
                If the function has only one input teradataml DataFrame (data),
                then condition column is in the data teradataml DataFrame. If the function
                has two input teradataml DataFrames, data and summary_data, then
                condition column is in the summary_data teradataml DataFrame.
                Types: str
         
            strata:
                Optional Argument.
                Specifies the sample conditions that appear in the stratum_column.
                If strata specifies a condition that does not appear in
                stratum_column, then the function issues an error message.
                Types: str or list of Strings (str)
         
            sample_fraction:
                Optional Argument.
                Specifies one or more fractions to use in sampling the data .
                (Syntax options that do not use sample_fraction require
                approx_sample_size.)
                If you specify only one fraction, then the function uses fraction
                for all strata defined by the sample conditions. If you specify
                more than one fraction, then the function uses each fraction for
                sampling a particular stratum defined by the condition arguments.
                Note: For conditional sampling with variable sample sizes,
                      specify one fraction for each condition that you specify with
                      the strata argument.
                Types: float or list of Floats (float)
         
            approx_sample_size:
                Optional Argument.
                Specifies one or more approximate sample sizes to use in sampling the
                data (syntax options that do not use approx_sample_size require
                sample_fraction). Each sample size is approximate because the
                function maps the size to the sample fractions and then generates the
                sample data. If you specify only one size, then it represents the
                total sample size for the entire population. If you also specify the
                strata argument, then the function proportionally generates sample
                units for each stratum. If you specify more than one size, then each
                size corresponds to a stratum, and the function uses each size to
                generate sample units for the corresponding stratum.
                Note: For conditional sampling with variable approximate sample
                      sizes, specify one size for each condition that you specify with
                      the strata argument.
                Types: int or list of Integers (int)
         
            seed:
                Optional Argument.
                Specifies the random seed used to initialize the algorithm.
                Default Value: 0
                Types: int
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            summary_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "summary_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Sampling.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SamplingObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("Sampling", ["students","score_category","score_summary"])
         
            # Create teradataml DataFrame objects.
            # The input table "score_category" is obtained by categorizing the
            # students in the "students" table based on their score in a given
            # subject. There are 100 students grouped into three categories -
            # excellent (score > 90), very good (80 < score < 90) and fair
            # (score < 80). The table "score_summary" groups the score_category
            # table based on the stratum column and also has their corresponding
            # count.
         
            students = DataFrame.from_table("students")
            score_category = DataFrame.from_table("score_category")
            score_summary = DataFrame.from_table("score_summary")
         
            # Example 1 - This example selects a sample of approximately 20%
            # of the rows in the student table.
            sampling_out1 = Sampling(data = students,
                                     sample_fraction = 0.2,
                                     seed = 2
                                     )
         
            # Print the result teradataml DataFrame
            print(sampling_out1)
         
            # Example 2 - This example applies sampling rates 20%, 30%, and 40%
            # to categories fair, very good, and excellent, respectively, and
            # rounds the number sampled to the nearest integer.
            sampling_out2 = Sampling(data = score_category,
                                      data_partition_column = "stratum",
                                      stratum_column = "stratum",
                                      strata = ["fair", "very good", "excellent"],
                                      sample_fraction = [0.2, 0.3, 0.4],
                                      seed = 2
                                      )
         
            # Print the result teradataml DataFrame
            print(sampling_out2.result)
         
            # Example 3 - This examples demonstrates conditional sampling with
            # Approximate Sample Size.
            sampling_out3 = Sampling(data=score_category,
                                   summary_data=score_summary,
                                   stratum_column='stratum',
                                   strata=['excellent','fair','very good'],
                                   approx_sample_size=[5,10,5],
                                   seed=2
                                  )
            # Print the result teradataml DataFrame
            print(sampling_out3.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.summary_data  = summary_data 
        self.stratum_column  = stratum_column 
        self.strata  = strata 
        self.sample_fraction  = sample_fraction 
        self.approx_sample_size  = approx_sample_size 
        self.seed  = seed 
        self.data_sequence_column  = data_sequence_column 
        self.summary_data_sequence_column  = summary_data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        self.summary_data_order_column  = summary_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["summary_data", self.summary_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["summary_data_order_column", self.summary_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["stratum_column", self.stratum_column, True, (str)])
        self.__arg_info_matrix.append(["strata", self.strata, True, (str,list)])
        self.__arg_info_matrix.append(["sample_fraction", self.sample_fraction, True, (float,list)])
        self.__arg_info_matrix.append(["approx_sample_size", self.approx_sample_size, True, (int,list)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["summary_data_sequence_column", self.summary_data_sequence_column, True, (str,list)])
        
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
        # Make sure that either sample.fraction or approx.sample.size is provided
        if ((self.sample_fraction is None and self.approx_sample_size is None) or
                (self.sample_fraction is not None and self.approx_sample_size is not None)):
            raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT,
                                                           "sample_fraction", "approx_sample_size"),
                                      MessageCodes.MISSING_ARGS)
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        self.__awu._validate_input_table_datatype(self.summary_data, "summary_data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.stratum_column, "stratum_column")
        self.__awu._validate_dataframe_has_argument_columns(self.stratum_column, "stratum_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.summary_data_sequence_column, "summary_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.summary_data_sequence_column, "summary_data_sequence_column", self.summary_data, "summary_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
            self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.summary_data_order_column, "summary_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.summary_data_order_column, "summary_data_order_column", self.summary_data, "summary_data", False)
        
        
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
        
        if self.stratum_column is not None:
            self.__func_other_arg_sql_names.append("StratumColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.stratum_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.sample_fraction is not None:
            self.__func_other_arg_sql_names.append("SampleFraction")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.sample_fraction, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.approx_sample_size is not None:
            self.__func_other_arg_sql_names.append("ApproxSampleSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.approx_sample_size, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.strata is not None:
            self.__func_other_arg_sql_names.append("Strata")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.strata, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.seed is not None and self.seed != 0:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.summary_data_sequence_column is not None:
            sequence_input_by_list.append("SummaryTable :" + UtilFuncs._teradata_collapse_arglist(self.summary_data_sequence_column, ""))
        
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
        if self.__awu._is_default_or_not(self.data_partition_column, "ANY"):
            self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column, "\"")
        
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        # Process summary_data
        if self.summary_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.summary_data, False)
            self.__func_input_distribution.append("DIMENSION")
            self.__func_input_arg_sql_names.append("SummaryTable ")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.summary_data_order_column, "\""))
        
        function_name = "Sampling"
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
        Returns the string representation for a Sampling class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
