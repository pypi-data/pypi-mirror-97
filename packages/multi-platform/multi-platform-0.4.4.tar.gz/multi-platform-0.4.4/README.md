# 课堂 android移动终端自动化项目

项目目录说明：


推荐语言 Python2.7
推荐IDE Pycharm
安装项目依赖 两种方式：
1. 命令行直接敲命令
```shell script
pip install -r requirements.txt -i http://pypi.dq.oa.com/simple --trusted-host pypi.dq.oa.com --extra-index-url http://pypi.org/simple --trusted-host pypi.org --proxy http://127.0.0.1:XXXXX # 替换对应的端口号
pip install -U setuptools
```
2. 修改pip.ini(windows)的配置
```ini
[global]
timeout = 60 ; timeout 尽量设置的大一些，否则可能来不及搜索直接timeout
proxy = http://127.0.0.1:XXXXX ; 外网访问proxy 要修改端口
index-url = http://pypi.dq.oa.com/simple/ ; 默认仓库链接 唯一
trusted-host = pypi.org ; 信任的域名
               pypi.dq.oa.com
extra-index-url = https://pypi.python.org/simple/ ; 备选仓库链接
```
再直接安装即可
```shell script
pip install -r requirements.txt
pip install -U setuptools
```

QT4A入门文档:
http://file.sng.com/browse/qta/htdocs/qt4a/lastest/index.html

QTA文档：
http://file.sng.com/browse/qta/htdocs/qtap/index.html

3、该项目依赖git.code.oa.com/edu_test/lib代码
可以在Pycharm -> Preferences -> Project Structer -> Add Content Root 添加依赖

ps：也可以通过 pip install multi-platform , 但是不保证 multi-platform 和 git.code.oa.com/edu_test/lib保持一致

