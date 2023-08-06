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
# Function Version: 1.4
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

class Closeness:
    
    def __init__(self,
        vertices_data = None,
        edges_data = None,
        target_key = None,
        sources_data = None,
        targets_data = None,
        directed = True,
        edge_weight = None,
        max_distance = 10,
        group_size = None,
        sample_rate = 1.0,
        seed = None,
        accumulate = None,
        vertices_data_sequence_column = None,
        edges_data_sequence_column = None,
        sources_data_sequence_column = None,
        targets_data_sequence_column = None,
        vertices_data_partition_column = None,
        edges_data_partition_column = None,
        sources_data_partition_column = None,
        targets_data_partition_column = None,
        vertices_data_order_column = None,
        edges_data_order_column = None,
        sources_data_order_column = None,
        targets_data_order_column = None):
        """
        DESCRIPTION:
            The Closeness function returns closeness and k-degree scores for each
            specified source vertex in a graph. The closeness scores are the
            inverse of the sum, the inverse of the average, and the sum of inverses
            for the shortest distances to all reachable target vertices
            (excluding the source vertex itself). The graph can be directed or
            undirected, weighted or unweighted.
         
         
        PARAMETERS:
            vertices_data:
                Required Argument.
                Specifies the teradataml DataFrame where each row represents a
                vertex of the graph.
            
            vertices_data_partition_column:
                Required Argument.
                Specifies Partition By columns for vertices_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
            
            vertices_data_order_column:
                Optional Argument.
                Specifies Order By columns for vertices_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
            
            edges_data:
                Required Argument.
                Specifies the teradataml DataFrame where each row represents an
                edge of the graph.
            
            edges_data_partition_column:
                Required Argument.
                Specifies Partition By columns for edges_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
            
            edges_data_order_column:
                Optional Argument.
                Specifies Order By columns for edges_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
            
            target_key:
                Required Argument.
                Specifies the target key (the names of the edges_data teradataml DataFrame
                columns that identify the target vertex). If you specify 
                targets_data, then the function uses only the vertices in
                targets_data as targets (which must be a subset of those that this
                argument specifies).
                Types: str OR list of Strings (str)
            
            sources_data:
                Required for directed graph, optional for undirected graph.
                Specifies the teradataml DataFrame which contains the vertices to use as sources.
            
            sources_data_partition_column:
                Required Argument when sources_data is used.
                Specifies Partition By columns for sources_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
            
            sources_data_order_column:
                Optional Argument.
                Specifies Order By columns for sources_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
            
            targets_data:
                Required for directed graph, optional for undirected graph.
                Specifies the teradataml DataFrame which contains the vertices to use as targets.
            
            targets_data_partition_column:
                Required Argument when targets_data is used.
                Specifies Partition By columns for targets_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
            
            targets_data_order_column:
                Optional Argument.
                Specifies Order By columns for targets_data.
                Values to this argument can be provided as a list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
            
            directed:
                Optional Argument.
                Specifies whether the graph is directed. 
                Default Value: True
                Types: bool
            
            edge_weight:
                Optional Argument.
                Specifies the name of the edges_data teradataml DataFrame column that
                contains edge weights. The weights are positive values.
                By default, the weight of each edge is 1 (that is, the graph is unweighted).
                Types: str
            
            max_distance:
                Optional Argument.
                Specifies the maximum distance between the source and
                target vertices. A negative max_distance specifies an infinite
                distance. If vertices are separated by more than max_distance, the
                function does not output them.
                Default Value: 10
                Types: int
            
            group_size:
                Optional Argument.
                Specifies the number of source vertices that execute a single-node shortest
                path (SNSP) algorithm in parallel. If group_size exceeds the number of
                source vertices in each partition, s, then s is the group size.
                By default, the function calculates the optimal group size based on
                various cluster and query characteristics.
                Running a group of vertices on each vWorker, in parallel, uses less
                memory than running all vertices on each vWorker.
                Types: int
            
            sample_rate:
                Optional Argument.
                Specifies the sample rate (the percentage of source vertices to 
                sample), a numeric value in the range (0, 1].
                Default Value: 1.0
                Types: float
            
            seed:
                Optional Argument.
                Specifies the random seed, used for deterministic results.
                Types: int
            
            accumulate:
                Optional Argument.
                Specifies the names of the vertices_data teradataml DataFrame columns to
                copy to the output teradataml DataFrame.
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
            
            targets_data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "targets_data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of Closeness.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as ClosenessObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("Closeness", ["callers", "calls"])
         
            # Create teradataml DataFrame object.
            callers = DataFrame.from_table("callers")
            calls = DataFrame.from_table("calls")
            sources = DataFrame.from_query("select * from callers where callerid <= 3")
            target = DataFrame.from_query("select * from callers where callerid >3")
         
            # Example 1 - Running Closeness function for unweighted and unbounded.
            closeness_out1 = Closeness(vertices_data=callers,
                           vertices_data_partition_column='callerid',
                           edges_data=calls,
                           edges_data_partition_column='callerfrom',
                           sources_data=sources,
                           sources_data_partition_column='callerid',
                           targets_data=target,
                           targets_data_partition_column='callerid',
                           target_key='callerto',
                           accumulate=['callerid', 'callername'],
                           max_distance=-1,
                           edges_data_sequence_column='callerfrom',
                           vertices_data_sequence_column='callerid'
                           )
         
            # Print the output DataFrames.
            print(closeness_out1.result)
         
            # Example 2 - Running Closeness function for weighted, bounded graph and with max_distance
            # argument taking 12.
            closeness_out2 = Closeness(vertices_data=callers,
                           vertices_data_partition_column='callerid',
                           edges_data=calls,
                           edges_data_partition_column='callerfrom',
                           sources_data=sources,
                           sources_data_partition_column='callerid',
                           targets_data=target,
                           targets_data_partition_column='callerid',
                           target_key='callerto',
                           edge_weight='calls',
                           accumulate=['callerid', 'callername'],
                           max_distance=12,
                           edges_data_sequence_column='callerfrom',
                           vertices_data_sequence_column='callerid'
                           )
         
            # Print the output DataFrames.
            print(closeness_out2.result)
         
            # Example 3 - Running Closeness function for weighted, bounded graph and with max_distance
            # argument taking 8.
            closeness_out3 = Closeness(vertices_data=callers,
                           vertices_data_partition_column='callerid',
                           edges_data=calls,
                           edges_data_partition_column='callerfrom',
                           sources_data=sources,
                           sources_data_partition_column='callerid',
                           targets_data=target,
                           targets_data_partition_column='callerid',
                           target_key='callerto',
                           edge_weight='calls',
                           accumulate=['callerid', 'callername'],
                           max_distance=8,
                           edges_data_sequence_column='callerfrom',
                           vertices_data_sequence_column='callerid'
                           )
         
            # Print the output DataFrames.
            print(closeness_out3.result)

            # Example 4 - Running Closeness function for unweighted and unbounded graph
            # without sources_data and target_data.
            closeness_out4 = Closeness(vertices_data=callers,
                           vertices_data_partition_column='callerid',
                           edges_data=calls,
                           edges_data_partition_column='callerfrom',
                           target_key='callerto',
                           accumulate=['callerid', 'callername'],
                           max_distance=-1,
                           edges_data_sequence_column='callerfrom',
                           vertices_data_sequence_column='callerid'
                           )
         
            # Print the output DataFrames.
            print(closeness_out4.result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.vertices_data  = vertices_data 
        self.edges_data  = edges_data 
        self.target_key  = target_key 
        self.sources_data  = sources_data 
        self.targets_data  = targets_data 
        self.directed  = directed 
        self.edge_weight  = edge_weight 
        self.max_distance  = max_distance 
        self.group_size  = group_size 
        self.sample_rate  = sample_rate 
        self.seed  = seed 
        self.accumulate  = accumulate 
        self.vertices_data_sequence_column  = vertices_data_sequence_column 
        self.edges_data_sequence_column  = edges_data_sequence_column 
        self.sources_data_sequence_column  = sources_data_sequence_column 
        self.targets_data_sequence_column  = targets_data_sequence_column 
        self.vertices_data_partition_column  = vertices_data_partition_column 
        self.edges_data_partition_column  = edges_data_partition_column 
        self.sources_data_partition_column  = sources_data_partition_column 
        self.targets_data_partition_column  = targets_data_partition_column 
        self.vertices_data_order_column  = vertices_data_order_column 
        self.edges_data_order_column  = edges_data_order_column 
        self.sources_data_order_column  = sources_data_order_column 
        self.targets_data_order_column  = targets_data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["vertices_data", self.vertices_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["vertices_data_partition_column", self.vertices_data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["vertices_data_order_column", self.vertices_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["edges_data", self.edges_data, False, (DataFrame)])
        self.__arg_info_matrix.append(["edges_data_partition_column", self.edges_data_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["edges_data_order_column", self.edges_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["target_key", self.target_key, False, (str,list)])
        self.__arg_info_matrix.append(["sources_data", self.sources_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["sources_data_partition_column", self.sources_data_partition_column, self.sources_data is None, (str, list)])
        self.__arg_info_matrix.append(["sources_data_order_column", self.sources_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["targets_data", self.targets_data, True, (DataFrame)])
        self.__arg_info_matrix.append(["targets_data_partition_column", self.targets_data_partition_column, self.targets_data is None, (str, list)])
        self.__arg_info_matrix.append(["targets_data_order_column", self.targets_data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["directed", self.directed, True, (bool)])
        self.__arg_info_matrix.append(["edge_weight", self.edge_weight, True, (str)])
        self.__arg_info_matrix.append(["max_distance", self.max_distance, True, (int)])
        self.__arg_info_matrix.append(["group_size", self.group_size, True, (int)])
        self.__arg_info_matrix.append(["sample_rate", self.sample_rate, True, (float)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["vertices_data_sequence_column", self.vertices_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["edges_data_sequence_column", self.edges_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["sources_data_sequence_column", self.sources_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["targets_data_sequence_column", self.targets_data_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.targets_data, "targets_data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.target_key, "target_key")
        self.__awu._validate_dataframe_has_argument_columns(self.target_key, "target_key", self.edges_data, "edges_data", False)
        
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
        
        self.__awu._validate_input_columns_not_empty(self.targets_data_sequence_column, "targets_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.targets_data_sequence_column, "targets_data_sequence_column", self.targets_data, "targets_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_partition_column, "vertices_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_partition_column, "vertices_data_partition_column", self.vertices_data, "vertices_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_partition_column, "edges_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_partition_column, "edges_data_partition_column", self.edges_data, "edges_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.sources_data_partition_column, "sources_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sources_data_partition_column, "sources_data_partition_column", self.sources_data, "sources_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.targets_data_partition_column, "targets_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.targets_data_partition_column, "targets_data_partition_column", self.targets_data, "targets_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_order_column, "vertices_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_order_column, "vertices_data_order_column", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_order_column, "edges_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_order_column, "edges_data_order_column", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.sources_data_order_column, "sources_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sources_data_order_column, "sources_data_order_column", self.sources_data, "sources_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.targets_data_order_column, "targets_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.targets_data_order_column, "targets_data_order_column", self.targets_data, "targets_data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("TargetKey")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.target_key, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.edge_weight is not None:
            self.__func_other_arg_sql_names.append("EdgeWeight")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.edge_weight, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.sample_rate is not None and self.sample_rate != 1.0:
            self.__func_other_arg_sql_names.append("SampleRate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.sample_rate, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None:
            self.__func_other_arg_sql_names.append("seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.max_distance is not None and self.max_distance != 10:
            self.__func_other_arg_sql_names.append("MaxDistance")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_distance, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.directed is not None and self.directed != True:
            self.__func_other_arg_sql_names.append("Directed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.directed, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.group_size is not None:
            self.__func_other_arg_sql_names.append("GroupSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.group_size, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.vertices_data_sequence_column is not None:
            sequence_input_by_list.append("vertices:" + UtilFuncs._teradata_collapse_arglist(self.vertices_data_sequence_column, ""))
        
        if self.edges_data_sequence_column is not None:
            sequence_input_by_list.append("edges:" + UtilFuncs._teradata_collapse_arglist(self.edges_data_sequence_column, ""))
        
        if self.sources_data_sequence_column is not None:
            sequence_input_by_list.append("sources:" + UtilFuncs._teradata_collapse_arglist(self.sources_data_sequence_column, ""))
        
        if self.targets_data_sequence_column is not None:
            sequence_input_by_list.append("targets:" + UtilFuncs._teradata_collapse_arglist(self.targets_data_sequence_column, ""))
        
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
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.vertices_data_order_column, "\""))
        
        # Process edges_data
        self.edges_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.edges_data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.edges_data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("edges")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.edges_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.edges_data_order_column, "\""))
        
        # Process sources_data
        self.sources_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.sources_data_partition_column, "\"")
        if self.sources_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.sources_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("sources")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.sources_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.sources_data_order_column, "\""))
        
        # Process targets_data
        self.targets_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.targets_data_partition_column, "\"")
        if self.targets_data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.targets_data, False)
            self.__func_input_distribution.append("FACT")
            self.__func_input_arg_sql_names.append("targets")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append(self.targets_data_partition_column)
            self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.targets_data_order_column, "\""))
        
        function_name = "Closeness"
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
        Returns the string representation for a Closeness class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
