import hashlib

def calculate_md5(input_string):
    # 创建 MD5 对象
    md5 = hashlib.md5()

    # 将字符串转换为字节对象并更新 MD5 对象
    md5.update(input_string.encode('utf-8'))

    # 获取 MD5 哈希值的十六进制表示
    md5_value = md5.hexdigest()

    return md5_value