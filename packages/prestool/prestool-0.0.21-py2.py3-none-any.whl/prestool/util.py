from loguru import logger
from bs4 import BeautifulSoup
import hashlib
import time
import requests
import json
import urllib.parse
import socket
import hmac
import base64
import yagmail
import random
import string
import telnetlib
from faker import Faker


def format_quot_str_util(pre_str, double_quot=False):
    if isinstance(pre_str, str):
        return f'"{pre_str}"' if double_quot else f"'{pre_str}'"
    if pre_str is None:
        return 'null'
    if pre_str is True:
        return 'true'
    if pre_str is False:
        return 'false'
    return str(pre_str)


# 记录日志
def logger_util(msg):
    logger.info(f'\n{msg}')


# 编码解码相关
def string_coding_util(pre_str, string_coding_type):
    if string_coding_type == 'url_encode':
        return urllib.parse.quote_plus(pre_str)
    elif string_coding_type == 'url_decode':
        return urllib.parse.unquote(pre_str)
    elif string_coding_type == 'base_64_encode':
        return base64.b64encode(pre_str)
    else:
        return pre_str


# json解析
def json_util(pre_json, to_json_type, **kwargs):
    try:
        return json.loads(pre_json) if to_json_type == 'json_load' else json.dumps(
            pre_json, ensure_ascii=False, **kwargs)
    except:
        return pre_json


# http请求
def http_client_util(url, method, data, **kwargs):
    res = requests.get(url, data, **kwargs) if method == 'GET' else requests.post(url, data, **kwargs)
    res.encoding = 'utf-8'
    return res


def time_stamp_util(timeType):
    t = time.time()
    stamp = int(t * 1000) if timeType == 'ms' else int(t)
    return stamp


# 将get类型的参数转成url形式展示拼接
def trans_data_to_url_util(url, data):
    if data:
        url = f'{url}?{"&".join([f"{k}={v}" for k, v in data.items()])}'
    return url


# 获取cookies
def get_cookies_util(url, data, method, headers):
    session = requests.Session()
    session.get(trans_data_to_url_util(url, data), headers=headers) \
        if method == 'GET' else session.post(url, data, headers=headers)
    return requests.utils.dict_from_cookiejar(session.cookies)


# 加密相关
def to_encrypt_util(pre_str, en_type, sign_key=''):
    if en_type == 'sha_256':
        return hashlib.sha256(pre_str.encode('utf-8')).hexdigest()
    if en_type == 'md5':
        md5 = hashlib.md5(sign_key.encode('utf-8'))
        md5.update(pre_str.encode('utf-8'))
        return md5.hexdigest()
    if en_type == 'hmac_256':
        return hmac.new(sign_key.encode("utf-8"), pre_str.encode("utf-8"), digestmod=hashlib.sha256).digest()


# 获取现在的时间
def get_now_time_util(format_type):
    f = '%Y-%m-%d %H:%M:%S' if format_type == '-' else '%Y%m%d%H%M%S'
    return time.strftime(f, time.localtime())


# 通过url获取ip地址
def get_ip_by_url_util(url):
    return socket.getaddrinfo(url, 'http')[0][4][0]


# 机器人
def send_robot_msg_util(msg, send_type, ding_talk_sign_key='', ding_talk_token='', qy_wechat_token=''):
    if send_type == 'dingTalk':
        url = 'https://oapi.dingtalk.com/robot/send'
        time_stamp = time_stamp_util('ms')
        pre_str = f'{time_stamp}\n{ding_talk_sign_key}'
        hmac_256_str = to_encrypt_util(pre_str, 'hmac_256', ding_talk_sign_key)
        base_64_str = string_coding_util(hmac_256_str, 'base_64_encode')
        sign = string_coding_util(base_64_str, 'url_encode')
        pre_data = {'access_token': ding_talk_token, 'timestamp': time_stamp, 'sign': sign}
    else:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send'
        pre_data = {'key': qy_wechat_token}
    url = trans_data_to_url_util(url, pre_data)
    payloads = {"msgtype": "text", "text": {"content": msg}}
    data = json_util(payloads, 'json_dump').encode('utf-8')
    http_client_util(url, 'POST', data=data, headers={'Content-Type': 'application/json'})


# 发送邮件
def send_mail_util(from_user, pwd, host, to_user, subject, content):
    yag = yagmail.SMTP(user=from_user, password=pwd, host=host)
    yag.send(to_user, subject, content)


def xml_to_dict_util(p_xml):
    soup = BeautifulSoup(p_xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {'error': 'FAIL', 'error_msg': p_xml}
    return dict([(item.name, item.text) for item in xml.find_all()])


def random_string_util(n):
    return ''.join(random.sample(string.ascii_letters + string.digits, n))


def telnet_util(host, port, command_str, flag):
    with telnetlib.Telnet(host, port) as t:
        t.write(b'\n')
        t.read_until(flag.encode())
        t.write(command_str.encode() + b'\n')
        read_until = t.read_until(flag.encode())
        try:
            res = read_until.decode('gbk')
        except:
            res = read_until.decode('utf-8')
        t.write('exit'.encode() + b'\n')
        return res.replace(flag, '')
