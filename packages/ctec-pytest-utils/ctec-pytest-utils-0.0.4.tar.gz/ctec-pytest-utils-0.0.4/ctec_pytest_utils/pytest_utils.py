#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import xlrd
import pytest
from flask import Flask

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# app.register_blueprint(recharge_open_service, url_prefix='/recharge')

def get_test_data(sheet_name, file_path):
    """
    read test data
    :param sheet_name:
    :param file_path:  file name:  data.xlsx
    :return:
    """
    if not os.path.isfile(file_path + os.sep + "pytest.ini"):
        fd = open(file_path + os.sep + "pytest.ini", mode="w", encoding="utf-8")
        fd.write("""# pytest.ini

[pytest]

python_files = test_*.py *_test.py tm*.py
python_classes = Test*
python_functions = test_*

; addopts= -v --html=./status/report.html --self-contained-html --cov=./ --cov-report=html
; -v (output report)  -s (output)    -- cov (output coverage)

; debug
;addopts = -v -s -p no:warnings

; output file
addopts= -v  --html=./status/report.html  --cov=../ --cov-report html --cov-report term-missing -p no:warnings""")
        fd.close()

    data_value = []
    work_xls = xlrd.open_workbook(file_path + os.sep + "data.xlsx")
    sheet = work_xls.sheet_by_name(sheet_name)
    ncols = sheet.ncols
    nrows = sheet.nrows
    for i in range(0, nrows):
        temp = []
        for j in range(0, ncols - 1):  # 最后一行注释不读取所以减一
            v1 = str(sheet.cell(i, j).value)
            temp.append(v1)
        data_value.append(temp)
    data = data_value[1:]
    args_name = data_value[0]
    return data, args_name


class TestUtils:

    @pytest.fixture()
    def client(self):
        with app.test_client() as c:
            yield c

    # @pytest.mark.parametrize("args_list", data)
    # @pytest.mark.functional
    # def test_flask_client(self, args_list, client):
    #     args = dict(zip(test_utils.func_para, args_list))
    #     self.test_func(args, client)
    #
    # @pytest.mark.parametrize("args_list", data)
    # @pytest.mark.functional
    # def test_func(self, args_list):
    #     args = dict(zip(func_para, args_list))
    #     self.test_func(args, client)


# if __name__ == '__main__':
#     result = get_test_data("wx", "/Users/xiaoyu/code/0_work/pytest_demo/test")

    # data = get_test_data()
    # print(data)
    # print(",".join(get_test_data()[0]), get_test_data()[1:])
    # pytest.main()
    # pytest - sv - -html =./ status / report.html - -self - contained - html - -cov =./ --cov - report = html
