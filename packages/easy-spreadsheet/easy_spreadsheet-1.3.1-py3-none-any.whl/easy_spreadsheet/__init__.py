"""
스프레드시트 인증, 시트 데이터프레임으로 가져오기 등 스프레드시트와 관련된 함수들이 있습니다.
"""
import time
import logging
import base64
import json
import itertools
import gspread
import os
import sys
import importlib
import pandas as pd
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):
            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)

class EasyWorksheet():

    def __init__(self, worksheet, load_render_option='FORMULA'):
        self._worksheet = worksheet
        self._table = self._load_table(load_render_option)

    @property
    def table():
        return self._table
        
    def push(self, cell_indexes=[]):
        cell_indexes = set(cell_indexes)

        cell_list = []

        for index, row in enumerate(json.loads(json.dumps(self._table.to_dict(orient='records'), ensure_ascii=False, cls=NumpyEncoder))):
            values = self._make_sheet_row(row.values())

            for value_index, value in enumerate(values):
                if cell_indexes and (index + 1, value_index + 1) not in cell_indexes:
                    continue

                cell = gspread.models.Cell(index + 1, value_index + 1)
                cell.value = value
                cell_list.append(cell)

        if len(cell_list):
            self._worksheet.update_cells(cell_list, value_input_option='USER_ENTERED')



    @staticmethod
    def get_label_from_indexes(row_index, col_index):
        return f'{spread_order[col_index]}{row_index + 1}'


    def _parse(self, value):
        if type(value) is list or type(value) is dict:
            v = value
        else:
            try:
                v = json.loads(value)
            except:
                v = value

        return v
        
    def _convert(self, value):
        if type(value) is list or type(value) is dict:
            v = json.dumps(value, ensure_ascii=False)
        else:
            v = value

        return v

    def _make_sheet_row(self, row):
        temp = []
        for p in row:
            v = self._convert(p)

            temp.append(v)

        return temp
            
    def _load_table(self, load_render_option):

        records = self._worksheet.get_all_values(load_render_option)

        rows = []
        for row in records:
            temp = []
            for p in row:
                v = self._parse(p)
                temp.append(v)

            rows.append(temp)

        return pd.DataFrame(rows)


class EasySpreadsheet():

    def __init__(self, auth_json, spreadsheet_id):
        self._spread_order = list(EasySpreadsheet.allcombinations(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZ', minlen=1, maxlen=3))
        self._auth_json = auth_json
        self._sheet = self._get_sheet(spreadsheet_id)

    @property
    def sheet():
        return self._sheet

    def _get_sheet(self, spreadsheet_id):
        
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/feeds',
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            self._auth_json, scopes)
        gc = gspread.authorize(credentials)
        spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0'

        return gc.open_by_url(spreadsheet_url)

    def get_worksheet(worksheet_name):
        return EasyWorksheet(self._sheet.worksheet(worksheet_name))


    def format(self, start_column, start_index, end_column, end_index, cell_format):
        
        range_name = self._spread_order[start_column] + str(start_index + 1) + ":" + \
                    self._spread_order[end_column] + str(end_index + 1)

        return self._cloudsheet.format(range_name, cell_format)

    @staticmethod
    def allcombinations(self, alphabet, minlen=1, maxlen=None):
        thislen = minlen
        while maxlen is None or thislen <= maxlen:
            for prod in itertools.product(alphabet, repeat=thislen):
                yield ''.join(prod)
            thislen += 1