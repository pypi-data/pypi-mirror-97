# 数据解析工具库



## 开始
1. 首先创建一个文件夹,文件夹名称不能包含连字符 - ,该文件夹(k_parse_tool)里面就是最终pypi包文件的内容(此步骤仅在初始化项目时使用),
2. 所有新增的功能都必须在文件夹k_parse_tool内.如果新增的是一个文件夹,则在该文件夹内必须包含一个以__init__.py命名的文件,
3. 在步骤1的同级目录中创建一个setup.py文件(此步骤仅初始化项目时使用)
4. 修改setup.py中的version名称,同时确保name值不能包含连字符 -
5. 生成pypi包文件:  python setup.py sdist bdist_wheel
    > 如果只安装到本地，在dist目录下使用命令  `pip install k_parse_tool-0.0.6-py3-none-any.whl`
6. 注册pypi的账号,待步骤7使用

   用户名:***xjliu***    密码:***liuxianjin926@***
7. 将步骤5生成的包上传到pypi库中,使用如下命令
    `python -m twine upload dist/*`
    
     > 发布新版时,请删除dist目录下所有旧版的包文件
    

setup.py文件中配置参数详见:
    [setup.py文件配置参数](https://packaging.python.org/tutorials/packaging-projects/)
    
### 依赖
- pdfplumber>=0.5.24
- python-docx>=0.8.10
- regex>=2020.11.13
- pandas>=1.1.5
- beautifulsoup4>=4.9.3
- numpy>=1.18.0
### 功能

### 安装
- 安装

```pip install k-parse-tool```



