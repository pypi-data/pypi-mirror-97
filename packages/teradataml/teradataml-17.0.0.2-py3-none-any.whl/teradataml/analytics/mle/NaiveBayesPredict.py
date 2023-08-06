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
# Function Version: 1.15
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
from teradataml.common.formula import Formula
from teradataml.analytics.mle.NaiveBayes import NaiveBayes

class NaiveBayesPredict:
    
    def __init__(self,
        formula = None,
        modeldata = None,
        newdata = None,
        id_col = None,
        output_prob = False,
        responses = None,
        terms = None,
        newdata_sequence_column = None,
        modeldata_sequence_column = None,
        newdata_order_column = None,
        modeldata_order_column = None):
        """
        DESCRIPTION:
            The NaiveBayesPredict function uses the model output by the
            NaiveBayes function to predict the outcomes for a test set
            of data.
         
            Note: This function is available only when teradataml is connected to
                  Vantage 1.1 or later versions.
         
         
        PARAMETERS:
            formula:
                Optional Argument.
                Required when the argument "modeldata" is teradataml DataFrame.
                Specifies a string consisting of "formula" which was used to fit in model data.
                Only basic formula of the "col1 ~ col2 + col3 +..." form is supported and
                all variables must be from the same virtual DataFrame object. The
                response should be column of type real, numeric, integer or boolean.
                Types: str
         
            modeldata:
                Required Argument.
                Specifies the teradataml DataFrame containing the model data.
                This argument can accept teradataml DataFrame or
                instance of NaiveBayes class.
         
            modeldata_order_column:
                Optional Argument.
                Specifies Order By columns for modeldata.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            newdata:
                Required Argument.
                Specifies the teradataml DataFrame that defines the input test data.
         
            newdata_order_column:
                Optional Argument.
                Specifies Order By columns for newdata.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)
         
            id_col:
                Required Argument.
                Specifies the name of the column that contains the ID that uniquely
                identifies the test input data.
                Types: str
         
            output_prob:
                Optional Argument.
                Specifies whether to output probabilities.
                Default Value: False
                Types: bool
         
            responses:
                Optional Argument.
                Specifies a list of responses to output.
                Note: This argument is required when connected to Vantage prior to Vantage 1.1.1.
                Types: str OR list of Strings (str)
         
            terms:
                Optional Argument.
                Specifies the names of input teradataml DataFrame columns to copy to
                the output teradataml DataFrame.
                Types: str OR list of Strings (str)
         
            newdata_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "newdata". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            modeldata_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "modeldata". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of NaiveBayesPredict.
            Output teradataml DataFrames can be accessed using attribute
            references, such as NaiveBayesPredictObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example
            load_example_data("NaiveBayesPredict",["nb_iris_input_test","nb_iris_input_train"])
         
            # Create teradataml DataFrame objects.
            nb_iris_input_train = DataFrame.from_table("nb_iris_input_train")
            nb_iris_input_test = DataFrame.from_table("nb_iris_input_test")
         
            # Example 1 -
            # We will try to predict the 'species' for the flowers represented
            # by the data points in the train data (nb_iris_input_train).
            naivebayes_train = NaiveBayes(formula="species ~ petal_length + sepal_width + petal_width + sepal_length",
                                          data=nb_iris_input_train)
         
            # Use the generated model to predict the 'species' on the test data
            # nb_iris_input_test by using naivebayes_train which is already
            # in the sparse format.
            naivebayes_predict_result = NaiveBayesPredict(newdata=nb_iris_input_test,
                                        modeldata=naivebayes_train,
                                        newdata_sequence_column=['sepal_width','petal_width'],
                                        id_col='id',
                                        responses=['virginica','setosa','versicolor'],
                                        output_prob=False
                                        )
         
            # Print the result DataFrame
            print(naivebayes_predict_result)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.formula  = formula 
        self.modeldata  = modeldata 
        self.newdata  = newdata 
        self.id_col  = id_col 
        self.output_prob  = output_prob 
        self.responses  = responses 
        self.terms  = terms 
        self.newdata_sequence_column  = newdata_sequence_column 
        self.modeldata_sequence_column  = modeldata_sequence_column 
        self.newdata_order_column  = newdata_order_column 
        self.modeldata_order_column  = modeldata_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["formula", self.formula, True, "formula"])
        self.__arg_info_matrix.append(["modeldata", self.modeldata, False, (DataFrame)])
        self.__arg_info_matrix.append(["modeldata_order_column", self.modeldata_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["newdata", self.newdata, False, (DataFrame)])
        self.__arg_info_matrix.append(["newdata_order_column", self.newdata_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["id_col", self.id_col, False, (str)])
        self.__arg_info_matrix.append(["output_prob", self.output_prob, True, (bool)])
        self.__arg_info_matrix.append(["responses", self.responses, True, (str,list)])
        self.__arg_info_matrix.append(["terms", self.terms, True, (str,list)])
        self.__arg_info_matrix.append(["newdata_sequence_column", self.newdata_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["modeldata_sequence_column", self.modeldata_sequence_column, True, (str,list)])
        
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
        if isinstance(self.modeldata, NaiveBayes):
            self.formula = self.modeldata.formula
            self.modeldata = self.modeldata._mlresults[0]
        elif self.formula is None:
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS, "formula"),
                                      MessageCodes.MISSING_ARGS)
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.newdata, "newdata", None)
        self.__awu._validate_input_table_datatype(self.modeldata, "modeldata", NaiveBayes)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.id_col, "id_col")
        self.__awu._validate_dataframe_has_argument_columns(self.id_col, "id_col", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.terms, "terms")
        self.__awu._validate_dataframe_has_argument_columns(self.terms, "terms", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_sequence_column, "newdata_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_sequence_column, "newdata_sequence_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.modeldata_sequence_column, "modeldata_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.modeldata_sequence_column, "modeldata_sequence_column", self.modeldata, "modeldata", False)
        
        self.__awu._validate_input_columns_not_empty(self.newdata_order_column, "newdata_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.newdata_order_column, "newdata_order_column", self.newdata, "newdata", False)
        
        self.__awu._validate_input_columns_not_empty(self.modeldata_order_column, "modeldata_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.modeldata_order_column, "modeldata_order_column", self.modeldata, "modeldata", False)
        
        
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
        
        self.__func_other_arg_sql_names.append("IDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.id_col, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.terms is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.terms, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.responses is not None:
            self.__func_other_arg_sql_names.append("Responses")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.responses, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.output_prob is not None and self.output_prob != False:
            self.__func_other_arg_sql_names.append("OutputProb")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_prob, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.newdata_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.newdata_sequence_column, ""))
        
        if self.modeldata_sequence_column is not None:
            sequence_input_by_list.append("model:" + UtilFuncs._teradata_collapse_arglist(self.modeldata_sequence_column, ""))
        
        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self.__func_other_args.append(sequence_input_by_arg_value)
            self.__func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value
        
        # Let's process formula argument
        self.formula = self.__awu._validate_formula_notation(self.formula, self.newdata, "formula")
        # Target Column
        self._target_column = self.formula._get_dependent_vars()
        # numerical input columns
        __numeric_columns = self.__awu._get_columns_by_type(self.formula, self.newdata, "numerical")
        if len(__numeric_columns) > 0:
            self.__func_other_arg_sql_names.append("NumericInputs")
            numerical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__numeric_columns, "\""), "'")
            self.__func_other_args.append(numerical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["NumericInputs"] = numerical_columns_list
            self._sql_formula_attribute_mapper["NumericInputs"] = "__numeric_columns"
        
        # categorical input columns
        __categorical_columns = self.__awu._get_columns_by_type(self.formula, self.newdata, "categorical")
        if len(__categorical_columns) > 0:
            self.__func_other_arg_sql_names.append("CategoricalInputs")
            categorical_columns_list = UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(__categorical_columns, "\""), "'")
            self.__func_other_args.append(categorical_columns_list)
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
            self._sql_specific_attributes["CategoricalInputs"] = categorical_columns_list
            self._sql_formula_attribute_mapper["CategoricalInputs"] = "__categorical_columns"
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process newdata
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.newdata, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.newdata_order_column, "\""))
        
        # Process modeldata
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.modeldata, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("model")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.modeldata_order_column, "\""))
        
        function_name = "NaiveBayesPredict"
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
        
        # Initialize the formula attributes.
        __response_column = kwargs.pop("__response_column", None)
        __all_columns = kwargs.pop("__all_columns", None)
        __numeric_columns = kwargs.pop("__numeric_columns", None)
        __categorical_columns = kwargs.pop("__categorical_columns", None)
        
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
        
        # Initialize the formula.
        if obj.formula is not None:
            obj.formula = Formula._from_formula_attr(obj.formula,
                                                     __response_column,
                                                     __all_columns,
                                                     __categorical_columns,
                                                     __numeric_columns)
        
        # Update output table data frames.
        obj._mlresults = []
        obj.result = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.result), source_type="table", database_name=UtilFuncs._extract_db_name(obj.result))
        obj._mlresults.append(obj.result)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a NaiveBayesPredict class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
