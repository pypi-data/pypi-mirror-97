#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: N Bhavana (bhavana.n@teradata.com)
# 
# Version: 1.2
# Function Version: 1.6
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

class NTree:
    
    def __init__(self,
        data = None,
        root_node = None,
        node_id = None,
        parent_id = None,
        allow_cycles = False,
        starts_with = None,
        mode = None,
        output = None,
        max_distance = 5,
        logging = False,
        result = None,
        data_sequence_column = None,
        data_partition_column = "1",
        data_order_column = None):
        """
        DESCRIPTION:
            The NTree function is a hierarchical analysis SQL-MapReduce function
            that can build and traverse tree structures on all worker machines. 
            The function reads the data only once from the disk and creates the trees in memory.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the input teradataml DataFrame that contains the input table.
            
            data_partition_column:
                Optional Argument.
                Specifies Partition By columns for data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for partition.
                Default Value: 1
                Types: str OR list of Strings (str)
            
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            root_node:
                Required Argument.
                Specifies the bool SQL expression that defines the root nodes of the 
                trees (for example, parent_id IS NULL).
                Types: str
            
            node_id:
                Required Argument.
                Specifies the SQL expression whose value uniquely identifies a node 
                in the input teradataml DataFrame (for example, order_id). 
                Note: A node can appear multiple times in the data set, with 
                      different parents.
                Types: str
         
            parent_id:
                Required Argument.
                Specifies the SQL expression whose value identifies the parent node.
                Types: str
            
            allow_cycles:
                Optional Argument.
                Specifies whether trees can contain cycles. If not, a cycle in the 
                data set causes the function to throw an exception. For information 
                about cycles, refer to "Cycles in NTree"
                Default Value: False
                Types: bool
         
            starts_with:
                Required Argument.
                Specifies the node from which to start tree traversal - must 
                be "root", "leaf ", or a SQL expression that identifies a node.
                Types: str
            
            mode:
                Required Argument.
                Specifies the direction of tree traversal from the start 
                node - up to the root node or down to the leaf nodes.
                Permitted Values: UP, DOWN
                Types: str
            
            output:
                Required Argument.
                Specifies when to output a tuple - at every node along the
                traversal path ("all") or only at the end of the traversal
                path ("end").
                Permitted Values: END, ALL
                Default Value: end
                Types: str
         
            max_distance:
                Optional Argument.
                Specifies the maximum tree depth. 
                Default Value: 5
                Types: int
            
            logging:
                Optional Argument.
                Specifies whether the function prints log messages. 
                Default Value: False
                Types: bool
         
            result:
                Required Argument.
                Specifies aggregate operations to perform during tree traversal. The 
                function reports the result of each aggregate operation in the output 
                table. The syntax of aggregate is: 
                    operation (expression) [ ALIAS alias ] 
                    operation is either PATH, SUM, LEVEL, MAX, MIN, IS_CYCLE, AVG, or 
                PROPAGATE. 
                expression is a SQL expression. If operation is LEVEL or 
                IS_CYCLE, then expression must be *. 
                alias is the name of the output teradataml DataFrame column that 
                contains the result of the operation. The default value is the string 
                "operation(expression)" without the quotation marks. For example, 
                PATH(node_name). 
                Note: The function ignores alias if it is the same as an input 
                      teradataml DataFrame column name.
                For the path from the Starts_With node to the last traversed node, 
                the operations do the following: 
                    1. PATH: Outputs the value of expression for each node, separating 
                values with "->". 
                    2. SUM: Computes the value of expression for each node and outputs the 
                sum of these values. 
                    3. LEVEL: Outputs the number of hops. 
                    4. MAX: Computes the value of expression for each node and outputs the 
                highest of these values. 
                    5. MIN: Computes the value of expression for each node and outputs the 
                lowest of these values. 
                    6. IS_CYCLE: Outputs the cycle (if any). 
                    7. AVG: Computes the value of expression for each node and outputs the 
                average of these values. 
                    8. PROPAGATE: Evaluates expression with the value of the starts_with 
                node and propagates the result to every node.
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of 
                the input argument "data". The argument is used to ensure 
                deterministic results for functions which produce results that vary 
                from run to run.
                Types: str OR list of Strings (str)       
         
        RETURNS:
            Instance of NTree.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as NTreeObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
         
            # Load example data
            load_example_data("ntree", ["employee_table", "emp_table_by_dept"])
            
            # Create teradataml DataFrame objects.
            employee_table = DataFrame.from_table("employee_table")
            emp_table_by_dept = DataFrame.from_table("emp_table_by_dept")
            
            # Example 1 - This example finds the employees who report to employee
            # 100 (either directly or indirectly) by traversing the tree 
            # of employees from employee 100 downward.
            ntree_out1 = NTree(data=employee_table,
                                  root_node = 'mgr_id is NULL',
                                  node_id='emp_id',
                                  parent_id='mgr_id',
                                  starts_with='emp_id=100',
                                  mode='down',
                                  output='end',
                                  result='PATH(emp_name) AS path'
                                 )
                                 
            # Print the result DataFrame
            print(ntree_out1)
            
            # Example 2 - This example finds the reporting structure by department.
            ntree_out2 = NTree(data=emp_table_by_dept,
                                      data_partition_column='department',
                                      root_node = "mgr_id = 'none'",
                                      node_id='id',
                                      parent_id='mgr_id',
                                      starts_with="id=10",
                                      mode='down',
                                      output='all',
                                      result='PATH(name) AS path, PATH(id) as path2'
                                     )
            
            # Print the result DataFrame
            print(ntree_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.root_node  = root_node 
        self.node_id  = node_id 
        self.parent_id  = parent_id 
        self.allow_cycles  = allow_cycles 
        self.starts_with  = starts_with 
        self.mode  = mode 
        self.output  = output 
        self.max_distance  = max_distance 
        self.logging  = logging 
        self.result  = result 
        self.data_sequence_column  = data_sequence_column 
        self.data_partition_column  = data_partition_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_partition_column", self.data_partition_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["root_node", self.root_node, False, (str)])
        self.__arg_info_matrix.append(["node_id", self.node_id, False, (str)])
        self.__arg_info_matrix.append(["parent_id", self.parent_id, False, (str)])
        self.__arg_info_matrix.append(["allow_cycles", self.allow_cycles, True, (bool)])
        self.__arg_info_matrix.append(["starts_with", self.starts_with, False, (str)])
        self.__arg_info_matrix.append(["mode", self.mode, False, (str)])
        self.__arg_info_matrix.append(["output", self.output, False, (str)])
        self.__arg_info_matrix.append(["max_distance", self.max_distance, True, (int)])
        self.__arg_info_matrix.append(["logging", self.logging, True, (bool)])
        self.__arg_info_matrix.append(["result", self.result, False, (str)])
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
        mode_permitted_values = ["UP", "DOWN"]
        self.__awu._validate_permitted_values(self.mode, mode_permitted_values, "mode")
        
        output_permitted_values = ["END", "ALL"]
        self.__awu._validate_permitted_values(self.output, output_permitted_values, "output")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_partition_column, "data_partition_column")
        if self.__awu._is_default_or_not(self.data_partition_column, "1"):
            self.__awu._validate_dataframe_has_argument_columns(self.data_partition_column, "data_partition_column", self.data, "data", True)
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("ROOT_NODE")
        self.__func_other_args.append(self.root_node)
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("NODE_ID")
        self.__func_other_args.append(self.node_id)
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("PARENT_ID")
        self.__func_other_args.append(self.parent_id)
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("MODE")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.mode,"'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.allow_cycles is not None and self.allow_cycles != False:
            self.__func_other_arg_sql_names.append("ALLOW_CYCLES")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.allow_cycles,"'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        self.__func_other_arg_sql_names.append("STARTS_WITH")
        # If starts_with is one of root or leaf, enclose it in quotes else for a SQL expression
        # don't do anything and send it as such
        if self.starts_with.lower == "root" or self.starts_with.lower == "leaf":
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.starts_with,"'"))
        else:
            self.__func_other_args.append(self.starts_with)
        self.__func_other_arg_json_datatypes.append("STRING")
        
        self.__func_other_arg_sql_names.append("OUTPUT")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output,"'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_distance is not None and self.max_distance != 5:
            self.__func_other_arg_sql_names.append("MAX_DISTANCE")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_distance,"'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        self.__func_other_arg_sql_names.append("RESULT")
        self.__func_other_args.append(self.result)
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.logging is not None and self.logging != False:
            self.__func_other_arg_sql_names.append("LOGGING")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.logging,"'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
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
        
        # Process data
        if self.__awu._is_default_or_not(self.data_partition_column, "1"):
            self.data_partition_column = UtilFuncs._teradata_collapse_arglist(self.data_partition_column,"\"")
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
      
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.data_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "NTree"
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
        Returns the string representation for a NTree class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
