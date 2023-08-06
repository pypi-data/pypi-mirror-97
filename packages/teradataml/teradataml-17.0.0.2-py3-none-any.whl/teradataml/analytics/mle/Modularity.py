#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2019 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Rohit Khurd (rohit.khurd@teradata.com)
# Secondary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# 
# Version: 1.2
# Function Version: 1.8
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

class Modularity:
    
    def __init__(self,
        vertices_data = None,
        edges_data = None,
        sources_data = None,
        target_key = None,
        edge_weight = None,
        community_association = None,
        resolution = 1.0,
        seed = 1,
        accumulate = None,
        vertices_data_sequence_column = None,
        edges_data_sequence_column = None,
        sources_data_sequence_column = None,
        vertices_data_partition_column = None,
        edges_data_partition_column = None,
        sources_data_partition_column = None):
        """
        DESCRIPTION:
            The Modularity function uses a clustering algorithm to detect
            communities in networks (graphs). The function needs no prior knowledge or
            estimation of starting cluster centers and assumes no particular data distribution of the
            input data set.
         
         
        PARAMETERS:
            vertices_data:
                Required Argument.
                Specifies vertex teradataml DataFrame where each row represents a vertex of the graph.
         
            vertices_data_partition_column:
                Required Argument.
                Specifies Partition By columns for vertices_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            edges_data:
                Required Argument.
                Specifies edge teradataml DataFrame where each row represents an edge of the graph.
         
            edges_data_partition_column:
                Required Argument.
                Specifies Partition By columns for edges_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            sources_data:
                Optional Argument.
                Specifies source vertices teradataml DataFrame, required for directed graph.
                Function ignores this teradataml DataFrame and treats all graphs as undirected.
         
            sources_data_partition_column:
                Optional Argument. Required when 'sources_data' argument is specified.
                Specifies Partition By columns for sources_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            target_key:
                Required Argument.
                Specifies the key of the target vertex of an edge. The key consists
                of the names of one or more edges teradataml DataFrame columns.
                Types: str OR list of Strings (str)
         
            edge_weight:
                Optional Argument.
                Specifies the name of the edges teradataml DataFrame column that
                contains edge weights. The weights are positive values. By default,
                the weight of each edge is 1 (that is, the graph is unweighted). This
                argument determines how the function treats duplicate edges (that is,
                edges with the same source and destination, which might have
                different weights). For a weighted graph, the function treats
                duplicate edges as a single edge whose weight is the sum of the
                weights of the duplicate edges. For an unweighted graph, the function
                uses only one of the duplicate edges.
                Types: str
         
            community_association:
                Optional Argument.
                Specifies the name of the column that represents the community
                association of the vertices. Use this argument if you already know
                some vertex communities.
                Types: str
         
            resolution:
                Optional Argument.
                Specifies hierarchical-level information for the communities. If you
                specify a list of resolution values, the function incrementally finds
                the communities for each value and for the default value. Each resolution
                must be a distinct float value in the range [0.0, 1000000.0]. The value 0.0
                puts each node in its own community of size 1. You can specify a maximum of 500
                resolution values. To get the modularity of more than 500 resolution
                points, call the function multiple times, specifying different values
                in each call.
                Default Value: 1.0
                Types: float OR list of floats
         
            seed:
                Optional Argument.
                Specifies the seed to use to create a random number during modularity
                computation. The seed must be a positive BIGINT value. The function
                multiplies seed by the hash code of vertex_key to generate a unique
                seed for each vertex. The seed significantly impacts community formation
                (and modularity score), because the function uses seed for these purposes:
                    • To break ties between different vertices during community formation.
                    • To determine how deeply to analyze the graph. Deeper analysis of the graph
                      can improve community formation, but can also increase execution time.
                Default Value: 1
                Types: int
         
            accumulate:
                Optional Argument.
                Specifies the names of the vertices columns to copy to the community
                vertex teradataml DataFrame. By default, the function copies the vertex_key
                columns to the output vertex teradataml DataFrame for each vertex, changing
                the column names to id, id_1, id_2, and so on.
                Types: str OR list of Strings (str)
         
            vertices_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "vertices_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            edges_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "edges_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            sources_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "sources_data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Modularity.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ModularityObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. community_edge_data
                2. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            # The examples use a graph in which nodes represent persons who are geographically distributed
            # across the United States and are connected on an online social network, where they follow each other.
            # The directed edges start at the follower and end at the leader.
            load_example_data("modularity", ["friends", "followers_leaders"])
         
            # Create teradataml DataFrame objects.
            friends = DataFrame.from_table("friends")
            followers_leaders = DataFrame.from_table("followers_leaders")
         
            # Example 1 - Unweighted Edges.
            # Followers follow leaders with equal intensity (all edges have default weight 1).
            Modularity_out1 = Modularity(vertices_data = friends,
                                         vertices_data_partition_column = ["friends_name"],
                                         edges_data = followers_leaders,
                                         edges_data_partition_column = ["follower"],
                                         target_key = ["leader"],
                                         community_association = "group_id",
                                         accumulate = ["friends_name","location"]
                                         )
            # Print the results
            print(Modularity_out1)
         
            # Example 2 - Weighted Edges and Community Edge Table.
            # Followers follow leaders with different intensity.
            Modularity_out2 = Modularity(vertices_data = friends,
                                         vertices_data_partition_column = ["friends_name"],
                                         edges_data = followers_leaders,
                                         edges_data_partition_column = ["follower"],
                                         target_key = ["leader"],
                                         edge_weight = "intensity",
                                         community_association = "group_id",
                                         accumulate = ["friends_name","location"]
                                         )
            # Print the results
            print(Modularity_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.vertices_data  = vertices_data 
        self.edges_data  = edges_data 
        self.sources_data  = sources_data 
        self.target_key  = target_key 
        self.accumulate  = accumulate 
        self.edge_weight  = edge_weight 
        self.community_association  = community_association 
        self.resolution  = resolution 
        self.seed  = seed 
        self.vertices_data_sequence_column  = vertices_data_sequence_column 
        self.edges_data_sequence_column  = edges_data_sequence_column 
        self.sources_data_sequence_column  = sources_data_sequence_column 
        self.vertices_data_partition_column  = vertices_data_partition_column 
        self.edges_data_partition_column  = edges_data_partition_column 
        self.sources_data_partition_column  = sources_data_partition_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["vertices_data", self.vertices_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["vertices_data_partition_column", self.vertices_data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["edges_data", self.edges_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["edges_data_partition_column", self.edges_data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["sources_data", self.sources_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["sources_data_partition_column", self.sources_data_partition_column, self.sources_data is None, (str,list)])
        self.__arg_info_matrix.append(["target_key", self.target_key, False, (str,list)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["edge_weight", self.edge_weight, True, (str)])
        self.__arg_info_matrix.append(["community_association", self.community_association, True, (str)])
        self.__arg_info_matrix.append(["resolution", self.resolution, True, (float,list)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["vertices_data_sequence_column", self.vertices_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["edges_data_sequence_column", self.edges_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["sources_data_sequence_column", self.sources_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.vertices_data, "vertices_data", None)
        self.__awu._validate_input_table_datatype(self.edges_data, "edges_data", None)
        self.__awu._validate_input_table_datatype(self.sources_data, "sources_data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.target_key, "target_key")
        self.__awu._validate_dataframe_has_argument_columns(self.target_key, "target_key", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.community_association, "community_association")
        self.__awu._validate_dataframe_has_argument_columns(self.community_association, "community_association", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.edge_weight, "edge_weight")
        self.__awu._validate_dataframe_has_argument_columns(self.edge_weight, "edge_weight", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_sequence_column, "vertices_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_sequence_column, "vertices_data_sequence_column", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_sequence_column, "edges_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_sequence_column, "edges_data_sequence_column", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.sources_data_sequence_column, "sources_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sources_data_sequence_column, "sources_data_sequence_column", self.sources_data, "sources_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_partition_column, "vertices_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_partition_column, "vertices_data_partition_column", self.vertices_data, "vertices_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_partition_column, "edges_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_partition_column, "edges_data_partition_column", self.edges_data, "edges_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.sources_data_partition_column, "sources_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sources_data_partition_column, "sources_data_partition_column", self.sources_data, "sources_data", True)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__community_edge_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_modularity0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["CommunityEdgeTable"]
        self.__func_output_args = [self.__community_edge_data_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("TargetKey")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.community_association is not None:
            self.__func_other_arg_sql_names.append("CommunityAssociation")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.community_association, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.edge_weight is not None:
            self.__func_other_arg_sql_names.append("EdgeWeight")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.edge_weight, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.resolution is not None and self.resolution != [1]:
            self.__func_other_arg_sql_names.append("Resolution")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.resolution, "'"))
            self.__func_other_arg_json_datatypes.append("FLOAT")
        
        if self.seed is not None and self.seed != 1:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.vertices_data_sequence_column is not None:
            sequence_input_by_list.append("vertices:" + UtilFuncs._teradata_collapse_arglist(self.vertices_data_sequence_column, ""))
        
        if self.edges_data_sequence_column is not None:
            sequence_input_by_list.append("edges:" + UtilFuncs._teradata_collapse_arglist(self.edges_data_sequence_column, ""))
        
        if self.sources_data_sequence_column is not None:
            sequence_input_by_list.append("sources:" + UtilFuncs._teradata_collapse_arglist(self.sources_data_sequence_column, ""))
        
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
        
        # Process vertices_data
        self.vertices_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.vertices_data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.vertices_data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("vertices")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.vertices_data_partition_column)
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process edges_data
        self.edges_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.edges_data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.edges_data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("edges")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.edges_data_partition_column)
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process sources_data
        self.sources_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.sources_data_partition_column, "\"")
        if self.sources_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.sources_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("sources")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.sources_data_partition_column)
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "Modularity"
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
        self.community_edge_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__community_edge_data_temp_tablename),
                                                                      source_type="table",
                                                                      database_name=UtilFuncs._extract_db_name(self.__community_edge_data_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename),
                                                         source_type="table",
                                                         database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.community_edge_data)
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
        community_edge_data = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("community_edge_data", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.community_edge_data  = community_edge_data 
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
        obj.community_edge_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.community_edge_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.community_edge_data))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.community_edge_data)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a Modularity class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ community_edge_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.community_edge_data)
        return repr_string
        
