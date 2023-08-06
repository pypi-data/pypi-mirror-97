#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# 
# Version: 1.2
# Function Version: 2.8
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

class SVMDense:
    
    def __init__(self,
        data = None,
        sample_id_column = None,
        attribute_columns = None,
        kernel_function = "LINEAR",
        gamma = 1.0,
        constant = 1.0,
        degree = 2,
        subspace_dimension = 512,
        hash_bits = 512,
        label_column = None,
        cost = 1.0,
        bias = 0.0,
        class_weights = None,
        max_step = 10000,
        epsilon = 0.001,
        seed = 0,
        data_sequence_column = None,
        force_mapreduce = False):
        """
        DESCRIPTION:
            The SVMDense function takes training data in dense format and
            outputs a predictive model in binary format, which is input to the
            functions SVMDensePredict and SVMDenseSummary.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains
                the training samples.
            
            sample_id_column:
                Required Argument.
                Specifies the name of the name of the column in data, teradataml DataFrame
                that contains the identifiers of the training samples.
                Types: str
            
            attribute_columns:
                Required Argument.
                Specifies the name of the name of the column in data, teradataml DataFrame
                that contains the attributes of the samples. Attribute columns must have a
                numeric value.
                Types: str OR list of Strings (str)
            
            kernel_function:
                Optional Argument.
                The distribution exponential family used to compute the hash function.
                For linear, a Pegasos algorithm is used to solve the linear SVM.
                For polynomial, RBF, or sigmoid, a Hash-SVM algorithm is used. Each
                sample is represented by compact hash bits, over which an inner
                product is defined to serve as the surrogate of the original
                nonlinear kernels.
                Default Value: "LINEAR"
                Permitted Values: LINEAR, POLYNOMIAL, RBF, SIGMOID
                Types: str
            
            gamma:
                Optional Argument.
                Only used when kernel_function is polynomial, RBF, or sigmoid. A
                positive double that specifies . The minimum value is 0.0.
                Default Value: 1.0
                Types: float
            
            constant:
                Optional Argument.
                Only used when kernel_function is polynomial or sigmoid. A double
                value that specifies c. If kernel_function is polynomial, the minimum
                value is 0.0.
                Default Value: 1.0
                Types: float
            
            degree:
                Optional Argument.
                Only used when kernel_function is polynomial. A positive integer that
                specifies the degree (d) of the polynomial kernel. The input value
                must be greater than 0.
                Default Value: 2
                Types: int
            
            subspace_dimension:
                Optional Argument.
                Only valid if kernel_function is polynomial, RBF, or sigmoid. A positive
                integer that specifies the random subspace dimension of the basis
                matrix V obtained by the Gram-Schmidt process. Since the Gram-Schmidt
                process cannot be parallelized, this dimension cannot be too large.
                Accuracy will increase with higher values of this number, but
                computation costs will also increase. The input value must be in the
                range [1, 2048].
                Note:
                    Argument is ignored when "kernel_function" is 'linear'.
                Default Value: 512
                Types: int
            
            hash_bits:
                Optional Argument.
                Only valid if kernel_function is polynomial, RBF, or sigmoid. A positive
                integer specifying the number of compact hash bits used to represent
                a data point. Accuracy will increase with higher values of this
                number, but computation costs will also increase. The input value
                must be in the range [8, 8192].
                Note:
                    Argument is ignored when "kernel_function" is 'linear'.
                Default Value: 512
                Types: int
            
            label_column:
                Required Argument.
                Column that identifies the class of the corresponding sample. Must be
                an integer or a string.
                Types: str
            
            cost:
                Optional Argument.
                The regularization parameter in the SVM soft-margin loss function.
                Must be greater than 0.0.
                Default Value: 1.0
                Types: float
            
            bias:
                Optional Argument.
                A non-negative value. If the value is greater than zero, each sample
                (x) in the training set will be converted to ( x, b); that is, it
                will add another dimension containing the bias value b. This argument
                addresses situations where not all samples center at 0.
                Default Value: 0.0
                Types: float
            
            class_weights:
                Optional Argument.
                Specifies the weights for different classes. The format should be:
                "classlabel m:weight m, classlabel n:weight n". If weight for a class
                is given, the cost parameter for this class will be weight * cost. A
                weight larger than 1 often increases the accuracy of the
                corresponding class; however, it may decrease global accuracy.
                Classes not assigned a weight in this argument will be assigned a
                weight of 1.0.
                Types: str OR list of Strings (str)
            
            max_step:
                Optional Argument.
                A positive integer value that specifies the maximum number of
                iterations of the training process. One step means that each sample
                is seen once by the trainer. The input value must be in the range [0,
                10000].
                Default Value: 10000
                Types: int
            
            epsilon:
                Optional Argument.
                Termination criterion. When the difference between the values of the
                loss function in two sequential iterations is less than this number,
                the function stops. Must be greater than 0.0.
                Default Value: 0.001
                Types: float
            
            seed:
                Optional Argument.
                A long integer value used to order the training set randomly and
                consistently. This value can be used to ensure that the same model
                will be generated if the function is run multiple times in a given
                database with the same arguments. The input value must be in the
                range [0, 9223372036854775807].
                Default Value: 0
                Types: int
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            force_mapreduce:
                Optional Argument.
                Specifies whether the function is to use MapReduce. If set to
                'False', a lighter version of the function runs for faster results.
                It has no effect without "kernel_function" is 'linear'.
                Note:
                    1. The model may be different with "force_mapreduce" set to 'True' and
                       "force_mapreduce" set to 'False'.
                    2. "force_mapreduce" argument support is only available when teradataml
                       is connected to Vantage 1.3 version.
                Default Value: False
                Types: bool
        
        RETURNS:
            Instance of SVMDense.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SVMDenseObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_table
                2. output
        
        
        RAISES:
            TeradataMlException, TypeError, ValueError
        
        
        EXAMPLES:

            # Load the data to run the example.
            load_example_data("svmdense","nb_iris_input_train")

            # Create teradataml DataFrame objects.
            nb_iris_input_train = DataFrame.from_table("nb_iris_input_train")

            # Example 1 - Linear Model
            svm_dense_out = SVMDense(data = nb_iris_input_train,
                                    sample_id_column = "id",
                                    attribute_columns = ['sepal_length', 'sepal_width' , 'petal_length' , 'petal_width'],
                                    kernel_function = "linear",
                                    label_column = "species",
                                    cost = 1.0,
                                    bias = 0.0,
                                    max_step = 100,
                                    seed = 1
                                    )

            # Print the result DataFrame
            print(svm_dense_out)

            # Example 2 - Polynomial Model
            svm_dense_out = SVMDense(data = nb_iris_input_train,
                                    sample_id_column = "id",
                                    attribute_columns = ['sepal_length', 'sepal_width' , 'petal_length' , 'petal_width'],
                                    kernel_function = "polynomial",
                                    gamma = 0.1,
                                    degree = 2,
                                    subspace_dimension = 120,
                                    hash_bits = 512,
                                    label_column = "species",
                                    cost = 1.0,
                                    bias = 0.0,
                                    max_step = 100,
                                    seed = 1
                                    )

            # Print the result DataFrame
            print(svm_dense_out)

            # Example 3 - Radial Basis Model (RBF) Model
            svm_dense_out = SVMDense(data = nb_iris_input_train,
                                    sample_id_column = "id",
                                    attribute_columns = ['sepal_length', 'sepal_width' , 'petal_length' , 'petal_width'],
                                    kernel_function = "rbf",
                                    gamma = 0.1,
                                    subspace_dimension = 120,
                                    hash_bits = 512,
                                    label_column = "species",
                                    cost = 1.0,
                                    bias = 0.0,
                                    max_step = 100,
                                    seed = 1
                                    )

            # Print the result DataFrame
            print(svm_dense_out)

            # Example 4 - Sigmoid Model
            svm_dense_out = SVMDense(data = nb_iris_input_train,
                                    sample_id_column = "id",
                                    attribute_columns = ['sepal_length', 'sepal_width' , 'petal_length' , 'petal_width'],
                                    kernel_function = "sigmoid",
                                    gamma = 0.1,
                                    subspace_dimension = 120,
                                    hash_bits = 512,
                                    label_column = "species",
                                    cost = 1.0,
                                    bias = 0.0,
                                    max_step = 30,
                                    seed = 1
                                    )

            # Print the result DataFrame
            print(svm_dense_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.sample_id_column  = sample_id_column 
        self.attribute_columns  = attribute_columns 
        self.kernel_function  = kernel_function 
        self.gamma  = gamma 
        self.constant  = constant 
        self.degree  = degree 
        self.subspace_dimension  = subspace_dimension 
        self.hash_bits  = hash_bits 
        self.label_column  = label_column 
        self.cost  = cost 
        self.bias  = bias 
        self.class_weights  = class_weights 
        self.max_step  = max_step 
        self.epsilon  = epsilon 
        self.seed  = seed 
        self.force_mapreduce  = force_mapreduce
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["sample_id_column", self.sample_id_column, False, (str)])
        self.__arg_info_matrix.append(["attribute_columns", self.attribute_columns, False, (str,list)])
        self.__arg_info_matrix.append(["kernel_function", self.kernel_function, True, (str)])
        self.__arg_info_matrix.append(["gamma", self.gamma, True, (float)])
        self.__arg_info_matrix.append(["constant", self.constant, True, (float)])
        self.__arg_info_matrix.append(["degree", self.degree, True, (int)])
        self.__arg_info_matrix.append(["subspace_dimension", self.subspace_dimension, True, (int)])
        self.__arg_info_matrix.append(["hash_bits", self.hash_bits, True, (int)])
        self.__arg_info_matrix.append(["label_column", self.label_column, False, (str)])
        self.__arg_info_matrix.append(["cost", self.cost, True, (float)])
        self.__arg_info_matrix.append(["bias", self.bias, True, (float)])
        self.__arg_info_matrix.append(["class_weights", self.class_weights, True, (str,list)])
        self.__arg_info_matrix.append(["max_step", self.max_step, True, (int)])
        self.__arg_info_matrix.append(["epsilon", self.epsilon, True, (float)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["force_mapreduce", self.force_mapreduce, True, (bool)])
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
        kernel_function_permitted_values = ["LINEAR", "POLYNOMIAL", "RBF", "SIGMOID"]
        self.__awu._validate_permitted_values(self.kernel_function, kernel_function_permitted_values, "kernel_function")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.sample_id_column, "sample_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sample_id_column, "sample_id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_columns, "attribute_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_columns, "attribute_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.label_column, "label_column")
        self.__awu._validate_dataframe_has_argument_columns(self.label_column, "label_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_svmdense0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["ModelTable"]
        self.__func_output_args = [self.__model_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("IdColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.sample_id_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("InputColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.label_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.kernel_function is not None and self.kernel_function != "LINEAR":
            self.__func_other_arg_sql_names.append("KernelFunction")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.kernel_function, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.gamma is not None and self.gamma != 1.0:
            self.__func_other_arg_sql_names.append("Gamma")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.gamma, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.constant is not None and self.constant != 1.0:
            self.__func_other_arg_sql_names.append("Constant")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.constant, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.degree is not None and self.degree != 2:
            self.__func_other_arg_sql_names.append("degree")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.degree, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.subspace_dimension is not None and self.kernel_function.upper() != "LINEAR":
            self.__func_other_arg_sql_names.append("SubspaceDimension")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.subspace_dimension, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.hash_bits is not None and self.kernel_function.upper() != "LINEAR":
            self.__func_other_arg_sql_names.append("HashBits")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.hash_bits, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.force_mapreduce is not None and self.force_mapreduce != False:
            self.__func_other_arg_sql_names.append("ForceMapReduce")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.force_mapreduce, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.cost is not None and self.cost != 1.0:
            self.__func_other_arg_sql_names.append("Cost")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.cost, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.bias is not None and self.bias != 0.0:
            self.__func_other_arg_sql_names.append("Bias")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.bias, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.class_weights is not None:
            self.__func_other_arg_sql_names.append("ClassWeights")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.class_weights, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_step is not None:
            self.__func_other_arg_sql_names.append("MaxStep")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_step, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.epsilon is not None:
            self.__func_other_arg_sql_names.append("Epsilon")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.epsilon, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None and self.seed != 0:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
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
        
        function_name = "SVMDense"
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
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_table)
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
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_table  = model_table 
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
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a SVMDense class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        return repr_string
        
