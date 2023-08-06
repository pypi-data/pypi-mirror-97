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
# Function Version: 1.16
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

class KMeans:
    
    def __init__(self,
        data = None,
        centers = None,
        iter_max = 10,
        initial_seeds = None,
        seed = None,
        unpack_columns = False,
        centroids_table = None,
        threshold = 0.0395,
        data_sequence_column = None,
        centroids_table_sequence_column = None):
        """
        DESCRIPTION:
            The KMeans function takes a data set and outputs the centroids of its
            clusters and, optionally, the clusters themselves.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame containing the list of
                features by which we are clustering the data.
         
            centers:
                Optional Argument.
                Specifies the number of clusters to generate from the data.
                Note: With centers, the function uses a nondeterministic
                      algorithm and the function supports up to 1543 dimensions.
                Types: int
         
            iter_max:
                Optional Argument.
                Specifies the maximum number of iterations that the algorithm runs
                before quitting if the convergence threshold has not been met.
                Default Value: 10
                Types: int
         
            initial_seeds:
                Optional Argument.
                Specifies the initial seed means as strings of underscore-delimited
                float values. For example, this clause initializes eight clusters in
                eight-dimensional space: Means("50_50_50_50_50_50_50_50",
                "150_150_150_150_150_150_150_150", "250_250_250_250_250_250_250_250",
                "350_350_350_350_350_350_350_350", "450_450_450_450_450_450_450_450",
                "550_550_550_550_550_550_550_550", "650_650_650_650_650_650_650_650",
                "750_750_750_750_750_750_750_750") The dimensionality of the means
                must match the dimensionality of the data (that is, each mean must
                have n numbers in it, where n is the number of input columns minus
                one). By default, the algorithm chooses the initial seed means
                randomly.
                Note: With initial_seeds, the function uses a deterministic
                      algorithm and the function supports up to 1596 dimensions.
                Types: str OR list of Strings (str)
         
            seed:
                Optional Argument.
                Sets a random seed for the algorithm.
                Types: int
         
            unpack_columns:
                Optional Argument.
                Specifies whether the means for each centroid appear unpacked (that
                is, in separate columns) in output DataFrame clusters_centroids.
                By default, the function concatenates the means for the centroids
                and outputs the result in a single VARCHAR column.
                Default Value: False
                Types: bool
         
            centroids_table:
                Optional Argument.
                Specifies the teradataml DataFrame that contains the initial seed
                means for the clusters. The schema of the centroids teradataml
                DataFrame depends on the value of the unpack_columns argument.
                Note: With centroids_table, the function uses a deterministic
                      algorithm and the function supports up to 1596 dimensions.
         
            threshold:
                Optional Argument.
                Specifies the convergence threshold. When the centroids move by less
                than this amount, the algorithm has converged.
                Default Value: 0.0395
                Types: float
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            centroids_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "centroids_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of KMeans.
            Output teradataml DataFrames can be accessed using attribute
            references, such as KMeansObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. clusters_centroids
                2. clustered_output
                3. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("KMeans","computers_train1")
         
            # Create teradataml Dataframe.
            computers_train1 = DataFrame.from_table("computers_train1")
         
            # Example 1 -
            kmeans_out =  KMeans(data=computers_train1,
                                 initial_seeds=['2249_51_408_8_14','2165_51_398_7_14.6','2182_51_404_7_14.6','2204_55_372_7.19_14.6','2419_44_222_6.6_14.3','2394_44.3_277_7.3_14.5','2326_43.6_301_7.11_14.3','2288_44_325_7_14.4'],
                                 centers=8,
                                 threshold=0.0395,
                                 iter_max=10,
                                 unpack_columns=False,
                                 seed=10,
                                 data_sequence_column='id'
                                 )
            # Print the result DataFrame
            print(kmeans_out.clusters_centroids)
            print(kmeans_out.clustered_output)
            print(kmeans_out.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.centers  = centers 
        self.iter_max  = iter_max 
        self.initial_seeds  = initial_seeds 
        self.seed  = seed 
        self.unpack_columns  = unpack_columns 
        self.centroids_table  = centroids_table 
        self.threshold  = threshold 
        self.data_sequence_column  = data_sequence_column 
        self.centroids_table_sequence_column  = centroids_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["centers", self.centers, True, (int)])
        self.__arg_info_matrix.append(["iter_max", self.iter_max, True, (int)])
        self.__arg_info_matrix.append(["initial_seeds", self.initial_seeds, True, (str,list)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["unpack_columns", self.unpack_columns, True, (bool)])
        self.__arg_info_matrix.append(["centroids_table", self.centroids_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["threshold", self.threshold, True, (float)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["centroids_table_sequence_column", self.centroids_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.centroids_table, "centroids_table", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.centroids_table_sequence_column, "centroids_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.centroids_table_sequence_column, "centroids_table_sequence_column", self.centroids_table, "centroids_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__clusters_centroids_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_kmeans0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__clustered_output_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_kmeans1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable", "ClusteredOutput"]
        self.__func_output_args = [self.__clusters_centroids_temp_tablename, self.__clustered_output_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        if self.initial_seeds is not None:
            self.__func_other_arg_sql_names.append("InitialSeeds")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.initial_seeds, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.centers is not None:
            self.__func_other_arg_sql_names.append("NumClusters")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.centers, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.threshold is not None and self.threshold != 0.0395:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.threshold, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.iter_max is not None:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.iter_max, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.unpack_columns is not None and self.unpack_columns != False:
            self.__func_other_arg_sql_names.append("UnpackColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.unpack_columns, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.centroids_table_sequence_column is not None:
            sequence_input_by_list.append("CentroidsTable:" + UtilFuncs._teradata_collapse_arglist(self.centroids_table_sequence_column, ""))
        
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
        
        # Process centroids_table
        if self.centroids_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.centroids_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("CentroidsTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "KMeans"
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
        self.clusters_centroids = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__clusters_centroids_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__clusters_centroids_temp_tablename))
        self.clustered_output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__clustered_output_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__clustered_output_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.clusters_centroids)
        self._mlresults.append(self.clustered_output)
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
        clusters_centroids = None,
        clustered_output = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("clusters_centroids", None)
        kwargs.pop("clustered_output", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.clusters_centroids  = clusters_centroids 
        obj.clustered_output  = clustered_output 
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
        obj.clusters_centroids = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.clusters_centroids), source_type="table", database_name=UtilFuncs._extract_db_name(obj.clusters_centroids))
        obj.clustered_output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.clustered_output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.clustered_output))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.clusters_centroids)
        obj._mlresults.append(obj.clustered_output)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a KMeans class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ clusters_centroids Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.clusters_centroids)
        repr_string="{}\n\n\n############ clustered_output Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.clustered_output)
        return repr_string
        
