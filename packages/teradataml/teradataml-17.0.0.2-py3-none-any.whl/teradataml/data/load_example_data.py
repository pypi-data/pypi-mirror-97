"""
Unpublished work.
Copyright (c) 2018 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: mounika.kotha@teradata.com
Secondary Owner:

This file implements the functionality of loading data to a table.
"""

import csv
import json
import os
import datetime
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.context.context import *
from teradataml.dataframe.copy_to import copy_to_sql
import pandas as pd
import numpy as np
from teradataml import *
from teradataml.options import display
from teradataml.common.utils import UtilFuncs
from teradataml.common.sqlbundle import SQLBundle
import teradataml.context.context as tdmlctx
from teradataml.context.context import _get_context_temp_databasename
from collections import OrderedDict, defaultdict

json_data = {}
col_types_dict = {}
curr_dir = os.path.dirname(os.path.abspath(__file__))

def load_example_data(function_name, table_name):
    """
    This function loads the data to the specified table. This is only used for
    trying examples for the analytic functions, to load the required data.
    
    PARAMETERS:
        function_name:
            Required Argument.
            The argument contains the prefix name of the example json file to be used to load data.
            Note: One must use the function_name values only as specified in the load_example_data()
                  function calls specified in the example sections of teradataml API's. If any other
                  string is passed as prefix input an error will be raised as 'prefix_str_example.json'
                  file not found.
            This *_example.json file contains the schema information for the tables that can be loaded
            using this JSON file. Sample json containing table schema is as follows. Here we can
            load three tables 'sentiment_extract_input', 'sentiment_word' and 'restaurant_reviews', with
            <function_name>_exmaple.json, assuming file name is <function_name>_exmaple.json
                {
                    "sentiment_extract_input": {
                        "id" : "integer",
                        "product" : "varchar(30)",
                        "category" : "varchar(10)",
                        "review" : "varchar(1500)"
                    },
                    "sentiment_word": {
                        "word" : "varchar(10)",
                        "opinion" : "integer"
                    },
                    "restaurant_reviews": {
                        "id" : "integer",
                        "review_text" : "varchar(500)"
                    }
                }

            Type : str

        table_name
            Required Argument.
            Specifies the name of the table to be created in the database.
            Note: Table names provided here must have an equivalent datatfile (CSV) present at
                  teradataml/data. Schema information for the same must also be present in
                  <function_name>_example.json as shown in 'function_name' argument description.
            Type : string or list of str

    EXAMPLES:
        load_example_data("pack", "ville_temperature")
        load_example_data("attribution", ["attribution_sample_table1", "attribution_sample_table2" , 
                                  "conversion_event_table", "optional_event_table", "model1_table", "model2_table"])
              
    RETURNS:
        None.
        
    RAISES:
        TeradataMlException - If table load fails.
        FileNotFoundError - If invalid function_name is provided.
    
    """
    example_filename = os.path.join(curr_dir, "{}_example.json".format(function_name.lower()))
    global json_data
    
    #Read json file to get table columns and datatypes
    with open(format(example_filename)) as json_input:
        json_data = json.load(json_input, object_pairs_hook = OrderedDict)

    if isinstance(table_name, list) :
        for table in table_name:
            try:
                __create_table_insert_data(table)
            except TeradataMlException as err:
                if err.code == MessageCodes.TABLE_ALREADY_EXISTS:
                    # TODO - Use the improved way of logging messages when the right tools for it are built in
                    print("WARNING: Skipped loading table {} since it already exists in the database.".format(table))
                else:
                    raise
    else:
        try:
            __create_table_insert_data(table_name)
        except TeradataMlException as err:
            if err.code == MessageCodes.TABLE_ALREADY_EXISTS:
                # TODO - Use the improved way of logging messages when the right tools for it are built in
                print("WARNING: Skipped loading table {} since it already exists in the database.".format(table_name))
            else:
                raise

    json_input.close()

