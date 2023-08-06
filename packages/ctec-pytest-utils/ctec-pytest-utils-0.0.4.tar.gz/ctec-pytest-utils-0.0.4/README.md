# ctec-pytest-utils

#### 环境依赖

    py2.7+
    py3.0+
    ["pytest>=4.6.11", 
     "pytest-html>=1.22.1",
     "pytest-cov>=2.8.1", 
     "flask>=0.10.1", 
     "xlrd==1.2.0"]

#### 简介:

      基于pytest pytest-cov(代码覆盖率)做的工具包, 更多功能可基于pytest扩展.
pytest documentation
https://docs.pytest.org/en/latest/contents.html

#### 安装
   
      pip install ctec-pytest-utils
#### 使用

1. 项目内创建test包, 包内创建test_xx.py 测试文件
   ```text
      目录结构描述
      ├── app                         // 应用
      ├── test                        // 测试包
      │   ├── data.xlsx               // 测试数据
      │   ├── pytest.ini              // pytest参数 读取测试数据后创建 / pytest --添加参数
      │   ├── test_dome.py            // 编写测试逻辑
      │   └── __init__.py 
      └── ...
   ```

2. 样例
   ```python
   # 以下为 test_dome.py 测试样例
   # coding:utf-8
   import os
   import pytest
   from Service import test_service
   from ctec_pytest_utils import pytest_utils
   
   # flask蓝图注册  需要测试flask接口时添加
   pytest_utils.app.register_blueprint(test_service, url_prefix='/demo')
   
   # get_test_data(sheet_name, path)
   # data 测试数据 [[...], [...], [...], [...]]
   # para_name data.xlsx 文件首行参数名
   data, para_name = pytest_utils.get_test_data('WeCat', os.path.dirname(__file__))
   demo_data, demo_para_name = pytest_utils.get_test_data('test_demo', os.path.dirname(__file__))
   
   
   class TestMain(pytest_utils.TestUtils):
   
       @pytest.mark.parametrize("args_list", data)
       @pytest.mark.functional
       def test_flask_client(self, args_list, client):
           """
           flask 初始化client
               data 测试数据 [[...], [...], [...], [...]]
           自动循环测试data
           :param args_list:
           :param client:
           :return:
           """
           args = dict(zip(para_name, args_list))
           print("参数=", args)
           result = client.get("/demo/test1", data=args, headers={})
           # result = client.post("/demo/test2")
           result_data = result.data
           print("result_data=", result_data)
   
           # 断言测试用例结果与client返回结果
           assert args["result"] == result['code']
   
       # demo_data = [[1, 2], [2, 3], [3, 4]]
       # demo_para_name = ["para", "result"]
       @pytest.mark.parametrize("args_list", demo_data)
       @pytest.mark.functional
       def test_function(self, args_list):
           """
           函数测试 自动循环
           :param args_list: 
           :return: 
           """
           # args {"para": 1, "result": 2}
           args = dict(zip(demo_para_name, args_list))
   
           print("参数=", args)
           test_demo = lambda x: x + 1
           result = test_demo(args["para"])
           print("result=", result)
   
           # 断言测试用例结果与client返回结果
           assert result == args["result"]  # 2 == 2
   
   
   if __name__ == '__main__':
       pytest.main()
       # pytest - sv - -html =./ status / report.html - -self - contained - html - -cov =./ --cov - report = html
   ```

3. 执行命令
      
       执行目录:  /项目/test/
       pytest

4. 查验结果
      
         test/status/report.html    -- 测试样例输出
         test/htmlcov/index.html    -- 代码覆盖率
