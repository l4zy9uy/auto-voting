from time import sleep

from seleniumbase import SB
import time
from twocaptcha import TwoCaptcha
import re
from dotenv import load_dotenv
import os
load_dotenv()

solver = TwoCaptcha(os.getenv("TOKEN"))

account = input("Nhập tài khoản: ")
password = input("Nhập mật khẩu: ")
option = input("Chọn mức đánh giá (0-4): ")

with SB(uc=True, headless=False) as sb:
    sb.open("https://ctt-sis.hust.edu.vn")
    sb.type('[value="Tài khoản"]', f'{account}')
    sb.execute_script(
        f"document.getElementById('ctl00_ctl00_contentPane_MainPanel_MainContent_tbPassword_I').value = '{password}';")

    # Retrieve the entered password to check if it's set
    typed_password = sb.execute_script(
        "return document.getElementById('ctl00_ctl00_contentPane_MainPanel_MainContent_tbPassword_I').value;")
    captcha_element = sb.find_element("#ctl00_ctl00_contentPane_MainPanel_MainContent_ASPxCaptcha1_IMGD")
    captcha_element.screenshot("captcha.png")

    result = solver.normal('captcha.png')
    code = result['code']

    sb.execute_script(
        f"document.getElementById('ctl00_ctl00_contentPane_MainPanel_MainContent_ASPxCaptcha1_TB_I').value = '{code}';")

    typed_captcha = sb.execute_script(
        "return document.getElementById('ctl00_ctl00_contentPane_MainPanel_MainContent_ASPxCaptcha1_TB_I').value;")

    sb.click("#ctl00_ctl00_contentPane_MainPanel_MainContent_btLogin_CD")
    time.sleep(3)

    full_text = sb.get_text("#ctl00_ctl00_contentPane_MainPanel_MainContent_lbFirstText")

    match = re.search(r"\b(\d+)\b", full_text)
    num_class = 0
    if match:
        num_class = match.group(1)
    else:
        "Not found"
        exit(1)

    print("remain class: ", num_class)



    for it in range(int(num_class)):
        rbl_element = sb.find_element("//*[contains(@id, 'formLayout_RBL_')]")
        rbl_element_id = rbl_element.get_attribute("id")
        match = re.search(r"RBL_(\d+)", rbl_element_id)
        num = 0
        if match:
            num = match.group(1)
        else:
            "Not found"
            exit(1)
        print("remain num: ", num)

        form_elements = sb.find_elements(
            "//*[starts-with(@id, 'ctl00_ctl00_contentPane_MainPanel_MainContent_formLayout_')]")

        count = 0  # Initialize counter

        for element in form_elements:
            element_id = element.get_attribute("id")

            # Check if ID ends with a number using regex
            if re.match(r"ctl00_ctl00_contentPane_MainPanel_MainContent_formLayout_\d+$", element_id):
                count += 1

        print(f"🔹 Total matching IDs: {count}")

        for i in range(0, count-2):
            sb.click(f"#ctl00_ctl00_contentPane_MainPanel_MainContent_formLayout_RBL_{int(num) + i}_RB{option}")

        sb.click("#ctl00_ctl00_contentPane_MainPanel_MainContent_formLayout_submitButton")
        time.sleep(2)

