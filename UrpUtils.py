import os
import json
import random

import UrpMD5
import UrpNet
import re

from bs4 import BeautifulSoup


# 将密码进行MD5加密
def md5_encode(password):
    return UrpMD5.hex_md5(password, "0")


# OCR获取验证码
def get_captcha(session, ocr):
    # 获取验证码
    captcha_url = 'http://jwstudent.lnu.edu.cn/img/captcha.jpg'
    response = UrpNet.Loop_GET(session, captcha_url, {})
    captcha_file = 'captcha' + str(random.randint(0, 100000)) + '.jpg'
    with open(captcha_file, 'wb') as f:
        f.write(response.content)
    # OCR识别验证码
    image = open(captcha_file, "rb").read()
    result = ocr.classification(image)
    # 排除常见识别错误
    if len(result) == 5:
        result = result[1:5]
    captcha_code = result
    print("captcha_code = " + captcha_code)
    os.remove(captcha_file)

    return result


# 获取tokenValue
def GetTokenValue(session, login_page_url):
    # 发送GET请求以获取登录页面HTML
    rp = UrpNet.Loop_GET(session, login_page_url, {})
    html = rp.text
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html, 'html.parser')
    # 提取 tokenValue
    token_value = soup.find('input', {'id': 'tokenValue'})['value']
    print(f"Token Value: {token_value}")

    return token_value


# 获取某一学期课程成绩
def GetCourseGrades(session, academic_year_code, term_code):
    # 首先获取callback前的随机生成的十位字符
    GradesUrl = 'http://jwstudent.lnu.edu.cn/student/integratedQuery/scoreQuery/allPassingScores/index'
    rp = UrpNet.Loop_GET(session, GradesUrl, data={})
    pos = rp.text.find('/callback') - 27
    token = rp.text[pos:pos + 10]
    # 拼接成绩查询url
    GradesUrl = 'http://jwstudent.lnu.edu.cn/student/integratedQuery/scoreQuery/' + token + '/allPassingScores/callback'
    rp = json.loads(UrpNet.Loop_GET(session, GradesUrl, data={}).text)
    grades = []
    # 遍历获取当前学期成绩
    for term in rp['lnList']:
        if term['cjbh'] == f'{academic_year_code}学年秋(两学期)' and term_code == '1':
            grades.extend(term['cjList'])
        elif term['cjbh'] == f'{academic_year_code}学年春(两学期)' and term_code == '2':
            grades.extend(term['cjList'])
    # 输出成绩
    # print(grades)
    for grade in grades:
        print(f"课程名称: {grade['courseName']}, 成绩: {grade['courseScore']}")
    return len(grades)
