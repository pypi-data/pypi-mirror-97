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

class PageRank:
    
    def __init__(self,
        vertices_data = None,
        edges_data = None,
        target_key = None,
        weights = None,
        damping = 0.85,
        niter = 1000,
        eps = 0.001,
        accumulate = None,
        vertices_data_sequence_column = None,
        edges_data_sequence_column = None,
        vertices_data_partition_column = None,
        edges_data_partition_column = None,
        vertices_data_order_column = None,
        edges_data_order_column = None):
        """
        DESCRIPTION:
            The PageRank function computes the PageRank values for a directed 
            graph, weighted or unweighted.
         
         
        PARAMETERS:
            vertices_data:
                Required Argument.
                The input teradataml DataFrame contains vertices in the graph.
         
            vertices_data_partition_column:
                Required Argument.
                Specifies Partition By columns for vertices_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            vertices_data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            edges_data:
                Required Argument.
                The input teradataml DataFrame contains edges in the graph.
         
            edges_data_partition_column:
                Required Argument.
                Specifies Partition By columns for edges_data.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)
         
            edges_data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            target_key:
                Required Argument.
                Specifies the target key columns in the edges_data.
                Types: str OR list of Strings (str)
         
            weights:
                Optional Argument.
                Specifies the column in the edges teradataml DataFrame that contains
                the edge weight, which must be a positive value. By default, all
                edges have the same weight (that is, the graph is unweighted).
                Types: str
         
            damping:
                Optional Argument.
                Specifies the value to use in the PageRank formula. The damping
                must be a float value between 0 and 1.
                Default Value: 0.85
                Types: float
         
            niter:
                Optional Argument.
                Specifies the maximum number of iterations for which the algorithm
                runs before the function completes. The niter must be a
                positive int value.
                Default Value: 1000
                Types: int
         
            eps:
                Optional Argument.
                Specifies the convergence criteria value. The eps must be a
                float value.
                Default Value: 0.001
                Types: float
         
            accumulate:
                Optional Argument.
                Specifies the vertices teradataml DataFrame columns to copy to the
                output table.
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
         
        RETURNS:
            Instance of PageRank.
            Output teradataml DataFrames can be accessed using attribute
            references, such as PageRankObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("pagerank", ["callers", "calls"])
         
            # Create teradataml DataFrame objects.
            # Vertices table
            callers = DataFrame.from_table("callers")
            # Edges table
            calls = DataFrame.from_table("calls")
         
            # Example 1 - Find PageRank for each vertex.
            PageRank_out = PageRank(vertices_data = callers,
                                    vertices_data_partition_column = ["callerid"],
                                    edges_data = calls,
                                    edges_data_partition_column = ["callerfrom"],
                                    target_key = ["callerto"],
                                    weights = "calls",
                                    accumulate = ["callerid","callername"]
                                    )
         
            # Print the results.
            print(PageRank_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.vertices_data  = vertices_data 
        self.edges_data  = edges_data 
        self.target_key  = target_key
        self.weights  = weights 
        self.damping  = damping 
        self.niter  = niter 
        self.eps  = eps 
        self.accumulate  = accumulate 
        self.vertices_data_sequence_column  = vertices_data_sequence_column 
        self.edges_data_sequence_column  = edges_data_sequence_column 
        self.vertices_data_partition_column  = vertices_data_partition_column 
        self.edges_data_partition_column  = edges_data_partition_column 
        self.vertices_data_order_column  = vertices_data_order_column 
        self.edges_data_order_column  = edges_data_order_column 
        
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
        self.__arg_info_matrix.append(["weights", self.weights, True, (str)])
        self.__arg_info_matrix.append(["damping", self.damping, True, (float)])
        self.__arg_info_matrix.append(["niter", self.niter, True, (int)])
        self.__arg_info_matrix.append(["eps", self.eps, True, (float)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["vertices_data_sequence_column", self.vertices_data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["edges_data_sequence_column", self.edges_data_sequence_column, True, (str,list)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Process output table schema
            self.__process_output_column_info()
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
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.target_key, "target_key")
        self.__awu._validate_dataframe_has_argument_columns(self.target_key, "target_key", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.weights, "weights")
        self.__awu._validate_dataframe_has_argument_columns(self.weights, "weights", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_sequence_column, "vertices_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_sequence_column, "vertices_data_sequence_column", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_sequence_column, "edges_data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_sequence_column, "edges_data_sequence_column", self.edges_data, "edges_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_partition_column, "vertices_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_partition_column, "vertices_data_partition_column", self.vertices_data, "vertices_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_partition_column, "edges_data_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_partition_column, "edges_data_partition_column", self.edges_data, "edges_data", True)
        
        self.__awu._validate_input_columns_not_empty(self.vertices_data_order_column, "vertices_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.vertices_data_order_column, "vertices_data_order_column", self.vertices_data, "vertices_data", False)
        
        self.__awu._validate_input_columns_not_empty(self.edges_data_order_column, "edges_data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.edges_data_order_column, "edges_data_order_column", self.edges_data, "edges_data", False)
        
        
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
        
        if self.weights is not None:
            self.__func_other_arg_sql_names.append("EdgeWeight")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.weights, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.damping is not None and self.damping != 0.85:
            self.__func_other_arg_sql_names.append("DampFactor")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.damping, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.niter is not None:
            self.__func_other_arg_sql_names.append("MaxIterNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.niter, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.eps is not None:
            self.__func_other_arg_sql_names.append("StopThreshold")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.eps, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.vertices_data_sequence_column is not None:
            sequence_input_by_list.append("vertices:" + UtilFuncs._teradata_collapse_arglist(self.vertices_data_sequence_column, ""))
        
        if self.edges_data_sequence_column is not None:
            sequence_input_by_list.append("edges:" + UtilFuncs._teradata_collapse_arglist(self.edges_data_sequence_column, ""))
        
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
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.vertices_data)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("vertices")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.vertices_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.vertices_data_order_column, "\""))
        
        # Process edges_data
        self.edges_data_partition_column = UtilFuncs._teradata_collapse_arglist(self.edges_data_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.edges_data)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("edges")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.edges_data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.edges_data_order_column, "\""))
        
        function_name = "PageRank"
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
        Function to generate AED nodes for output tables.
        This makes a call aed_ml_query() and then output table dataframes are created.
        """
        # Create a list of input node ids contributing to a query.
        self.__input_nodeids = []
        self.__input_nodeids.append(self.vertices_data._nodeid)
        self.__input_nodeids.append(self.edges_data._nodeid)
        
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        self.__func_output_args.insert(0, sqlmr_stdout_temp_tablename)
        try:
            # Call aed_ml_query and generate AED nodes.
            node_id_list = self.__aed_utils._aed_ml_query(self.__input_nodeids, self.sqlmr_query, self.__func_output_args, "PageRank", self.__aqg_obj._multi_query_input_nodes)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.AED_EXEC_FAILED, str(emsg)), MessageCodes.AED_EXEC_FAILED)
        
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=node_id_list[0], metaexpr=UtilFuncs._get_metaexpr_using_columns(node_id_list[0], self.__stdout_column_info))
        self._mlresults.append(self.result)
        
    def __process_output_column_info(self):
        """ 
        Function to process the output schema for all the ouptut tables.
        This function generates list of column names and column types
        for each generated output tables, which can be used to create metaexpr.
        """
        # Collecting STDOUT output column information.
        stdout_column_info_name = []
        stdout_column_info_type = []
        if self.accumulate is not None:
            for column_name, column_type in self.__awu._retrieve_column_info(df_input=self.vertices_data, parameter=self.accumulate, columns=None):
                stdout_column_info_name.append(column_name)
                stdout_column_info_type.append(column_type)
                
        stdout_column_info_name.append("pagerank")
        stdout_column_info_type.append(self.__awu._get_json_to_sqlalchemy_mapping("float"))
        
        self.__stdout_column_info = zip(stdout_column_info_name, stdout_column_info_type)
        
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
        Returns the string representation for a PageRank class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
