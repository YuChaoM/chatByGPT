class ErrorCode:
    SUCCESS = (0, "ok")
    PARAMS_ERROR = (40000, "请求参数错误")
    NOT_LOGIN_ERROR = (40100, "未登录")
    NO_AUTH_ERROR = (40101, "无权限")
    NOT_FOUND_ERROR = (40400, "请求数据不存在")
    FORBIDDEN_ERROR = (40300, "禁止访问")
    SYSTEM_ERROR = (50000, "系统内部异常")
    OPERATION_ERROR = (50001, "操作失败")

    # def __init__(self, code, message):
    #     self.code = code
    #     self.message = message

    def __str__(self):
        return f"ErrorCode: {self.code}, Message: {self.message}"

    @classmethod
    def get_code(cls, error):
        return error[0]

    @classmethod
    def get_message(cls, error):
        return error[1]

# 示例用法
# print(ErrorCode.get_code(ErrorCode.PARAMS_ERROR))  # 输出: 40000
# print(ErrorCode.get_message(ErrorCode.PARAMS_ERROR))  # 输出: 请求参数错误
# print(ErrorCode.SUCCESS)
