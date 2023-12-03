import SparkApi
import configparser

# 读取配置文件
config = configparser.ConfigParser()
config.read('../config.ini')

# 从配置文件获取密钥信息
appid = config['Credentials']['appid']  # 填写控制台中获取的 APPID 信息
api_secret = config['Credentials']['api_secret']  # 填写控制台中获取的 APISecret 信息
api_key = config['Credentials']['api_key']  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
# domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
domain = "generalv3"  # v3.0版本
# 云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址
Spark_url = "wss://spark-api.xf-yun.com/v3.1/chat"  # v3.0环境的地址

text = []


# length = 0

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


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


if __name__ == '__main__':
    text.clear()
    while (1):
        Input = input("\n" + "我:")
        question = checklen(getText("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)  # 封装的请求参数的构造和打印响应
        getText("assistant", SparkApi.answer)  # 将回答添加到列表，作为下一次提问的上下文了，assistant表示AI的历史回答结果
        # print(str(text))