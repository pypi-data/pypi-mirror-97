"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: karthik.thelukuntla@teradata.com
Secondary Owner:

This file is for providing user configurable options.
"""
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes


class _ConfigureSuper(object):

    def __init__(self):
        pass

    def _SetKeyValue(self, name, value):
        super().__setattr__(name, value)

    def _GetValue(self, name):
        return super().__getattribute__(name)


def _create_property(name):
    storage_name = '_' + name

    @property
    def prop(self):
        return self._GetValue(storage_name)

    @prop.setter
    def prop(self, value):
        self._SetKeyValue(storage_name, value)

    return prop


class _Configure(_ConfigureSuper):
    """
    Options to configure database related values.
    """

    default_varchar_size = _create_property('default_varchar_size')
    column_casesensitive_handler = _create_property('column_casesensitive_handler')
    vantage_version = _create_property('vantage_version')
    val_install_location = _create_property('VAL_install_location')
    sandbox_container_id = _create_property('sandbox_container_id')

    def __init__(self, default_varchar_size=1024, column_casesensitive_handler = False,
                 vantage_version="vantage1.1", val_install_location=None,
                 sandbox_container_id=None):
        """
        PARAMETERS:
            default_varchar_size:
                Specifies the size of varchar datatype in Teradata Vantage, the default
                size is 1024.
                User can configure this parameter using options.
                Types: int
                Example:
                    teradataml.options.configure.default_varchar_size = 512

            column_casesensitive_handler:
                Specifies a boolean value that sets the value of this option to True or
                False.
                One should set this to True, when ML Engine connector property is
                CASE-SENSITIVE, else set to False, which is CASE-INSENSITIVE.
                Types: bool
                Example:
                    # When ML Engine connector property is CASE-SENSITIVE, set this
                    # parameter to True.
                    teradataml.options.configure.column_casesensitive_handler = True

            vantage_version:
                Specifies the Vantage version of the system teradataml is connected to.
                Types: string
                Example:
                    # Set the Vantage Version
                    teradataml.options.configure.vantage_version = "vantage1.1"

            val_install_location:
                Specifies the name of the database where Vantage Analytic Library functions
                are installed.
                Types: string
                Example:
                    # Set the Vantage Analytic Library install location to 'SYSLIB'
                    # when VAL functions are installed in 'SYSLIB'.
                    teradataml.options.configure.val_install_location = "SYSLIB"

            sandbox_container_id:
                Specifies the id of sandbox container that will be used by test_script method.
                Types: string
                Example:
                    # Set the sandbox_container_id.
                    teradataml.options.configure.sandbox_container_id = '734rfjsls3'

        """
        super().__init__()
        super().__setattr__('default_varchar_size', default_varchar_size)
        super().__setattr__('column_casesensitive_handler', column_casesensitive_handler)
        super().__setattr__('vantage_version', vantage_version)
        super().__setattr__('val_install_location', val_install_location)
        super().__setattr__('sandbox_container_id', sandbox_container_id)

        # internal configurations
        # These configurations are internal and should not be
        # exported to the user's namespace.
        super().__setattr__('_validate_metaexpression', False)
        # Internal parameter, that should be used while testing to validate whether
        # Garbage collection is being done or not.
        super().__setattr__('_validate_gc', False)
        # Internal parameter, that is used for checking if sto sandbox image exists on user's system
        super().__setattr__('_latest_sandbox_exists', False)
        # Internal parameter, that is used for checking whether a container was started by
        # teradataml.
        super().__setattr__('_container_started_by_teradataml', None)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            if name == 'default_varchar_size':
                if not isinstance(value, int):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'int'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)
                if value <= 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT, name, "greater than"),
                                              MessageCodes.TDMLDF_POSITIVE_INT)
            elif name in ['column_casesensitive_handler', '_validate_metaexpression',
                          '_validate_gc', '_latest_sandbox_exists']:

                if not isinstance(value, bool):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'bool'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)
            elif name == 'vantage_version':
                if not isinstance(value, str):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'str'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)
                valid_versions = ['vantage1.0', 'vantage1.1', 'vantage1.3', 'vantage2.0']
                value = value.lower()
                if value not in valid_versions:
                    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                                                   value,
                                                                   name,
                                                                   "a value in {}".format(valid_versions)),
                                              MessageCodes.INVALID_ARG_VALUE)
            elif name == 'val_install_location':
                if not isinstance(value, str):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'str'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)

            elif name in ['sandbox_container_id', '_container_started_by_teradataml']:
                if not isinstance(value, str) and not isinstance(value, type(None)) :
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'str or None'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)

            super().__setattr__(name, value)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))


configure = _Configure()