import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 '
                  'Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://jwstudent.lnu.edu.cn/login',
}


def Set_headers(new_headers):
    headers['Referer'] = new_headers


# 任何一个处理成功抛出错误
def Loop_GET(session, url, data):
    flag = 0
    rp = None
    while flag == 0:
        try:
            rp = session.get(url, data=data, headers=headers, timeout=5)
            flag = 1
        except requests.exceptions.RequestException as e:
            flag = 0
            print('Timeout,Retrying...')
    return rp


def Loop_POST(session, url, data):
    flag = 0
    rp = None
    while flag == 0:
        try:
            rp = session.post(url, data=data, headers=headers, timeout=10)
            flag = 1
        except requests.exceptions.RequestException as e:
            flag = 0
            print('Timeout,Retrying...')
    return rp
