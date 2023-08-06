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
# Function Version: 1.31
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

class DecisionTree:
    
    def __init__(self,
        data = None,
        attribute_name_columns = None,
        attribute_value_column = None,
        id_columns = None,
        attribute_table = None,
        response_table = None,
        response_column = None,
        categorical_attribute_table = None,
        splits_table = None,
        split_value = None,
        num_splits = 10,
        approx_splits = True,
        nodesize = 1,
        max_depth = 30,
        weighted = False,
        weight_column = None,
        split_measure = "gini",
        output_response_probdist = False,
        response_probdist_type = "Laplace",
        categorical_encoding = "graycode",
        attribute_table_sequence_column = None,
        data_sequence_column = None,
        categorical_attribute_table_sequence_column = None,
        response_table_sequence_column = None,
        splits_table_sequence_column = None):
        """
        DESCRIPTION:
            The Decision Tree function creates a single decision tree in a
            distributed fashion, either weighted or unweighted. The model teradataml
            DataFrame that this function outputs can be input to the function
            DecisionTreePredict.
         
         
        PARAMETERS:
            data:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                input data set.
                Note: This argument is required if you omit attribute_table
                      and response_table.
         
            attribute_name_columns:
                Required Argument.
                Specifies the names of the attribute teradataml DataFrame columns
                that define the attribute.
                Types: str OR list of Strings (str)
         
            attribute_value_column:
                Required Argument.
                Specifies the names of the attribute teradataml DataFrame columns
                that define the value.
                Types: str
         
            id_columns:
                Required Argument.
                Specifies the names of the columns in the response and attribute
                tables that specify the ID of the instance.
                Types: str OR list of Strings (str)
         
            attribute_table:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                attribute names and the values.
                Note : This argument is required if you omit data.
         
            response_table:
                Optional Argument.
                Specifies the name of the teradataml DataFrame that contains the
                response values.
                Note : This argument is required if you omit data.
         
            response_column:
                Required Argument.
                Specifies the name of the response teradataml DataFrame column that
                contains the response variable.
                Types: str
         
            categorical_attribute_table:
                Optional Argument.
                The name of the input teradataml DataFrame containing the categorical
                attributes.
         
            splits_table:
                Optional Argument.
                Specifies the name of the input teradataml DataFrame that contains
                the user-specified splits. By default, the function creates new
                splits.
         
            split_value:
                Optional Argument.
                If you specify splits_table, this argument specifies the name of the
                column that contains the split value. If approx_splits is "true",
                then the default value is splits_valcol; if not, then the default
                value is the attribute_value_column argument, node_column.
                Types: str
         
            num_splits:
                Optional Argument.
                Specifies the number of splits to consider for each variable. The
                function does not consider all possible splits for all attributes.
                Default Value: 10
                Types: int
         
            approx_splits:
                Optional Argument.
                Specifies whether to use approximate percentiles (true) or exact
                percentiles (false). Internally, the function uses percentile values
                as split values.
                Default Value: True
                Types: bool
         
            nodesize:
                Optional Argument.
                Specifies the decision tree stopping criteria and the minimum size
                of any particular node within each decision tree.
                Default Value: 1
                Types: int
         
            max_depth:
                Optional Argument.
                Specifies a decision tree stopping criteria. If the tree reaches a
                depth past this value, the algorithm stops looking for splits.
                Decision trees can grow up to (2(max_depth+1) - 1) nodes. This
                stopping criteria has the greatest effect on function performance.
                The maximum value is 60.
                Default Value: 30
                Types: int
         
            weighted:
                Optional Argument.
                Specifies whether to build a weighted decision tree. If you specify
                "true", then you must also specify the weight_column argument.
                Default Value: False
                Types: bool
         
            weight_column:
                Optional Argument.
                Specifies the name of the response teradataml DataFrame column that
                contains the weights of the attribute values.
                Types: str
         
            split_measure:
                Optional Argument.
                Specifies the impurity measurement to use while constructing the
                decision tree.
                Default Value: "gini"
                Permitted Values: GINI, ENTROPY, CHISQUARE
                Types: str
         
            output_response_probdist:
                Optional Argument.
                Specifies switch to enable or disable output of probability
                distribution for output labels.
                Note: 'output_response_probdist' argument can accept input value True
                      only when teradataml is connected to Vantage 1.0 Maintenance
                Update 2 version or later.
                Default Value: False
                Types: bool
         
            response_probdist_type:
                Optional Argument.
                Specifies the type of algorithm to use to generate output probability
                distribution for output labels. Uses one of Laplace, Frequency or
                RawCounts to generate Probability Estimation Trees (PET) based
                distributions.
                Note: This argument can only be used when output_response_probdist is
                      set to True.
                Default Value: "Laplace"
                Permitted Values: Laplace, Frequency, RawCount
                Types: str
         
            categorical_encoding:
                Optional Argument.
                Specifies which encoding method is used for categorical variables.
                Note: categorical_encoding argument support is only available
                      when teradataml is connected to Vantage 1.1 or later.
                Default Value: "graycode"
                Permitted Values: graycode, hashing
                Types: str
         
            attribute_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "attribute_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            categorical_attribute_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "categorical_attribute_table". The argument is
                used to ensure deterministic results for functions which produce
                results that vary from run to run.
                Types: str OR list of Strings (str)
         
            response_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "response_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            splits_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "splits_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of DecisionTree.
            Output teradataml DataFrames can be accessed using attribute
            references, such as DecisionTreeObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_table
                2. intermediate_splits_table
                3. final_response_tableto
                4. output
         
            Note: When argument splits_table is used, output teradataml DataFrame,
                  intermediate_splits_table, is not created. If tried to access this
                  attribute an AttributeError will be raised.
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("DecisionTree", ["iris_attribute_train", "iris_response_train", "iris_altinput"])
         
            # Create teradataml DataFrame
            iris_attribute_train = DataFrame.from_table("iris_attribute_train")
            iris_altinput = DataFrame.from_table("iris_altinput")
            iris_response_train = DataFrame.from_table("iris_response_train")
         
            # Example 1 -
            sdt_out1 = DecisionTree(attribute_name_columns = 'attribute',
                                    attribute_value_column = 'attrvalue',
                                    id_columns = 'pid',
                                    attribute_table = iris_attribute_train,
                                    response_table = iris_response_train,
                                    response_column = 'response',
                                    approx_splits = True,
                                    nodesize = 100,
                                    max_depth = 5,
                                    weighted = False,
                                    split_measure = "gini",
                                    output_response_probdist = False)
         
            # Print the result DataFrame
            print(sdt_out1.model_table)
            print(sdt_out1.intermediate_splits_table)
            print(sdt_out1.final_response_tableto)
            print(sdt_out1.output)
         
         
            # Example 2 -
            sdt_out2 = DecisionTree(data = iris_altinput,
                                    attribute_name_columns = 'attribute',
                                    attribute_value_column = 'attrvalue',
                                    id_columns = 'pid',
                                    response_column = 'response',
                                    num_splits = 10,
                                    nodesize = 100,
                                    max_depth = 5,
                                    weighted = False,
                                    split_measure = "gini",
                                    output_response_probdist = False,
                                    response_probdist_type = "Laplace")
         
            # Print the result DataFrame
            print(sdt_out2.model_table)
            print(sdt_out2.intermediate_splits_table)
            print(sdt_out2.final_response_tableto)
            print(sdt_out2.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.attribute_name_columns  = attribute_name_columns 
        self.attribute_value_column  = attribute_value_column 
        self.id_columns  = id_columns 
        self.attribute_table  = attribute_table 
        self.response_table  = response_table 
        self.response_column  = response_column 
        self.categorical_attribute_table  = categorical_attribute_table 
        self.splits_table  = splits_table 
        self.split_value  = split_value 
        self.num_splits  = num_splits 
        self.approx_splits  = approx_splits 
        self.nodesize  = nodesize 
        self.max_depth  = max_depth 
        self.weighted  = weighted 
        self.weight_column  = weight_column 
        self.split_measure  = split_measure 
        self.output_response_probdist  = output_response_probdist 
        self.response_probdist_type  = response_probdist_type 
        self.categorical_encoding  = categorical_encoding 
        self.attribute_table_sequence_column  = attribute_table_sequence_column 
        self.data_sequence_column  = data_sequence_column 
        self.categorical_attribute_table_sequence_column  = categorical_attribute_table_sequence_column 
        self.response_table_sequence_column  = response_table_sequence_column 
        self.splits_table_sequence_column  = splits_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, True, (DataFrame)])
        self.__arg_info_matrix.append(["attribute_name_columns", self.attribute_name_columns, False, (str,list)])
        self.__arg_info_matrix.append(["attribute_value_column", self.attribute_value_column, False, (str)])
        self.__arg_info_matrix.append(["id_columns", self.id_columns, False, (str,list)])
        self.__arg_info_matrix.append(["attribute_table", self.attribute_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["response_table", self.response_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["response_column", self.response_column, False, (str)])
        self.__arg_info_matrix.append(["categorical_attribute_table", self.categorical_attribute_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["splits_table", self.splits_table, True, (DataFrame)])
        self.__arg_info_matrix.append(["split_value", self.split_value, True, (str)])
        self.__arg_info_matrix.append(["num_splits", self.num_splits, True, (int)])
        self.__arg_info_matrix.append(["approx_splits", self.approx_splits, True, (bool)])
        self.__arg_info_matrix.append(["nodesize", self.nodesize, True, (int)])
        self.__arg_info_matrix.append(["max_depth", self.max_depth, True, (int)])
        self.__arg_info_matrix.append(["weighted", self.weighted, True, (bool)])
        self.__arg_info_matrix.append(["weight_column", self.weight_column, True, (str)])
        self.__arg_info_matrix.append(["split_measure", self.split_measure, True, (str)])
        self.__arg_info_matrix.append(["output_response_probdist", self.output_response_probdist, True, (bool)])
        self.__arg_info_matrix.append(["response_probdist_type", self.response_probdist_type, True, (str)])
        self.__arg_info_matrix.append(["categorical_encoding", self.categorical_encoding, True, (str)])
        self.__arg_info_matrix.append(["attribute_table_sequence_column", self.attribute_table_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["categorical_attribute_table_sequence_column", self.categorical_attribute_table_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["response_table_sequence_column", self.response_table_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["splits_table_sequence_column", self.splits_table_sequence_column, True, (str,list)])
        
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
        self.__awu._validate_input_table_datatype(self.attribute_table, "attribute_table", None)
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        self.__awu._validate_input_table_datatype(self.categorical_attribute_table, "categorical_attribute_table", None)
        self.__awu._validate_input_table_datatype(self.response_table, "response_table", None)
        self.__awu._validate_input_table_datatype(self.splits_table, "splits_table", None)

        # Make sure either of the input tables are provided
        if ((self.data is None and (self.attribute_table is None or self.response_table is None)) or
                (self.data is not None and (self.attribute_table is not None or self.response_table is not None))):
            raise TeradataMlException(Messages.get_message(MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, "data",
                                                           "attribute_table and response_table"),
                                      MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)

        # Check for permitted values
        split_measure_permitted_values = ["GINI", "ENTROPY", "CHISQUARE"]
        self.__awu._validate_permitted_values(self.split_measure, split_measure_permitted_values, "split_measure")
        
        response_probdist_type_permitted_values = ["LAPLACE", "FREQUENCY", "RAWCOUNT"]
        self.__awu._validate_permitted_values(self.response_probdist_type, response_probdist_type_permitted_values, "response_probdist_type")
        
        categorical_encoding_permitted_values = ["GRAYCODE", "HASHING"]
        self.__awu._validate_permitted_values(self.categorical_encoding, categorical_encoding_permitted_values, "categorical_encoding")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        if self.data is not None:
            input_data = self.data
            input_data_arg_name = "data"
        else:
            input_data = self.attribute_table
            input_data_arg_name = "attribute_table"

        self.__awu._validate_input_columns_not_empty(self.attribute_name_columns, "attribute_name_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_name_columns, "attribute_name_columns", input_data, input_data_arg_name, False)
        
        self.__awu._validate_input_columns_not_empty(self.id_columns, "id_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.id_columns, "id_columns", input_data, input_data_arg_name, False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_value_column, "attribute_value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_value_column, "attribute_value_column", input_data, input_data_arg_name, False)

        if self.data is None:
            input_data = self.response_table
            input_data_arg_name = "response_table"

        self.__awu._validate_input_columns_not_empty(self.response_column, "response_column")
        self.__awu._validate_dataframe_has_argument_columns(self.response_column, "response_column", input_data, input_data_arg_name, False)
        
        self.__awu._validate_input_columns_not_empty(self.split_value, "split_value")
        self.__awu._validate_dataframe_has_argument_columns(self.split_value, "split_value", self.splits_table, "splits_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.weight_column, "weight_column")
        self.__awu._validate_dataframe_has_argument_columns(self.weight_column, "weight_column", input_data, input_data_arg_name, False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_table_sequence_column, "attribute_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_table_sequence_column, "attribute_table_sequence_column", self.attribute_table, "attribute_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.categorical_attribute_table_sequence_column, "categorical_attribute_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.categorical_attribute_table_sequence_column, "categorical_attribute_table_sequence_column", self.categorical_attribute_table, "categorical_attribute_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.response_table_sequence_column, "response_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.response_table_sequence_column, "response_table_sequence_column", self.response_table, "response_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.splits_table_sequence_column, "splits_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.splits_table_sequence_column, "splits_table_sequence_column", self.splits_table, "splits_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_decisiontree0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__intermediate_splits_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_decisiontree1", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        self.__final_response_tableto_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_decisiontree2", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        if (self.splits_table is None):
            self.__func_output_args_sql_names = ["OutputTable", "IntermediateSplitsTable", "SaveFinalResponseTableTo"]
            self.__func_output_args = [self.__model_table_temp_tablename, self.__intermediate_splits_table_temp_tablename, self.__final_response_tableto_temp_tablename]
        else:
            self.__func_output_args_sql_names = ["OutputTable", "SaveFinalResponseTableTo"]
            self.__func_output_args = [self.__model_table_temp_tablename, self.__final_response_tableto_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("AttributeNameColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_name_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("IdColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("AttributeValueColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_value_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.response_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.split_value is not None:
            self.__func_other_arg_sql_names.append("SplitsValueColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.split_value, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.weight_column is not None:
            self.__func_other_arg_sql_names.append("WeightColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.weight_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.num_splits is not None and self.num_splits != 10:
            self.__func_other_arg_sql_names.append("NumSplits")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.num_splits, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.approx_splits is not None and self.approx_splits != True:
            self.__func_other_arg_sql_names.append("ApproxSplits")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.approx_splits, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.nodesize is not None:
            self.__func_other_arg_sql_names.append("MinNodeSize")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.nodesize, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.max_depth is not None:
            self.__func_other_arg_sql_names.append("MaxDepth")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_depth, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.split_measure is not None and self.split_measure != "gini":
            self.__func_other_arg_sql_names.append("SplitMeasure")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.split_measure, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.weighted is not None and self.weighted != False:
            self.__func_other_arg_sql_names.append("Weighted")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.weighted, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.output_response_probdist is not None and self.output_response_probdist != False:
            self.__func_other_arg_sql_names.append("OutputResponseProbDist")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_response_probdist, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.response_probdist_type is not None and self.response_probdist_type != "Laplace":
            self.__func_other_arg_sql_names.append("ResponseProbDistType")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.response_probdist_type, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.categorical_encoding is not None and self.categorical_encoding != "graycode":
            self.__func_other_arg_sql_names.append("CategoricalEncoding")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.categorical_encoding, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.attribute_table_sequence_column is not None:
            sequence_input_by_list.append("AttributeTableName:" + UtilFuncs._teradata_collapse_arglist(self.attribute_table_sequence_column, ""))
        
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.categorical_attribute_table_sequence_column is not None:
            sequence_input_by_list.append("CategoricalAttributeTableName:" + UtilFuncs._teradata_collapse_arglist(self.categorical_attribute_table_sequence_column, ""))
        
        if self.response_table_sequence_column is not None:
            sequence_input_by_list.append("ResponseTableName:" + UtilFuncs._teradata_collapse_arglist(self.response_table_sequence_column, ""))
        
        if self.splits_table_sequence_column is not None:
            sequence_input_by_list.append("SplitsTable:" + UtilFuncs._teradata_collapse_arglist(self.splits_table_sequence_column, ""))
        
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
        
        # Process attribute_table
        if self.attribute_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.attribute_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("AttributeTableName")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process data
        if self.data is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("InputTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process categorical_attribute_table
        if self.categorical_attribute_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.categorical_attribute_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("CategoricalAttributeTableName")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process response_table
        if self.response_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.response_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("ResponseTableName")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        # Process splits_table
        if self.splits_table is not None:
            self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.splits_table, False)
            self.__func_input_distribution.append("NONE")
            self.__func_input_arg_sql_names.append("SplitsTable")
            self.__func_input_table_view_query.append(self.__table_ref["ref"])
            self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
            self.__func_input_partition_by_cols.append("NA_character_")
            self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "DecisionTree"
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
        if self.splits_table is None:
            self.intermediate_splits_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__intermediate_splits_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__intermediate_splits_table_temp_tablename))
        self.final_response_tableto = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__final_response_tableto_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__final_response_tableto_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_table)
        if self.splits_table is None:
            self._mlresults.append(self.intermediate_splits_table)
        self._mlresults.append(self.final_response_tableto)
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
        final_response_tableto = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_table", None)
        intermediate_splits_table = None
        if "intermediate_splits_table" in kwargs.keys():
            intermediate_splits_table = kwargs["intermediate_splits_table"]
        kwargs.pop("intermediate_splits_table", None)
        kwargs.pop("final_response_tableto", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_table  = model_table 
        obj.intermediate_splits_table  = intermediate_splits_table 
        obj.final_response_tableto  = final_response_tableto 
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
        if intermediate_splits_table is not None:
            obj.intermediate_splits_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.intermediate_splits_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.intermediate_splits_table))
        obj.final_response_tableto = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.final_response_tableto), source_type="table", database_name=UtilFuncs._extract_db_name(obj.final_response_tableto))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        if intermediate_splits_table is not None:
            obj._mlresults.append(obj.intermediate_splits_table)
        obj._mlresults.append(obj.final_response_tableto)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a DecisionTree class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        if self.splits_table is None:
            repr_string="{}\n\n\n############ intermediate_splits_table Output ############".format(repr_string)
            repr_string = "{}\n\n{}".format(repr_string,self.intermediate_splits_table)
        repr_string="{}\n\n\n############ final_response_tableto Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.final_response_tableto)
        return repr_string
        
