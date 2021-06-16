import string
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import getcwd
from time import sleep
import sys
import json
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from twocaptcha import TwoCaptcha

PATH = str(getcwd()) + "./chromedriver.exe"
options = Options()
options.headless = True  # change this to False to show the browser on screen
options.add_argument(f"user-data-dir={str(getcwd()) + 'selenium'}")
download_interval = 10

driver = webdriver.Chrome(options=options, executable_path=PATH)
driver.maximize_window()

iterations = 0
solved_captcha = 0

user = "????"
passw = "????"

driver.get("https://proxer.me/watch/24565/22/engsub")
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "loginNav")))

def start():
    global user
    global passw
    checking_status(user, passw)

def checking_status(username, password):
    try:
        driver.find_element_by_id("loginNav").click()
        driver.find_element_by_id("mod_login_username").send_keys(username)
        driver.find_element_by_id("mod_login_password").send_keys(password)
        driver.find_element_by_id("mod_login_submit").click()
        print("Logged in successfully")
    except:
        print("Already logged in!")
    checking_captcha()

def checking_donate():
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "donatecall")))
        driver.find_element_by_xpath("//div[@id='donatecall']//a[1]").click()
        print("Will not donate!")
    except:
        print("Already not donating!")
    running()

def checking_captcha():
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "g-recaptcha")))
        print("Captcha found!")
        captcha_solver()
        print("Captcha solved!")
    except:
        print("No Captcha found!")
    checking_donate()

def captcha_solver():
    print("Stareted solving!")
    global solved_captcha
    data_sitekey = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "g-recaptcha"))).get_attribute("data-sitekey")

    api_key = os.getenv('APIKEY_2CAPTCHA', 'YOUR_APIKEY_HERE')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
        sitekey=data_sitekey,
        url=driver.current_url)

    except Exception as e:
        sys.exit(e)

    else:
        solved_captcha +=1
        dresult = (json.dumps(result))
        solved_key = (dresult[dresult.find("code")+8:dresult.rfind('"')])
        driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % solved_key)
        sleep(1)
        driver.find_element_by_xpath("(//input[@type='submit'])[2]").click()

def running():
    global iterations
    global solved_captcha
    aga = True
    while aga:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "wContainer")))
            sleep(1230)
            driver.refresh()
            iterations+=1
            print("Total iterations:" + str(iterations))
            print("Captchas solved:" + str(solved_captcha))
        except:
            print("No Video")
            start()

start()
