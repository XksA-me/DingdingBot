from time import time
import hmac
import hashlib
import base64
import urllib.parse
import requests


'''
钉钉机器人相关设置
'''



'''
钉钉机器人数字签名计算
'''
def get_digest():
    timestamp = str(round(time() * 1000))
    secret = '你的钉钉加签密钥'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # print(timestamp)
    # print(sign)
    return f"&timestamp={timestamp}&sign={sign}"


# 发送消息
def warning_bot(message, title):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":title,
            "text": message
        },
        "at": {
        "atMobiles": [
            "要@的用户的手机号"  # 要@对象的手机号，在文本message里也需要加上@用户的手机号
        ],
        "isAtAll": False # 是否要@所有人
        }
    }
    # 机器人链接地址，发post请求 向钉钉机器人传递指令
    webhook_url = '你自己的钉钉机器人Webhook链接'
    # 利用requests发送post请求
    req = requests.post(webhook_url+get_digest(), json=data)
    # print(req.status_code)
    return