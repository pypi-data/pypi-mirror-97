# encoding: utf-8
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
import logging
import os
import sys

dir_file = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')

class ExcelLib(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.1

    def __init__(self):
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        logger = logging.getLogger(__name__)

    # Function Excel
    @keyword('Open excel test data')
    def open_excel_test_data(self, dirData, docID, sheetName):
        keyword_execute = 'Open excel test data'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        BuiltIn().run_keyword(keyword_execute, r'{}'.format(dirData.replace('\\','/')), docID, sheetName)

    @keyword('Count rows test data')
    def count_rows_test_data(self, docID):
        keyword_execute = 'Count rows test data'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        data = BuiltIn().run_keyword(keyword_execute, docID)
        return data

    @keyword('Read row test data')
    def read_row_test_data(self, docID, writeRow):
        keyword_execute = 'Read row test data'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        data = BuiltIn().run_keyword(keyword_execute, docID, writeRow)
        return data

    @keyword('Close excel test data')
    def close_excel_test_data(self, docID):
        keyword_execute = 'Close excel test data'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        BuiltIn().run_keyword(keyword_execute, docID)

    @keyword('Result configurations')
    def result_configurations(self, dirResult, docID, row, data):
        keyword_execute = 'Result Configurations'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        BuiltIn().run_keyword(keyword_execute, dirResult, docID, row, data)

    @keyword('Compare data table')
    def compare_data_table(self, titel_excel, data):
        keyword_execute = 'Compare Data Table'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        EXCEL_DICTIONARY = BuiltIn().run_keyword(keyword_execute, titel_excel, data)
        return EXCEL_DICTIONARY

    @keyword('Reports excel')
    def Reports_excel(self, dirResult, docID, resultTitle, resultData, row=2):
        keyword_execute = 'Reports Excel'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        BuiltIn().run_keyword(keyword_execute, dirResult, docID, resultTitle, resultData, row)

    @keyword('Append to result data')
    def append_to_result_data(self, **listData):
        keyword_execute = 'Append To Result Data'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        returnData = BuiltIn().run_keyword(keyword_execute, listData)
        return returnData

    @keyword('Append to result title')
    def append_to_result_title(self, **listData):
        keyword_execute = 'Append To Result Title'
        BuiltIn().log_to_console(keyword_execute)
        BuiltIn().import_resource(dir_file+'/excellib.txt')
        returnKey = BuiltIn().run_keyword(keyword_execute, listData)
        return returnKey