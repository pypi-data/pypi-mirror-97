"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: karthik.thelukuntla@teradata.com
Secondary Owner: mark.sandan@teradata.com

This file is for providing user configurable options.
"""
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes


class _DisplaySuper(object):

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


class _Display(_DisplaySuper):
    """
    Display options for printing teradataml DataFrames and SQLMR functions.
    """

    max_rows = _create_property('max_rows')
    precision = _create_property('precision')
    byte_encoding = _create_property('byte_encoding')
    print_sqlmr_query = _create_property('print_sqlmr_query')

    def __init__(self,
                 max_rows = 10,
                 precision = 3,
                 byte_encoding = 'base16',
                 print_sqlmr_query = False):

        super().__init__()
        super().__setattr__('max_rows', max_rows)
        super().__setattr__('precision', precision)
        super().__setattr__('byte_encoding', byte_encoding)
        super().__setattr__('print_sqlmr_query', print_sqlmr_query)

    def __setattr__(self, name, value):
        if hasattr(self, name):
            if name == 'max_rows' or name == 'precision':
                if not isinstance(value, int):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'int'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)
                if value <= 0:
                    raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_POSITIVE_INT, name, "greater than"),
                                              MessageCodes.TDMLDF_POSITIVE_INT)
            elif name == 'byte_encoding':
                valid_encodings = ['ascii', 'base16', 'base2', 'base8', 'base64m']
                if not isinstance(value, str):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'str'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)

                value = value.lower()
                if value not in valid_encodings:
                    raise TeradataMlException(Messages.get_message(MessageCodes.INVALID_ARG_VALUE,
                                                                   value,
                                                                   name,
                                                                   "a value in {}".format(valid_encodings)),
                                              MessageCodes.INVALID_ARG_VALUE)
            elif name == 'print_sqlmr_query':
                if not isinstance(value, bool):
                    raise TeradataMlException(Messages.get_message(MessageCodes.UNSUPPORTED_DATATYPE, name,
                                                                   'bool'),
                                              MessageCodes.UNSUPPORTED_DATATYPE)

            super().__setattr__(name, value)
        else:
            raise AttributeError("'{}' object has no attribute '{}'".format(self.__class__.__name__, name))


display = _Display()
