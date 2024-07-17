import os
import sys
import time

import ddddocr
import requests
import winsound

import UrpNet
import UrpUtils

# Author : Core_65536
# Version : 1.0
# License : Apache-2.0
# Special Thanks To github.com/sml2h3/ddddocr
def main():
    # 初始化OCR
    sys.stdout = open(os.devnull, 'w')
    ocr = ddddocr.DdddOcr()
    ocr.set_ranges(6)
    sys.stdout = sys.__stdout__

    account = input('输入学号:')
    password = input('输入密码:')

    # URL
    login_page_url = 'http://jwstudent.lnu.edu.cn/'
    login_url = 'http://jwstudent.lnu.edu.cn/j_spring_security_check'
    auth_url = 'http://jwstudent.lnu.edu.cn/student/courseSelect/courseSelect/index?mobile=false'

    # 创建一个会话对象
    session = requests.Session()
    # 获取验证码
    captcha_code = UrpUtils.get_captcha(session, ocr)
    # 获取 tokenValue
    token_value = UrpUtils.GetTokenValue(session, login_page_url)
    # 加密密码
    encrypted_password = UrpUtils.md5_encode(password)

    # 提交表单数据
    payload = {
        'j_username': account,
        'j_password': encrypted_password,
        'j_captcha': captcha_code,
        'tokenValue': token_value  # 使用从页面提取的 tokenValue
    }

    # 发送POST请求，提交登录表单
    rp = UrpNet.Loop_POST(session, login_url, payload)
    # 访问需要认证的页面
    rp = UrpNet.Loop_GET(session, auth_url, {})
    # 输出页面内容
    if rp.text.find("选课") != -1:
        print("登录成功 !")
    else:
        print("登录失败 !")
        quit()

    YearCode = input('输入学年(例如2023-2024):')
    TermCode = input('输入学期(1 or 2):')

    UrpUtils.GetCourseGrades(session, YearCode, TermCode)

    os.system('pause')


if __name__ == "__main__":
    main()
