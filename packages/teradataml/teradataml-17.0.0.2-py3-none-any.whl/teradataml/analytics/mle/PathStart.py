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
from teradataml.analytics.mle.PathSummarizer import PathSummarizer

class PathStart:
    
    def __init__(self,
        object = None,
        count_column = None,
        delimiter = ",",
        parent_column = None,
        partition_names = None,
        node_column = None,
        object_sequence_column = None,
        object_partition_column = None,
        object_order_column = None):
        """
        DESCRIPTION:
            The PathStart function takes output of the function PathSummarizer 
            and returns, for each parent in the input teradataml DataFrame, the parent and
            children and the number of times that each of its sub-sequences was
            traveled.


        PARAMETERS:
            object:
                Required Argument.
                The name of the teradataml DataFrame containing the input data.

            object_partition_column:
                Required Argument.
                Specifies Partition By columns for object.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Types: str OR list of Strings (str)

            object_order_column:
                Optional Argument.
                Specifies Order By columns for object.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)

            count_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the number of times a path was traveled.
                Types: str

            delimiter:
                Optional Argument.
                Specifies the single-character delimiter that separates symbols in
                the path string.
                Note: Do not use any of the following characters as delimiter (they
                      cause the function to fail):
                          Asterisk (*), Plus (+), Left parenthesis ((),
                          Right parenthesis ()), Single quotation mark ('),
                          Escaped single quotation mark (\\'), Backslash (\\).
                Default Value: ","
                Types: str

            parent_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the parent nodes. The object_partition_column argument in the
                function call must include this column.
                Types: str

            partition_names:
                Required Argument.
                Lists the names of the columns that the object_partition_column argument
                specifies. The function uses these names for output teradataml
                DataFrame columns. This argument and the object_partition_column argument
                must specify the same names in the same order. One object_partition_column
                must be parent_column.
                Types: str OR list of strs

            node_column:
                Required Argument.
                Specifies the name of the input teradataml DataFrame column that
                contains the nodes.
                Types: str

            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of PathStart.
            Output teradataml DataFrames can be accessed using attribute
            references, such as PathStartObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException


        EXAMPLES:
            # Load example data.
            load_example_data("pathgenerator", "clickstream1")

            # Create teradataml DataFrame objects.
            # The table contains clickstream data, where the "path" column
            # contains symbols for the pages that the customer clicked.
            clickstream1 = DataFrame.from_table("clickstream1")

            # Example 1 - PathStart uses the output of PathSummarizer.
            PathGeneratorOut = PathGenerator(data = clickstream1,
                                              seq_column = "path"
                                              )

            PathSummarizerOut = PathSummarizer(object = PathGeneratorOut,
                                                object_partition_column = ['prefix'],
                                                seq_column = 'sequence',
                                                partition_names = 'prefix',
                                                prefix_column = 'prefix'
                                                )

            PathStartOut1 = PathStart(object=PathSummarizerOut,
                                      object_partition_column='parent',
                                      node_column='node',
                                      parent_column='parent',
                                      count_column='cnt',
                                      partition_names='partitioned'
                                      )
            # Print the results
            print(PathStartOut1)

            # Example 2 - Alternatively, persist and use the output table of PathSummarizer.
            copy_to_sql(PathSummarizerOut.result, "generated_summarized_path_table")
            generated_summarized_path_table = DataFrame.from_table("generated_summarized_path_table")

            PathStartOut2 = PathStart(object=generated_summarized_path_table,
                                      object_partition_column='parent',
                                      node_column='node',
                                      parent_column='parent',
                                      count_column='cnt',
                                      partition_names='partitioned'
                                      )
            # Print the results
            print(PathStartOut2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.count_column  = count_column 
        self.delimiter  = delimiter 
        self.parent_column  = parent_column 
        self.partition_names  = partition_names 
        self.node_column  = node_column 
        self.object_sequence_column  = object_sequence_column 
        self.object_partition_column  = object_partition_column 
        self.object_order_column  = object_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["object_partition_column", self.object_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["object_order_column", self.object_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["count_column", self.count_column, False, (str)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["parent_column", self.parent_column, False, (str)])
        self.__arg_info_matrix.append(["partition_names", self.partition_names, False, (str,list)])
        self.__arg_info_matrix.append(["node_column", self.node_column, False, (str)])
        self.__arg_info_matrix.append(["object_sequence_column", self.object_sequence_column, True, (str,list)])
        
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
        if isinstance(self.object, PathSummarizer):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.object, "object", PathSummarizer)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.node_column, "node_column")
        self.__awu._validate_dataframe_has_argument_columns(self.node_column, "node_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.parent_column, "parent_column")
        self.__awu._validate_dataframe_has_argument_columns(self.parent_column, "parent_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.count_column, "count_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_column, "count_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_partition_column, "object_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_partition_column, "object_partition_column", self.object, "object", True)
        
        self.__awu._validate_input_columns_not_empty(self.object_order_column, "object_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_order_column, "object_order_column", self.object, "object", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.partition_names, "partition_names")
        
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
        
        self.__func_other_arg_sql_names.append("NodeColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.node_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ParentColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.parent_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("CountColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.count_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("PartitionNames")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.partition_names, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.delimiter is not None and self.delimiter != ",":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
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
        
        # Process object
        self.object_partition_column = UtilFuncs._teradata_collapse_arglist(self.object_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.object_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.object_order_column, "\""))
        
        function_name = "PathStart"
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
        Returns the string representation for a PathStart class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
