# 官渡
官渡之战的官渡

将基础封装上传到第三方库

# 使用方法
检查setup.py 是否正确

`python3 setup.py check` 

打包

`python3 setup.py sdist` 

发布

安装工具twine `pip install twine`  
`twine upload dist/*`

使用

`python -m pip install guandu`

# 开发注意事项
1. 做适用性强的基础封装
2. 写单元测试


# db操作
## mysql
`from db_cmd.mysql import ExecuteMysql`