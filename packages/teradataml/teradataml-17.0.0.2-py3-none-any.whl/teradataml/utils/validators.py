import numbers
import os
from pathlib import Path
import re
from teradataml.common.constants import TeradataConstants, PTITableConstants
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import MessageCodes, Messages
from teradataml.utils.dtypes import _Dtypes

class _Validators:
    """
    A class containing set of utilities that can be used for validations of various kinds.
    Currently, this facilitates the validations done for:
        1. Analytic function execution engine: (_validate_engine)
        2. Validation for the vantage_version: (_validate_vantage_version)
        3. Validate whether argument has passed with empty string or not: (_validate_input_columns_not_empty)
        4. Validate for permitted values of the argument: (_validate_permitted_values)
        5. Validate function arguments. (_validate_function_arguments) This specifically validates for
            1. Argument types check.
            2. Argument is empty or not.
            3. Permitted values check.
        6. Validate for missing required arguments.
        7. Validate column exists in a DataFrame or not. (_validate_column_exists_in_dataframe)
        8. Validate required arguments are missing or not. (_validate_missing_required_arguments)
    """
    @staticmethod
    def __getTypeAsStr(type_list):
        """
        Function to convert type to string.

        PARAMETERS:
            type_list
                Required Argument.
                A tuple of types or a type to be converted to string.

        RAISES:
            None

        RETURNS:
            A list of strings representing types in type_list.

        EXAMPLES:
            _Validators.__getTypeAsStr(type_list)
        """
        type_as_str = []
        if isinstance(type_list, tuple):
            for typ in type_list:
                if isinstance(typ, tuple):
                    for typ1 in typ:
                        type_as_str.append(typ1.__name__)
                elif typ.__name__ == "DataFrame":
                    type_as_str.append("teradataml DataFrame")
                else:
                    type_as_str.append(typ.__name__)

        if isinstance(type_list, type):
            if type_list.__name__ == "DataFrame":
                type_as_str.append("teradataml DataFrame")
            else:
                type_as_str.append(type_list.__name__)

        return type_as_str

    @staticmethod
    def _check_isinstance(obj, class_or_tuple):
        """
        Function checks whether an object is an instance of a class.

        PARAMETER
            obj:
                Required Argument.
                Specifies the object to check instance of.

            class_or_tuple:
                Required Argument.
                Specifies the type or tuple of types to check instance against.

        RAISES:
            None.

        RETURNS:
            True, if obj is instance of class_or_tuple

        EXAMPLES:
            _Validators._check_isinstance(obj, (int, list, str))
        """
        # If obj is of type bool and type to check against contains int, then we  must
        # check/validate the instance as type(obj) == class_or_tuple.
        # bool is subclass of int, hence isinstance(True, int) will always return true.
        # And we would like to return false, as bool is not a int.
        if not isinstance(obj, bool):
            # If obj of any type other than bool, then we shall use "isinstance()"
            # to perform type checks.
            return isinstance(obj, class_or_tuple)

        else:
            # 'obj' is of type bool.
            if isinstance(class_or_tuple, tuple):
                if int not in class_or_tuple:
                    # If class_or_tuple is instance of tuple and int is not in class_or_tuple
                    # use "isinstance()" to validate type check for obj.
                    return isinstance(obj, class_or_tuple)
                else:
                    return type(obj) in class_or_tuple

            else:  # isinstance(class_or_tuple, type):
                if int != class_or_tuple:
                    # If class_or_tuple is instance of type and class_or_tuple is not an int
                    # use "isinstance()" to validate type check for obj.
                    return isinstance(obj, class_or_tuple)
                else:
                    return type(obj) == class_or_tuple

    @staticmethod
    def _validate_dataframe_has_argument_columns(columns, column_arg, data, data_arg, is_partition_arg=False):
        """
        Function to check whether column names in columns are present in given dataframe or not.
        This function is used currently only for Analytics wrappers.

        PARAMETERS:
            columns:
                Required Argument.
                Specifies name or list of names of columns to be validated for existence.
                Types: str or List of strings

            column_arg:
                Required Argument.
                Specifies the name of the argument.
                Types: str

            data:
                Required Argument.
                Specifies teradataml DataFrame to check against for column existence.
                Types: teradataml DataFrame

            data_arg:
                Required Argument.
                Specifies the name of the dataframe argument.
                Types: str

            isPartitionArg:
                Optional Argument.
                Specifies a bool argument notifying, whether argument being validate is
                Partition argument or not.
                Types: bool

        RAISES:
            TeradataMlException - TDMLDF_COLUMN_IN_ARG_NOT_FOUND column(s) does not exist in a dataframe.

        EXAMPLES:
            _Validators._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data")
            _Validators._validate_dataframe_has_argument_columns(self.data_partition_column, "data_sequence_column", self.data, "data", true)
        """
        if is_partition_arg and columns is None:
            return True

        if columns is None:
            return True

        if data is None and columns is not None:
            raise TeradataMlException(Messages.get_message(MessageCodes.DEPENDENT_ARGUMENT, column_arg, data_arg),
                                      MessageCodes.DEPENDENT_ARGUMENT)

        # Converting columns to a list if string is passed.
        if not isinstance(columns, list) and columns is not None:
            columns = [columns]

        total_columns = []
        # Add new column range separators to this list.
        valid_separators = [":"]
        for column in columns:
            for separator in valid_separators:
                if column is None:
                    total_columns.append(column)
                elif separator in column:
                    column_names = column.split(separator)
                    if len(column_names) != 2:
                        # Raises Exception as column range has more than 2 boundaries.
                        err_msg = Messages.get_message(MessageCodes.INVALID_COLUMN_RANGE_FORMAT)
                        raise ValueError(err_msg.format(column_arg))
                    if all([column_names[0].isdigit(), column_names[1].isdigit()]):
                        # If both are indices then ignore and let database handle the validations.
                        continue
                    elif any([column_names[0].isdigit(), column_names[1].isdigit()]):
                        # Raises Exception if column range has mixed types.
                        err_msg = Messages.get_message(MessageCodes.MIXED_TYPES_IN_COLUMN_RANGE)
                        raise ValueError(err_msg.format(column_arg))
                    else:
                        total_columns.extend(column_names)
                else:
                    total_columns.append(column)

        return _Validators._validate_column_exists_in_dataframe(total_columns, data._metaexpr, column_arg=column_arg,
                                                                data_arg=data_arg)

    @staticmethod
    def _validate_column_exists_in_dataframe(columns, metaexpr, case_insensitive=False, column_arg=None,
                                             data_arg=None):
        """
        Method to check whether column or list of columns exists in a teradataml DataFrame or not.

        PARAMETERS:
            columns:
                Required Argument.
                Specifies name or list of names of columns to be validated for existence.
                Types: str or List of strings

            metaexpr:
                Required Argument.
                Specifies a teradataml DataFrame metaexpr to be validated against.
                Types: MetaExpression

            case_insensitive:
                Optional Argument.
                Specifies a flag, that determines whether to check for column existence in
                case_insensitive manner or not.
                Default Value: False (Case-Sensitive lookup)
                Types: bool

            column_arg:
                Optional Argument.
                Specifies the name of the argument.
                Types: str

            data_arg:
                Optional Argument.
                Specifies the name of the dataframe argument.
                Types: str

        RAISES:
            ValueError
                TDMLDF_DROP_INVALID_COL - If columns not found in metaexpr.

        RETURNS:
            None

        EXAMPLES:
            _Validators._validate_column_exists_in_dataframe(["col1", "col2"], self.metaexpr)

        """
        if columns is None:
            return True

        # If just a column name is passed, convert it to a list.
        if isinstance(columns, str):
            columns = [columns]

        # Constructing New unquotted column names for selected columns ONLY using Parent _metaexpr
        if case_insensitive:
            # If lookup has to be a case insensitive then convert the
            # metaexpr columns name to lower case.
            unquoted_df_columns = [c.name.replace('"', "").lower() for c in metaexpr.c]
        else:
            unquoted_df_columns = [c.name.replace('"', "") for c in metaexpr.c]

        # Let's validate existence of each column one by one.
        for column_name in columns:
            if column_name is None:
                column_name = str(column_name)

            if case_insensitive:
                # If lookup has to be a case insensitive then convert the
                # column name to lower case.
                column_name = column_name.lower()

            # If column name does not exist in metaexpr, raise the exception
            if not column_name.replace('"', "") in unquoted_df_columns:
                if column_arg and data_arg:
                    raise ValueError(Messages.get_message(MessageCodes.TDMLDF_COLUMN_IN_ARG_NOT_FOUND,
                                                          column_name, column_arg, data_arg))
                else:
                    raise ValueError(Messages.get_message(MessageCodes.TDMLDF_DROP_INVALID_COL,
                                                          column_name, sorted(unquoted_df_columns)))

        return True

    @staticmethod
    def _validate_engine(engine):
        """
        Function to validate whether the argument engine is supported or not.

        PARAMETERS:
            engine:
                Required Argument.
                Specifies the type of the engine.

        RETURNS:
            True, if engine is supported.

        RAISES:
            TeradataMLException

        EXAMPLES:
            _Validators._validate_engine("ENGINE_SQL")
        """
        supported_engines = TeradataConstants.SUPPORTED_ENGINES.value
        if engine not in supported_engines.keys():
            raise TeradataMlException(Messages.get_message(
                MessageCodes.CONFIG_ALIAS_ENGINE_NOT_SUPPORTED).format(engine,
                                                                       ", ".join(supported_engines.keys())),
                                      MessageCodes.CONFIG_ALIAS_ENGINE_NOT_SUPPORTED)

        return True

    @staticmethod
    def _validate_function_arguments(arg_list, skip_empty_check = None):
        """
        Method to verify that the input arguments are of valid data type except for
        argument of DataFrameType.

        PARAMETERS:
            arg_list:
                Required Argument.
                Specifies a list of arguments, expected types are mentioned as type or tuple.
                       argInfoMatrix = []
                       argInfoMatrix.append(["data", data, False, (DataFrame)])
                       argInfoMatrix.append(["centers", centers, True, (int, list)])
                       argInfoMatrix.append(["threshold", threshold, True, (float)])
                Types: List of Lists
            skip_empty_check:
                Optional Argument.
                Specifies column name and values for which to skip check.
                Types: Dictionary specifying column name to values mapping.

        RAISES:
            Error if arguments are not of valid datatype

        EXAMPLES:
            _Validators._validate_function_arguments(arg_list)
        """
        invalid_arg_names = []
        invalid_arg_types = []

        typeCheckFailed = False

        for args in arg_list:
            num_args = len(args)
            if not isinstance(args[0], str):
                raise TypeError("First element in argument information matrix should be str.")

            if not isinstance(args[2], bool):
                raise TypeError("Third element in argument information matrix should be bool.")

            if not (isinstance(args[3], tuple) or isinstance(args[3], type)):
                err_msg = "Fourth element in argument information matrix should be a 'tuple of types' or 'type' type."
                raise TypeError(err_msg)

            if num_args >= 5:
                if not isinstance(args[4], bool):
                    raise TypeError("Fifth element in argument information matrix should be bool.")

            #
            # Let's validate argument types.
            #
            # Verify datatypes for arguments which are required or the optional arguments are not None
            if ((args[2] == True and args[1] is not None) or (args[2] == False)):
                # Validate the types of argument, if expected types are instance of tuple or type
                dtype_list = _Validators.__getTypeAsStr(args[3])

                if isinstance(args[3], tuple) and list in args[3]:
                    # If list of data types contain 'list', which means argument can accept list of values.
                    dtype_list.remove('list')
                    valid_types_str = ", ".join(dtype_list) + " or list of values of type(s): " + ", ".join(
                        dtype_list)

                    if isinstance(args[1], list):
                        # If argument contains list of values, check each value.
                        for value in args[1]:
                            # If not valid datatype add invalid_arg to dictionary and break
                            if not _Validators._check_isinstance(value, args[3]):
                                invalid_arg_names.append(args[0])
                                invalid_arg_types.append(valid_types_str)
                                typeCheckFailed = True
                                break
                    elif not _Validators._check_isinstance(args[1], args[3]):
                        # Argument is not of type list.
                        invalid_arg_names.append(args[0])
                        invalid_arg_types.append(valid_types_str)
                        typeCheckFailed = True

                elif isinstance(args[3], tuple):
                    # Argument can accept values of multiple types, but not list.
                    valid_types_str = " or ".join(dtype_list)
                    if not _Validators._check_isinstance(args[1], args[3]):
                        invalid_arg_names.append(args[0])
                        invalid_arg_types.append(valid_types_str)
                        typeCheckFailed = True
                else:
                    # Argument can accept values of single type.
                    valid_types_str = " or ".join(dtype_list)
                    if not _Validators._check_isinstance(args[1], args[3]):
                        invalid_arg_names.append(args[0])
                        invalid_arg_types.append(valid_types_str)
                        typeCheckFailed = True

                #
                # Validate the arguments for empty value
                #
                if not typeCheckFailed and len(args) >= 5:
                    if args[4]:
                        _Validators._validate_input_columns_not_empty(args[1], args[0], skip_empty_check)

                #
                # Validate the arguments for permitted values
                #
                if not typeCheckFailed and len(args) >= 6:
                    if args[5] is not None:
                        _Validators._validate_permitted_values(args[1], args[5], args[0])

        if typeCheckFailed:
            if len(invalid_arg_names) != 0:
                raise TypeError(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE,
                                                     invalid_arg_names, invalid_arg_types))

        return True

    @staticmethod
    def _validate_input_columns_not_empty(arg, arg_name, skip_empty_check = None):
        """
        Function to check whether argument is empty string or not.

        PARAMETERS:
            arg:
                Required Argument.
                Argument value (string) to be checked whether it is empty or not.
            skip_empty_check:
                Optional Argument.
                Specifies column name and values for which to skip check.
                Types: Dictionary specifying column name to values mapping.
                Example: When '\n', '\t' are valid values for argument 'arg_name', this check should be skipped.

        RAISES:
            Error if argument contains empty string

        EXAMPLES:
            _Validators._validate_input_columns_not_empty(arg)
        """
        if isinstance(arg, str):
            if not (skip_empty_check and arg_name in skip_empty_check.keys() and arg in skip_empty_check[arg_name]):
                    if ((len(arg.strip()) == 0)):
                        raise ValueError(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name))

        if isinstance(arg, list):
            if len(arg) == 0:
                raise ValueError(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name))

            for col in arg:
                if not (skip_empty_check and arg_name in skip_empty_check.keys() and col in skip_empty_check[arg_name]):
                    if isinstance(col, str):
                        if (not (col is None) and ((len(col.strip()) == 0))):
                            raise ValueError(Messages.get_message(MessageCodes.ARG_EMPTY, arg_name))
        return True

    @staticmethod
    def _validate_missing_required_arguments(arg_list):
        """
        Method to check whether the required arguments passed to the function are missing
        or not. Only wrapper's use this function.

        PARAMETERS:
            arg_list - A list
                       The argument is expected to be a list of arguments

        RAISES:
            If any arguments are missing exception raised with missing arguments which are
            required.

        EXAMPLES:
            An example input matrix will be:
            arg_info_matrix = []
            arg_info_matrix.append(["data", data, False, DataFrame])
            arg_info_matrix.append(["centers", centers, True, int])
            arg_info_matrix.append(["threshold", threshold, True, "float"])
            awu = AnalyticsWrapperUtils()
            awu._validate_missing_required_arguments(arg_info_matrix)
        """
        miss_args = []
        for args in arg_list:
            '''
            Check for missing arguments which are required. If args[2] is false
            the argument is required.
            The following conditions are true :
                1. The argument should not be None and an empty string.
            then argument is required which is missing and Raises exception.
            '''
            if args[2] == False and args[1] is None:
                miss_args.append(args[0])

        if (len(miss_args)>0):
            raise TeradataMlException(Messages.get_message(MessageCodes.MISSING_ARGS,miss_args),
                            MessageCodes.MISSING_ARGS)
        return True

    @staticmethod
    def _validate_permitted_values(arg, permitted_values, arg_name, case_insensitive=True, includeNone=True):
        """
        Function to check the permitted values for the argument.

        PARAMETERS:
            arg:
                Required Argument.
                Argument value to be checked against permitted values from the list.
                Types: string

            permitted_values:
                Required Argument.
                A list of strings/ints/floats containing permitted values for the argument.
                Types: string

            arg_name:
                Required Argument.
                Name of the argument to be printed in the error message.
                Types: string

            case_insensitive:
                Optional Argument.
                Specifies whether values in permitted_values could be case sensitive.
                Types: bool

            includeNone:
                Optional Argument.
                Specifies whether 'None' can be included as valid value.
                Types: bool

        RAISES:
            Error if argument is not present in the list

        EXAMPLES:
            permitted_values = ["LOGISTIC", "BINOMIAL", "POISSON", "GAUSSIAN", "GAMMA", "INVERSE_GAUSSIAN", "NEGATIVE_BINOMIAL"]
            arg = "LOGISTIC"
            _Validators._validate_permitted_values(arg, permitted_values, argument_name)
        """
        # validating permitted_values type which has to be a list
        _Validators._validate_function_arguments([["permitted_values", permitted_values, False, (list)]])

        if case_insensitive:
            permitted_values = [item.upper() if isinstance(item, str) else item for item in permitted_values]

        # Validate whether argument has value from permitted values list or not.
        if not isinstance(arg, list) and arg is not None:
            arg = [arg]

        if arg is not None:
            # Getting arguments in uppercase to compare with 'permitted_values'
            arg_upper = []
            for element in arg:
                if element is None:
                    # If element is None, then we shall add a string "None"
                    if includeNone:
                        continue
                    arg_upper.append(str(element))
                elif isinstance(element, str):
                    # If element is of type str, then we will convert it to upper case.
                    if case_insensitive:
                        arg_upper.append(element.upper())
                    else:
                        arg_upper.append(element)
                else:
                    # For anytother type of element, we will keep it as is.
                    arg_upper.append(element)

            # If any of the arguments in 'arg_upper' not in 'permitted_values',
            # then, raise exception
            if not (set(arg_upper).issubset(set(permitted_values))):
                upper_invalid_values = list(set(arg_upper).difference(set(permitted_values)))
                # Getting actual invalid arguments (non-upper)
                invalid_values = []
                for element in arg:
                    if element is None:
                        if includeNone:
                            continue
                        invalid_values.append(str(element))
                    elif isinstance(element, str) and element.upper() in upper_invalid_values:
                        invalid_values.append(element)
                    elif element in upper_invalid_values:
                        invalid_values.append(element)
                invalid_values.sort()
                raise ValueError(
                    Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                         ', '.join([str(item) if not isinstance(item, str) else item for item in invalid_values]),
                                         arg_name, permitted_values))
        # If any of the arguments doesn't want to include None as valid value 
        # then, raise exception
        else:
            if not includeNone:
                raise ValueError(
                        Messages.get_message(MessageCodes.INVALID_ARG_VALUE, None,
                                arg_name, permitted_values), MessageCodes.INVALID_ARG_VALUE)
        # Returns True when arg is None or there is no Exception
        return True

    @staticmethod
    def _validate_positive_int(arg, arg_name, lbound=0, ubound=None, lbound_inclusive=False):
        """
        Validation to check arg values is a positive int.

        PARAMETERS:
            arg:
                Required Argument.
                Specifies the number to be validated for positive INT.
                Types: int

            arg_name:
                Required Argument.
                Specifies the name of the argument to be printed in error message.
                Types: str

            lbound:
                Optional Argument.
                Specifies the lower bound value for arg.
                Note: Value provided to this argument is exclusive, i.e., if value provided
                      to this argument 10, then error will be raised for any value of arg <= 10.
                      It can be made inclusive, if lbound_inclusive is set to 'True'.
                Types: int

            ubound:
                Optional Argument.
                Specifies the upper bound value for arg.
                Note: Value provided to this argument is inclusive, i.e., if value provided
                      to this argument 10, then error will be raised for any value of arg > 10.
                Types: int

            lbound_inclusive:
                Optional Argument.
                Specifies a boolean flag telling API whether to lbound value is inclusive or not.
                Types: bool

        RAISES:
            ValueError - If arg is not a positive int.

        RETURNS:
            True - If success

        EXAMPLES:
            # Validate n for value > 0
            _Validators._validate_positive_int(n, "n")
            # Validate n for value > 0 and value <= 32767
            _Validators._validate_positive_int(n, "n", ubound="32767")
        """
        if arg is None:
            return True

        if ubound is None:
            if lbound_inclusive:
                if not isinstance(arg, numbers.Integral) or arg < lbound:
                    raise ValueError(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format(arg_name, "greater than or equal to"))
            else:
                if not isinstance(arg, numbers.Integral) or arg <= lbound:
                    raise ValueError(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT).format(arg_name, "greater than"))
        else:
            if not isinstance(arg, numbers.Integral) or arg <= lbound or arg > ubound:
                raise ValueError(Messages.get_message(MessageCodes.TDMLDF_LBOUND_UBOUND).format(arg_name, lbound,
                                                                                                ubound))

        return True

    @staticmethod
    def _validate_vantage_version(vantage_version):
        """
        Function to verify whether the given vantage_version is
        supported or not.

        PARAMETERS:
            vantage_version:
                Required Argument.
                Specifies the vantage version.

        RETURNS:
            True, if the current vantage version is supported or not.

        RAISES:
            TeradataMLException

        EXAMPLES:
            _Validators._validate_vantage_version("vantage1.0")
        """
        supported_vantage_versions = TeradataConstants.SUPPORTED_VANTAGE_VERSIONS.value

        # Raise exception if the vantage version is not supported.
        if vantage_version not in supported_vantage_versions.keys():
            err_ = Messages.get_message(MessageCodes.CONFIG_ALIAS_VANTAGE_VERSION_NOT_SUPPORTED).\
                    format(vantage_version, ", ".join(supported_vantage_versions.keys()))
            raise TeradataMlException(err_,
                                      MessageCodes.CONFIG_ALIAS_VANTAGE_VERSION_NOT_SUPPORTED)

        return True

    @staticmethod
    def _validate_timebucket_duration(timebucket_duration, timebucket_duration_arg_name='timebucket_duration'):
        """
        Internal function to validate timeduration_bucket specified when creating a
        Primary Time Index (PTI) table.

        PARAMETERS:
            timebucket_duration:
                Specifies the timebucket_duration passed to a function().
                Types: str

            timebucket_duration_arg_name:
                Specifies the name of the argument to be displayed in the error message.
                Types: str

        RETURNS:
            True if the value is valid.

        RAISES:
            ValueError or TeradataMlException when the value is invalid.

        EXAMPLES:
            _Validators._validate_timebucket_duration('HOURS(2)')
            _Validators._validate_timebucket_duration('2hours')
            _Validators._validate_timebucket_duration('ayear') # Invalid
        """
        # Return True is it is not specified or is None since it is optional
        if timebucket_duration is None:
            return True

        # Check if notation if formal or shorthand (beginning with a digit)
        if timebucket_duration[0].isdigit():
            valid_timebucket_durations = PTITableConstants.VALID_TIMEBUCKET_DURATIONS_SHORTHAND.value
            pattern_to_use = PTITableConstants.PATTERN_TIMEBUCKET_DURATION_SHORT.value
            normalized_timebucket_duration = timebucket_duration.lower()
        else:
            valid_timebucket_durations = PTITableConstants.VALID_TIMEBUCKET_DURATIONS_FORMAL.value
            pattern_to_use = PTITableConstants.PATTERN_TIMEBUCKET_DURATION_FORMAL.value
            normalized_timebucket_duration = timebucket_duration.upper()

        for timebucket_duration_notation in valid_timebucket_durations:
            pattern = re.compile(pattern_to_use.format(timebucket_duration_notation))
            match = pattern.match(normalized_timebucket_duration)
            if match is not None:
                n = int(match.group(1))
                _Validators._validate_positive_int(n, "n", ubound=32767)

                # Looks like the value is valid
                return True

        # Match not found
        raise ValueError(Messages.get_message(
            MessageCodes.INVALID_ARG_VALUE).format(timebucket_duration, timebucket_duration_arg_name,
                                                   'a valid time unit of format time_unit(n) or it\'s short hand '
                                                   'equivalent notation'))

    @staticmethod
    def _validate_column_type(df, col, col_arg, expected_types, raiseError = True):
        """
        Internal function to validate the type of an input DataFrame column against
        a list of expected types.

        PARAMETERS
            df:
                Required Argument.
                Specifies the input teradataml DataFrame which has the column to be tested
                for type.
                Types: teradataml DataFrame

            col:
                Required Argument.
                Specifies the column in the input DataFrame to be tested for type.
                Types: str

            col_arg:
                Required Argument.
                Specifies the name of the argument used to pass the column name.
                Types: str

            expected_types:
                Required Argument.
                Specifies a list of teradatasqlachemy datatypes that the column is
                expected to be of type.
                Types: list of SQLAlchemy types

            raiseError:
                Optional Argument.
                Specifies a boolean flag that decides whether to raise error or just return True or False.
                Default Values: True, raise exception if column is not of desired type.
                Types: bool

        RETURNS:
            True, when the columns is of an expected type.

        RAISES:
            TeradataMlException, when the columns is not one of the expected types.

        EXAMPLES:
            _Validators._validate_column_type(df, timecode_column, 'timecode_column', PTITableConstants.VALID_TIMECODE_DATATYPES)
        """
        if not any(isinstance(df[col].type, t) for t in expected_types):
            if raiseError:
                raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_COLUMN_TYPE).
                                          format(col_arg, df[col].type, ' or '.join(expected_type.__visit_name__
                                                                                    for expected_type in expected_types)),
                                          MessageCodes.INVALID_COLUMN_TYPE)
            else:
                return False

        return True

    @staticmethod
    def _validate_aggr_operation_unsupported_datatype(operation, columns, td_column_names_and_types):
        """
        Internal function to validate the for unsupported data types of an input DataFrame column for
        an aggreagate function.

        PARAMETERS
            operation:
                Required Argument.
                Specifies the name of the aggregate operation.
                Types: str

            columns:
                Required Argument.
                Specifies the column names to be validated for datatype check.
                Types: str

            td_column_names_and_types:
                Required Argument.
                Specifies the input teradataml DataFrames column name to SQLAlchemy type mapper.
                Types: str

        RETURNS:
            None

        RAISES:
            TeradataMlException, when the columns is not one of the expected types.

        EXAMPLES:
            _Validators._validate_aggr_operation_unsupported_datatype(operation, columns, td_column_names_and_types):
        """
        # Check if the user provided columns has unsupported datatype for aggregate operation or not.
        # Get the list of unsupported types for aggregate function.
        unsupported_types = _Dtypes._get_unsupported_data_types_for_aggregate_operations(operation)
        invalid_columns = []

        for column in columns:
            if isinstance(td_column_names_and_types[column.lower()], tuple(unsupported_types)):
                invalid_columns.append(
                    "({0} - {1})".format(column, td_column_names_and_types[column.lower()]))

        if len(invalid_columns) > 0:
            invalid_columns.sort()  # helps in catching the columns in
            # lexicographic order
            error = MessageCodes.TDMLDF_AGGREGATE_UNSUPPORTED.value.format(
                ", ".join(invalid_columns), operation)
            msg = Messages.get_message(MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR). \
                format(error)
            raise TeradataMlException(msg, MessageCodes.TDMLDF_AGGREGATE_COMBINED_ERR)

    @staticmethod
    def _validate_str_arg_length(arg_name, arg_value, op, length):
        """
        Internal function to validate the length of a string passed as an argument.

        PARAMETERS
            arg_name:
                Required Argument.
                Specifies the name of the argument for which we need to validate the value length.
                Types: str

            arg_value:
                Required Argument.
                Specifies the value passed to the argument.
                Types: str

            op:
                Required Argument.
                Specifies the type of check, and can be one of:
                * LT - Less than
                * LE - less than or equal to
                * GT - greater than
                * GE - greater than or equal to
                * EQ - equal to
                * NE - not equal to
                Types: str
                Permitted Values: ['LT', 'LE', 'GT', 'GE', 'EQ', 'NE']

            length:
                Required Argument.
                Specifies the length against which the 'op' check for the argument value length will be made.
                Types: int

        RETURNS:
            None

        RAISES:
            ValueError.

        EXAMPLES:
            _Validators._validate_str_arg_length("name", "The value", 10):
        """
        # Check if the length of the string value for the argument is acceptable.
        # First, check if op is an acceptable operation.
        acceptable_op = {'LT': int.__lt__,
                         'LE': int.__le__,
                         'GT': int.__gt__,
                         'GE': int.__ge__,
                         'EQ': int.__eq__,
                         'NE': int.__ne__
                         }
        if op not in acceptable_op:
            raise ValueError(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                                  op, "op", acceptable_op))

        # Format the error message with the substring based on the op type.
        errors = {'LT': "less than {}",
                  'LE': "less than or equal to {}",
                  'GT': "greater than {}",
                  'GE': "greater than or equal to {}",
                  'EQ': "equal to {}",
                  'NE': "not equal to {}"
                  }
        if not acceptable_op[op](len(arg_value), length):
            raise ValueError(Messages.get_message(MessageCodes.INVALID_LENGTH_STRING_ARG,
                                                  arg_name, errors[op].format(length)))

    @staticmethod
    def _validate_file_exists(file_path):
        """
        DESCRIPTION:
            Function to validate whether the path specified is a file and if it exists.

        PARAMETERS:
            file_path:
                Required Argument.
                Specifies the path of the file.
                Types: str

        RETURNS:
            True, if the path is a file and it exists.

        RAISES:
            TeradataMLException

        EXAMPLES:
            _Validators._validate_file_exists("/data/mapper.py")
        """
        if not Path(file_path).exists() or not os.path.isfile(file_path):
            raise TeradataMlException(
                Messages.get_message(MessageCodes.INPUT_FILE_NOT_FOUND).format(file_path),
                MessageCodes.INPUT_FILE_NOT_FOUND)

        return True

    @staticmethod
    def _validate_mutually_exclusive_arguments(arg1, err_disp_arg1_name, arg2,
                                               err_disp_arg2_name, skip_all_none_check = False):
        """
        DESCRIPTION:
            Function to validate whether "arg1" and "arg2" are mutually exclusive.

        PARAMETERS:
            arg1:
                Required Argument.
                Specifies the value of argument1.
                Types: Any

            err_disp_arg1_name:
                Required Argument.
                Specifies the name of argument1.
                Types: str

            arg2:
                Required Argument.
                Specifies the value of argument2.
                Types: Any

            err_disp_arg2_name:
                Required Argument.
                Specifies the name of argument2.
                Types: str

            skip_all_none_check:
                Optional Argument.
                Specifies whether to skip check when arg1 and arg2 both are None.
                Default Value: False
                Types: bool

        RETURNS:
            True, if either arg1 or arg2 is None or both are None.

        RAISES:
            TeradataMLException
            
        EXAMPLES:
            _Validators._validate_mutually_exclusive_arguments(arg1, "arg1", arg2, "arg2")
                """
        both_args_none = arg1 is None and arg2 is None
        if skip_all_none_check:
            both_args_none = False

        # Either both the arguments are specified or both are None.
        if all([arg1, arg2]) or both_args_none:
            raise TeradataMlException(Messages.get_message(
                MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT, err_disp_arg1_name,
                err_disp_arg2_name), MessageCodes.EITHER_THIS_OR_THAT_ARGUMENT)
        return True