def __create_table_insert_data(tablename):
    """
    Function creates table and inserts data from csv into the table.
    
    PARAMETERS:
        tablename:
            Required Argument.
            Specifies the name of the table to be created in the database.
            Type : str
     
    EXAMPLES:
         __create_table_insert_data("ville_temperature")
         
    RETURNS:
         None.
        
    RAISES:
         TeradataMlException - If table already exists in database.
     """
    csv_file = os.path.join(curr_dir, "{}.csv".format(tablename))
    col_types_dict  = json_data[tablename]
    column_dtypes = ''
    date_time = {}
    pti_table = False
    pti_clause = ""
    
    '''
    Create column datatype string required to create a table.
    EXAMPLE:
        id integer,model varchar(30)
    '''
    column_count = 0
    for column in col_types_dict.keys():
        if column in ["TD_TIMECODE", "TD_SEQNO"]:
            column_count = column_count + 1
            continue

        if column == "<PTI_CLAUSE>":
            pti_table = True
            pti_clause = col_types_dict[column]
            continue

        # Create a dictionary with column names as list of values which has 
        # datatype as date and timestamp.
        # EXAMPLE : date_time_columns = {'date':['orderdate']}
        if col_types_dict[column] == "date":
            date_time.setdefault("date", []).append(column)
        elif col_types_dict[column] == "timestamp":
            date_time.setdefault("timestamp", []).append(column)
        column_dtypes ="{0}{1} {2},\n" .format(column_dtypes, column, col_types_dict[column])
        column_count = column_count + 1

    td_number_of_columns = '?,' * column_count
    # Deriving global connection using context.get_context()
    con = get_context()    
    table_exists = con.dialect.has_table(con, tablename, schema=_get_context_temp_databasename())
    if table_exists:
        raise TeradataMlException(Messages.get_message(MessageCodes.TABLE_ALREADY_EXISTS, tablename),
                                              MessageCodes.TABLE_ALREADY_EXISTS)   
    else:
        tablename = "{}.{}".format(UtilFuncs._teradata_quote_arg(_get_context_temp_databasename(), "\"", False),
                                   UtilFuncs._teradata_quote_arg(tablename, "\"", False))
        if pti_table:
            UtilFuncs._create_table_using_columns(tablename, column_dtypes[:-2], pti_clause)
        else:
            UtilFuncs._create_table_using_columns(tablename, column_dtypes[:-2])

        try:
            __insert_into_table_from_csv(tablename, td_number_of_columns[:-1], csv_file, date_time)
        except:
            # Drop the table, as we have created the same.
            UtilFuncs._drop_table(tablename)
            raise
        

def __insert_into_table_from_csv(tablename, column_markers, file, date_time_columns):
        """
        Builds and executes a prepared statement with parameter markers for a table. 
        
        PARAMETERS:
            tablename:
                Required Argument.
                Table name to insert data into.
                Types: str

            column_markers
                Required Argument.
                The parameter markers for the insert prepared statement.
                Types: str

            file
                Required Argument.
                csv file which contains data to be loaded into table.
                Types: str

            date_time_columns
                Required Argument.
                Dictionary containing date and time columns.
                Types: Dictionary
            
        EXAMPLES:
            date_time_columns = {'date':['orderdate']}
            preparedstmt = __insert_into_table_from_csv(
                            'mytab', '?, ?','file.csv', date_time_columns )

        RETURNS:
             None

        RAISES:
            Database error if an error occurred while executing the DDL statement.
        
        """
        insert_stmt = SQLBundle._build_insert_into_table_records(tablename, column_markers)
        
        if tdmlctx.td_connection is not None:
            try:
                with open (file, 'r') as f:
                    reader = csv.reader(f)
                    # Read headers of csv file
                    headers = next(reader)

                    insert_list = []
                    for row in reader :
                        # For NULL values, entries in csv are ""
                        # Handling table with NULL values
                        new_row = [] # Row with None when element is empty
                        for element in row:
                            if element == "":
                                new_row.append(None)
                            else:
                                new_row.append(element)
                        '''
                        The data in the row is converted from string to date or 
                        timestamp format, which is required to insert data into
                        table for date or timestamp columns.
                        '''
                        for key,value in date_time_columns.items():
                            if key == 'date':
                                for val in value:
                                    if val in headers:
                                        if new_row[headers.index(val)] != None:
                                            new_row[headers.index(val)] = datetime.datetime.strptime(
                                                new_row[headers.index(val)], '%Y-%m-%d')
                            elif key == 'timestamp':
                                for val in value:
                                    if val in headers:
                                        if new_row[headers.index(val)] != None:
                                            new_row[headers.index(val)] = datetime.datetime.strptime(
                                                new_row[headers.index(val)], '%Y-%m-%d %H:%M:%S')
                            elif key == 'timestamp(6)':
                                for val in value:
                                    if val in headers:
                                        if new_row[headers.index(val)] != None:
                                            new_row[headers.index(val)] = datetime.datetime.strptime(
                                                new_row[headers.index(val)], '%Y-%m-%d %H:%M:%S.%f')

                        insert_list.append(tuple(new_row))

                    # Batch Insertion (using DBAPI's executeMany) used here to insert list of dictionaries
                    get_context().execution_options(autocommit=True).execute(insert_stmt, *(r for r in insert_list))

            except:
                raise
        else:
            raise TeradataMlException(Messages.get_message(MessageCodes.CONNECTION_FAILURE), MessageCodes.CONNECTION_FAILURE)
    
