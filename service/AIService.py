import configparser
from service import SparkApi
from flask import current_app



def initialize_spark_api():
    # # 创建应用上下文
    # with app.app_context():
    #     # 从 Flask 应用程序的配置中获取密钥信息
    #     appid = current_app.config['credentials']['appid']
    #     api_secret = current_app.config['credentials']['api_secret']
    #     api_key = current_app.config['credentials']['api_key']

    appid = current_app.config['APP_ID']
    api_secret = current_app.config['API_SECRET']
    api_key = current_app.config['API_KEY']
    # 可以在应用的任何地方使用这些配置项
    # print(appid, api_secret, api_key)

    # 用于配置大模型版本，默认“general/generalv2”
    domain = "generalv3"  # v3.0版本
    Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
    return appid, api_key, api_secret, domain, Spark_url


def send(message_list):
    text = []
    # 先构造上下文
    for message in reversed(message_list):
        if message.userId == 0:
            appendText("assistant", message.content, text)
        else:
            appendText("user", message.content, text)

    question = checklen(text)
    SparkApi.answer = ""
    print("星火:", end="")
    appid, api_key, api_secret, domain, Spark_url = initialize_spark_api()
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)  # 封装的请求参数的构造和打印响应
    return SparkApi.answer


def appendText(role, content, text):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)


'''
这个函数用于计算 text 列表中所有对话内容的字符总数
'''


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]  # 上下文超的就删除最早的一条
    return text


# if __name__ == '__main__':
#     while (1):
#         Input = input("\n" + "我:")
#         question = checklen(getText("user", Input))  # 上下文列表
#         SparkApi.answer = ""
#         print("星火:", end="")
#         SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)  # 封装的请求参数的构造和打印响应
#         getText("assistant", SparkApi.answer)  # 将回答添加到列表，作为下一次提问的上下文了，assistant表示AI的历史回答结果
#         # print(str(text))
