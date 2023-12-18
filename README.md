# chatByGPT
一个基于Flask，使用讯飞火星认知大模型开发的智能问答系统（纯后端）

## 项目运行

先运行sql文件夹里的db.sql生成对应的库表结构。

然后去官网开通创建下面三个密钥
地址：https://xinghuo.xfyun.cn/

在app.py同一级目录创建config.ini，在里面配置下面的信息
```text
[credentials]
APP_ID = xxxxxx
API_SECRET = xxxxxxxxxxx
API_KEY = xxxxxxxxxxx
```

也可以在AIService.py中直接修改，代码如下

```python
def initialize_spark_api():

    # 配置你的密钥
    appid = "xxxxxxid"
    api_secret = "xxxxxxxxkey"
    api_key = "xxxxxxxxxxx"


    # 用于配置大模型版本，默认“general/generalv2”
    domain = "generalv3"  # v3.0版本
    Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
    return appid, api_key, api_secret, domain, Spark_url
```
安装好依赖后，不出以外，你就可以运行项目了。