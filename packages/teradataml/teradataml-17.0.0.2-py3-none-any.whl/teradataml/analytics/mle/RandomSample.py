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

class RandomSample:
    
    def __init__(self,
        data = None,
        num_sample = None,
        weight_column = None,
        sampling_mode = "Basic",
        distance = "EUCLIDEAN",
        input_columns = None,
        as_categories = None,
        category_weights = None,
        categorical_distance = "OVERLAP",
        seed = None,
        seed_column = None,
        over_sampling_rate = 1.0,
        iteration_num = 5,
        setid_as_first_column = True,
        data_sequence_column = None):
        """
        DESCRIPTION:
            The RandomSample function takes a data set and uses a specified
            sampling method to output one or more random samples. Each sample has
            exactly the number of rows specified.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains the data
                set from which to take samples.
         
            num_sample:
                Required Argument.
                Specifies both the number of samples and their sizes. For each
                sample_size (an int value), the function selects a sample that has
                sample_size rows.
                Types: int OR list of Integers (int)
         
            weight_column:
                Optional Argument.
                Specifies the name of the teradataml DataFrame column that
                contains weights for weighted sampling. The weight_column must
                have a numeric SQL data type. By default, rows have equal weight.
                Types: str
         
            sampling_mode:
                Optional Argument.
                Specifies the sampling mode  and can be one of the following:
                    • "Basic": Each input_table row has a probability of being
                      selected that is proportional to its weight. The weight
                      of each row is in weight_column.
                    • "KMeans++": One row is selected in each of k iterations,
                      where k is the number of desired output rows. The first
                      row is selected randomly. In subsequent iterations, the
                      probability of a row being selected is proportional to the
                      value in the weight_column multiplied by the distance from
                      the nearest row in the set of selected rows. The distance
                      is calculated using the methods specified by the distance
                      and categorical_distance arguments.
                    • "KMeans||": Enhanced version of KMeans++ that exploits
                      parallel architecture to accelerate the sampling process.
                      The algorithm is described in the paper Scalable KMeans++
                      by Bahmani et al (http://theory.stanford.edu/~sergei/papers/vldb12-kmpar.pdf).
                      Briefly, at each iteration, the probability that a row is
                      selected is proportional to the value in the weight_column
                      multiplied by the distance from the nearest row in the set of
                      selected rows (as in KMeans++). However, the KMeans|| algorithm
                      oversamples at each iteration, significantly reducing the
                      required number of iterations; therefore, the resulting set of
                      rows might have more than k data points. Each row in the
                      resulting set is then weighted by the number of rows in the
                      teradataml DataFrame that are closer to that row than to any
                      other selected row, and the rows are clustered to produce
                      exactly k rows.
                Tip: For optimal performance, use "KMeans++" when the
                desired sample size is less than 15 and "KMeans||" otherwise.
                Default Value: "Basic"
                Permitted Values: Basic, KMeans++, KMeans||
                Types: str
         
            distance:
                Optional Argument.
                For KMeans++ and KMeans|| sampling, specifies the function for
                computing the distance between numerical variables:
                    • 'EUCLIDEAN' : The distance between two variables is defined
                      using Euclidean Distance.
                    • 'MANHATTAN': The distance between two variables is defined
                      using Manhattan Distance.
                Default Value: "EUCLIDEAN"
                Permitted Values: MANHATTAN, EUCLIDEAN
                Types: str
         
            input_columns:
                Optional Argument.
                For KMeans++ and KMeans|| sampling, specifies the names of the
                teradataml DataFrame columns to calculate the distance between
                numerical variables.
                Types: str OR list of Strings (str)
         
            as_categories:
                Optional Argument.
                For KMeans++ and KMeans|| sampling, specifies the names of the
                teradataml DataFrame columns that contain numerical variables
                to treat as categorical variables.
                Types: str OR list of Strings (str)
         
            category_weights:
                Optional Argument.
                For KMeans++ and KMeans|| sampling, specifies the weights
                (float values) of the categorical variables, including those
                that 'as_categories' argument specifies. Specify the weights in
                the order (from left to right) that the variables appear in the
                input teradataml Dataframe. When calculating the distance between
                two rows, distances between categorical values are scaled by
                these weights.
                Types: float or list of Floats (float).
         
            categorical_distance:
                Optional Argument.
                For KMeans++ and KMeans|| sampling, specifies the function for
                computing the distance between categorical variables:
                    • "OVERLAP" : The distance between two variables is 0 if
                      they are the same and 1 if they are different.
                    • "HAMMING": The distance beween two variables is the Hamming
                      distance between the strings that represent them. The
                      strings must have equal length.
                Default Value: "OVERLAP"
                Permitted Values: OVERLAP, HAMMING
                Types: str
         
            seed:
                Optional Argument.
                Specifies the random seed used to initialize the algorithm.
                Types: int
         
            seed_column:
                Optional Argument.
                Specifies the names of the teradataml DataFrame columns by
                which to partition the input. Function calls that use the same
                input data, seed, and seed_column output the same result. If
                you specify seed_column, you must also specify seed.
                Note: Ideally, the number of distinct values in the seed_column
                      is the same as the number of workers in the cluster. A very
                      large number of distinct values in the seed_column degrades
                      function performance.
                Types: str OR list of Strings (str)
         
            over_sampling_rate:
                Optional Argument.
                For KMeans|| sampling, specifies the oversampling rate (a float
                value greater than 0.0). The function multiplies rate by
                sample size (for each sample size).
                Default Value: 1.0
                Types: float
         
            iteration_num:
                Optional Argument.
                For KMeans|| sampling, specifies the number of iterations (an
                int value greater than 0).
                Default Value: 5
                Types: int
         
            setid_as_first_column:
                Optional Argument.
                Specifies whether the generated set_id values to be included as first
                column in output.
                Note: "setid_as_first_column" argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Default Value: True
                Types: bool
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each
                row of the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of RandomSample.
            Output teradataml DataFrames can be accessed using attribute
            references, such as RandomSampleObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("randomsample", ["fs_input", "fs_input1"])
         
            # Create teradataml DataFrame objects. The input tables have
            # observations of 11 variables for different models of cars.
            fs_input = DataFrame.from_table("fs_input")
            fs_input1 = DataFrame.from_table("fs_input1")
         
            # Example 1 - Basic Sampling (Weighted).
            # This example uses basic sampling to select one sample of 10 rows,
            # which are weighted by car weight.
            RandomSample_out1 = RandomSample(data = fs_input,
                                            num_sample = 10,
                                            weight_column = "wt",
                                            sampling_mode = "basic",
                                            seed = 1,
                                            seed_column = ["model"])
         
            # Print the result DataFrame
            print(RandomSample_out1)
         
            # Example 2 - KMeans++ Sampling.
            # This example uses KMeans++ sampling with the Manhattan
            # distance metric, and treats the numeric variables cyl,
            # gear, and carb as categorical variables.
            RandomSample_out2 = RandomSample(data = fs_input,
                                             num_sample = 10,
                                             sampling_mode = "KMeans++",
                                             distance = "manhattan",
                                             input_columns = ['mpg','cyl','disp','hp','drat','wt','qsec','vs','am','gear','carb'],
                                             as_categories = ["cyl","gear","carb"],
                                             category_weights = [1000.0,10.0,100.0,100.0,100.0],
                                             seed = 1,
                                             seed_column = ["model"]
                                             )
         
            # Print the result DataFrame
            print(RandomSample_out2.result)
         
            # Example 3 - KMeans|| Sampling.
            # This example uses KMeans|| sampling with the Manhattan
            # distance metric for the numerical variables and the Hamming
            # distance metric for the categorical variables.
            RandomSample_out3 = RandomSample(data = fs_input1,
                                            num_sample = 20,
                                            sampling_mode = "KMeans||",
                                            distance = "MANHATTAN",
                                            input_columns = ['mpg','cyl','disp','hp','drat','wt','qsec','vs','am','gear','carb'],
                                            as_categories = ["cyl","gear","carb"],
                                            category_weights = [1000.0,10.0,100.0,100.0,100.0],
                                            categorical_distance = "HAMMING",
                                            seed = 1,
                                            seed_column = ["model"],
                                            iteration_num = 2
                                            )
         
            # Print the result DataFrame
            print(RandomSample_out3.result)
         
            # Example 4 - This example uses basic sampling to select 3 sample
            # sets of sizes 2, 3 and 1 rows, weighted by car weight.
            RandomSample_out4 = RandomSample(data = fs_input,
                                             num_sample = [2,3,1],
                                              weight_column = "wt"
                                             )
         
            # Print the result DataFrame
            print(RandomSample_out4)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.num_sample  = num_sample 
        self.weight_column  = weight_column 
        self.sampling_mode  = sampling_mode 
        self.distance  = distance 
        self.input_columns  = input_columns 
        self.as_categories  = as_categories 
        self.category_weights  = category_weights 
        self.categorical_distance  = categorical_distance 
        self.seed  = seed 
        self.seed_column  = seed_column 
        self.over_sampling_rate  = over_sampling_rate 
        self.iteration_num  = iteration_num 
        self.setid_as_first_column  = setid_as_first_column 
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["num_sample", self.num_sample, False, (int,list)])
        self.__arg_info_matrix.append(["weight_column", self.weight_column, True, (str)])
        self.__arg_info_matrix.append(["sampling_mode", self.sampling_mode, True, (str)])
        self.__arg_info_matrix.append(["distance", self.distance, True, (str)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, True, (str,list)])
        self.__arg_info_matrix.append(["as_categories", self.as_categories, True, (str,list)])
        self.__arg_info_matrix.append(["category_weights", self.category_weights, True, (float,list)])
        self.__arg_info_matrix.append(["categorical_distance", self.categorical_distance, True, (str)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["seed_column", self.seed_column, True, (str,list)])
        self.__arg_info_matrix.append(["over_sampling_rate", self.over_sampling_rate, True, (float)])
        self.__arg_info_matrix.append(["iteration_num", self.iteration_num, True, (int)])
        self.__arg_info_matrix.append(["setid_as_first_column", self.setid_as_first_column, True, (bool)])
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
        sampling_mode_permitted_values = ["BASIC", "KMEANS++", "KMEANS||"]
        self.__awu._validate_permitted_values(self.sampling_mode, sampling_mode_permitted_values, "sampling_mode")
        
        distance_permitted_values = ["MANHATTAN", "EUCLIDEAN"]
        self.__awu._validate_permitted_values(self.distance, distance_permitted_values, "distance")
        
        categorical_distance_permitted_values = ["OVERLAP", "HAMMING"]
        self.__awu._validate_permitted_values(self.categorical_distance, categorical_distance_permitted_values, "categorical_distance")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.weight_column, "weight_column")
        self.__awu._validate_dataframe_has_argument_columns(self.weight_column, "weight_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.as_categories, "as_categories")
        self.__awu._validate_dataframe_has_argument_columns(self.as_categories, "as_categories", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.seed_column, "seed_column")
        self.__awu._validate_dataframe_has_argument_columns(self.seed_column, "seed_column", self.data, "data", False)
        
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
        
        if self.weight_column is not None:
            self.__func_other_arg_sql_names.append("WeightColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.weight_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.input_columns is not None:
            self.__func_other_arg_sql_names.append("InputColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.input_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.as_categories is not None:
            self.__func_other_arg_sql_names.append("AsCategories")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.as_categories, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.seed_column is not None:
            self.__func_other_arg_sql_names.append("SeedColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.seed_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("NumSample")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_sample, "'"))
        self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.sampling_mode is not None and self.sampling_mode != "Basic":
            self.__func_other_arg_sql_names.append("SamplingMode")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.sampling_mode, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.distance is not None and self.distance != "EUCLIDEAN":
            self.__func_other_arg_sql_names.append("Distance")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.distance, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.categorical_distance is not None and self.categorical_distance != "OVERLAP":
            self.__func_other_arg_sql_names.append("CategoricalDistance")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.categorical_distance, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.category_weights is not None:
            self.__func_other_arg_sql_names.append("CategoryWeights")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.category_weights, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        if self.over_sampling_rate is not None and self.over_sampling_rate != 1.0:
            self.__func_other_arg_sql_names.append("OverSamplingRate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.over_sampling_rate, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.iteration_num is not None and self.iteration_num != 5:
            self.__func_other_arg_sql_names.append("IterationNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.iteration_num, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.setid_as_first_column is not None and self.setid_as_first_column != True:
            self.__func_other_arg_sql_names.append("SetIdAsFirstColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.setid_as_first_column, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
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
        
        function_name = "RandomSample"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type = TeradataConstants.TERADATA_TABLE)
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
        Returns the string representation for a RandomSample class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
