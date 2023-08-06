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
# Function Version: 2.12
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
from teradataml.analytics.mle.AdaBoost import AdaBoost

class AdaBoostPredict:
    
    def __init__(self,
        object = None,
        newdata = None,
        attr_groupby_columns = None,
        attr_pid_columns = None,
        attr_val_column = None,
        output_response_probdist = False,
        accumulate = None,
        output_responses = None,
        newdata_sequence_column = None,
        object_sequence_column = None,
        newdata_partition_column = None,
        newdata_order_column = None):
        """
        DESCRIPTION:
            The AdaBoostPredict function applies the model output by the
            AdaBoost function to a new data set, outputting predicted labels for each data point.
         
         
        PARAMETERS:
            object:
                Required Argument.
                Specifies the name of the teradataml DataFrame containing the output
                model from AdaBoost or instance of AdaBoost.
         
            newdata:
                Required Argument.
                Specifies the name of the teradataml DataFrame containing the
                attribute names and the values of test data.
         
            newdata_partition_column:
                Required Argument.
                Specifies Partition By columns for newdata.
                Values to this argument can be provided as list, if multiple columns
                are used for partition.
                Required when there are more than one data point identifiers in newdata.
                Types: str OR list of Strings (str)
         
            newdata_order_column:
                Optional Argument.
                Specifies Order By columns for newdata.
                Values to this argument can be provided as list, if multiple columns
                are used for ordering.
                Types: str OR list of Strings (str)
         
            attr_groupby_columns:
                Required Argument.
                Specifies the names of the columns on which the attribute teradataml
                DataFrame is partitioned.
                Types: str
         
            attr_pid_columns:
                Required Argument.
                Specifies the names of the attribute teradataml DataFrame columns
                that contain the data point identifiers.
                Types: str OR list of Strings (str)
         
            attr_val_column:
                Required Argument.
                Specifies the name of the attribute teradataml DataFrame column that
                contains the data point values.
                Types: str
         
            output_response_probdist:
                Optional Argument.
                Specifies whether to output probabilities.
                It can be set to True only when the Adaboost function call used 
                to generate the model had output_response_probdist = True.
                Note: With Vantage version prior to 1.1.1, when this argument is 
                      set to True, need to specify output_responses also.
                Default Value: False
                Types: bool
         
            accumulate:
                Optional Argument.
                Specifies the names of newdata columns to copy to the output
                teradataml DataFrame.
                Types: str OR list of Strings (str)
         
            output_responses:
                Optional Argument.
                Specifies all responses in input teradataml DataFrame.
                This can be used only when both the AdaBoostPredict function, 
                and the Adaboost function call used to generate the model, use(d) 
                output_response_probdist = True.
                This argument requires the output_response_probdist argument to be 
                set to True.
                Types: str OR list of Strings (str)
         
            newdata_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "newdata". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of AdaBoostPredict.
            Output teradataml DataFrames can be accessed using attribute
            references, such as AdaBoostPredictObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("adaboost", ["housing_train", "housing_cat", "housing_train_response", "iris_attribute_train", "iris_response_train"])
            load_example_data("adaboostpredict", ["housing_test", "iris_attribute_test"])
         
            # Create teradataml DataFrame objects.
            housing_train = DataFrame.from_table("housing_train")
            housing_cat = DataFrame.from_table("housing_cat")
            housing_train_response = DataFrame.from_table("housing_train_response")
            iris_attribute_train =  DataFrame.from_table("iris_attribute_train")
            iris_response_train = DataFrame.from_table("iris_response_train")
         
            housing_test = DataFrame.from_table("housing_test")
            iris_attribute_test = DataFrame.from_table("iris_attribute_test")
         
            # Example 1 -
            # Here, we will try to predict the 'homestyle' for the data points in the test data (housing_test)
            # based on the model generated using AdaBoost functions Example #1.
            #
            # First, we will have to run AdaBoost on the input in sparse format.
            # We run Unpivot to be create the input in Sparse format.
            unpivot_out_1 = Unpivot(data=housing_train,
                                    unpivot = ["price", "lotsize", "bedrooms", "bathrms", "stories","driveway", "recroom", "fullbase", "gashw", "airco", "garagepl", "prefarea"],
                                    accumulate = ["sn"])
         
            AdaBoost_out_1 = AdaBoost(attribute_data = unpivot_out_1.result,
                                      attribute_name_columns = ["attribute"],
                                      attribute_value_column = "value_col",
                                      categorical_attribute_data = housing_cat,
                                      response_data = housing_train_response,
                                      id_columns = ["sn"],
                                      response_column = "response",
                                      iter_num = 2,
                                      num_splits = 10,
                                      max_depth = 3,
                                      min_node_size = 100
                                      )
         
            # Use the generated model to predict the house style, on the test data.
            # But we need to transform that too into sparse format
            unpivot_out_2 = Unpivot(data=housing_test,
                                    unpivot = ["price", "lotsize", "bedrooms", "bathrms", "stories","driveway", "recroom", "fullbase", "gashw", "airco", "garagepl", "prefarea"],
                                    accumulate = ["sn"])
         
            AdaBoostPredict_out_1 = AdaBoostPredict(object = AdaBoost_out_1.model_table,
                                                    newdata = unpivot_out_2.result,
                                                    newdata_partition_column = ["sn"],
                                                    attr_groupby_columns = "attribute",
                                                    attr_pid_columns = ["sn"],
                                                    attr_val_column = "value_col"
                                                    )
         
            # Print the results
            print(AdaBoostPredict_out_1)
         
            # Example 2 -
            # In this example, we will try to predict the 'species' for the flowers represented by the data points in the test data (iris_attribute_test)
            # based on the model generated using AdaBoost functions Example #2.
            #
            # First, we will have to run AdaBoost on the input (which is already in sparse format).
            AdaBoost_out_2 = AdaBoost(attribute_data = iris_attribute_train,
                                      attribute_name_columns = ["attribute"],
                                      attribute_value_column = "attrvalue",
                                      response_data = iris_response_train,
                                      id_columns = ["pid"],
                                      response_column = "response",
                                      iter_num = 3,
                                      num_splits = 10,
                                      approx_splits = False,
                                      max_depth = 3,
                                      min_node_size = 5,
                                      output_response_probdist = True
                                      )
         
            # Use the generated model to predict the species, on the test data which is already in the sparse format.
            AdaBoostPredict_out_2 = AdaBoostPredict(object = AdaBoost_out_2.model_table,
                                                    newdata = iris_attribute_test,
                                                    newdata_partition_column = ["pid"],
                                                    attr_groupby_columns = "attribute",
                                                    attr_pid_columns = ["pid"],
                                                    attr_val_column = "attrvalue",
                                                    output_response_probdist = True,
                                                    output_responses = ['          1','          2','          3']
                                                    )
         
            # Print the results
            print(AdaBoostPredict_out_2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.newdata  = newdata 
        self.attr_groupby_columns  = attr_groupby_columns 
        self.attr_pid_columns  = attr_pid_columns 
        self.attr_val_column  = attr_val_column 
        self.output_response_probdist  = output_response_probdist 
        self.accumulate  = accumulate 
        self.output_responses  = output_responses 
        self.newdata_sequence_column  = newdata_sequence_column 
        self.object_sequence_column  = object_sequence_column 
        self.newdata_partition_column  = newdata_partition_column 
        self.newdata_order_column  = newdata_order_column
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["newdata", self.newdata, False, (DataFrame)])
        self.__arg_info_matrix.append(["newdata_partition_column", self.newdata_partition_column, False, (str,list)])
        self.__arg_info_matrix.append(["newdata_order_column", self.newdata_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["attr_groupby_columns", self.attr_groupby_columns, False, (str)])
        self.__arg_info_matrix.append(["attr_pid_columns", self.attr_pid_columns, False, (str,list)])
        self.__arg_info_matrix.append(["attr_val_column", self.attr_val_column, False, (str)])
        self.__arg_info_matrix.append(["output_response_probdist", self.output_response_probdist, True, (bool)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["output_responses", self.output_responses, True, (str,list)])
        self.__arg_info_matrix.append(["newdata_sequence_column", self.newdata_sequence_column, True, (str,list)])
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
        if isinstance(self.object, AdaBoost):
            self.object = self.object._mlresults[0]

        # To use output_responses, output_response_probdist must be set to True
        if self.output_response_probdist is False and self.output_responses is not None:
            raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARG_MISSING,
                                                           'output_response_probdist=True',
                                                           'output_responses'),
                                      MessageCodes.DEPENDENT_ARG_MISSING)
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.newdata, "newdata", None)
        self.__awu._validate_input_table_datatype(self.object, "object", AdaBoost)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.attr_groupby_columns, "attr_groupby_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.attr_groupby_columns, "attr_groupby_columns", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.attr_pid_columns, "attr_pid_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.attr_pid_columns, "attr_pid_columns", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.attr_val_column, "attr_val_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attr_val_column, "attr_val_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_sequence_column, "newdata_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_sequence_column, "newdata_sequence_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_partition_column, "newdata_partition_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_partition_column, "newdata_partition_column", self.newdata, "newdata", True)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_order_column, "newdata_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_order_column, "newdata_order_column", self.newdata, "newdata", False)
        

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
        
        self.__func_other_arg_sql_names.append("AttrTableGroupbyColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attr_groupby_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("AttrTablePidColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attr_pid_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("AttrTableValColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attr_val_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.output_response_probdist is not None and self.output_response_probdist != False:
            self.__func_other_arg_sql_names.append("OutputResponseProbDist")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_response_probdist, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.output_responses is not None:
            self.__func_other_arg_sql_names.append("Responses")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_responses, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.newdata_sequence_column is not None:
            sequence_input_by_list.append("AttributeTable:" + UtilFuncs._teradata_collapse_arglist(self.newdata_sequence_column, ""))
        
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("Model:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
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
        
        # Process newdata
        self.newdata_partition_column = UtilFuncs._teradata_collapse_arglist(self.newdata_partition_column, "\"")
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.newdata, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("AttributeTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append(self.newdata_partition_column)
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.newdata_order_column, "\""))
        
        # Process object
        object_order_column = ["classifier_id", "node_id"]
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("Model")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(object_order_column, "\""))
        
        function_name = "AdaBoostPredict"
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
        Returns the string representation for a AdaBoostPredict class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
