# pip install selenium
# pip install webdriver-manager 
# pip install fake_useragent 
# pip install faker
import time
import random
import datetime
import faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains

# GET A RANDOM NAME
f = faker.Faker()
namez = f.name()

# GET RANDOM DATE VALUE
DATE = datetime.datetime.today() + datetime.timedelta(days=random.randint(1,9))
datez = datetime.datetime.strftime(DATE, '%m-%d-%Y')

# FAKE EMAIL ADDRESS CONSTRUCTOR (SO THEY CAN'T BLOCK)
domains = ['@hotmail.com', '@gmail.com', '@protonmail.com', '@yahoo.com']
arr = namez.lower().split()
sender = arr[0] + arr[1] + domains[random.randint(0,3)]

age = random.randint(30,65)

# ARRAY OF MESSAGE STRINGS
text = ["You have been reported to the local police department as well as state and federal authorities.", "<WHATEVER YOU WANT TO SEND>"]

inquiry = text[random.randint(0,len(text)-1)]

# CREATE AGENT AND DRIVER
ua = UserAgent()
userAgent = ua.random

options = webdriver.ChromeOptions()
options.add_argument("--incognito") 
options.add_argument(f"user-agent={userAgent}")
options.add_argument("start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# OPTION TO RUN WITHOUT EXPLICITLY OPENING UP CHROME (RUNS IN BACKGROUND)
# SOME WEBSITES MAY BE ABLE TO DETECT THIS, BUT NOT AMATEURE CRIMINALS.
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# GET PAGE
driver.get("<URL OF PAGE SOLICITING ILLEGAL SERVICES>")

time.sleep(2)

open_button = driver.find_element("xpath", '//*[@id="header"]/div[2]/div[1]/span')
open_button.click()

time.sleep(2)

# GET DOM VARS
fname = driver.find_element("xpath", '//*[@id="booking_name"]')
date = driver.find_element("xpath", '//*[@id="booking_date"]')
email = driver.find_element("xpath", '//*[@id="booking_email"]')
ttime = driver.find_element("xpath", '//*[@id="booking_time"]')
dtime = Select(driver.find_element("xpath", '//*[@id="booking_time_unit"]')).select_by_visible_text('hours')
text = driver.find_element("xpath", '//*[@id="booking_info"]')

# FILL OUT THE FORM
fname.send_keys(f'{namez}')
date.send_keys(f'{datez}')
email.send_keys(f'{sender}')
ttime.send_keys('1')
text.send_keys(f'{inquiry}')

time.sleep(2)

driver.execute_script("document.getElementById('booking_date').removeAttribute('readonly')")
driver.execute_script(f"document.getElementById('booking_date').setAttribute('value', '{datez}')")

driver.find_element("xpath", '//*[@id="booking_time_unit"]').click()

time.sleep(10)

# REQUIRED FOR THE SPECIFIC PAGE IT WAS USED FOR
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()

# GET THE CAPTCHA TEXT VALUE
reCaptcha = driver.find_element("xpath", '//*[@id="booking_request_form"]/div[6]/div/div[1]').text

# SOLVE THE CAPTCHA

'''The captcha that this program hacked used a serialization of "o" and " " empty spaces. Another algorithm
could have been used to solve this (optimized) but only four chars ['7' & 'T'] and ['Z' & 'I'] were found to 
have a similar row-by-row char count. So we just let it make a best guess which wasn't an issue. Since this program
was scheduled through a scheduling tool, we had our retry params set to "3" - but this is out-of-scope for this demo.'''

dictionary = {"5226114":'9', "5225225":'8', "7111111":['7', 'T'], "4116225":'6', "7161125":'5', "1222711":'4',
              "5212125":'3', "5211227":'2', "1221117":'1', "3233323":'0', "6226226":'B', "5211125":'C', "6222226":'D',
              "7114117":'E', "7114111":'F', "5211425":'G', "2227222":'H', "1111125":'J', "2332332":'K', "1111117":'L', 
              "2443222":'M', "2333332":'N', "5222225":'O', "6226111":'P', "5222325":'Q', "6226222":'R', "5215125":'S',
              "2222225":'U', "2222221":'V', "2223442":'W', "2221222":'X', "2221111":'Y', "7111117":['Z','I']}

nums = ['','','','']

with open("./captcha.txt", 'w+') as f1:
    f1.write(reCaptcha)
    f1.close()

with open("./captcha.txt", 'r') as f2:
    for line in f2.readlines():
        top = [i for i in line]
        letters = [top[:9],top[9:18],top[18:27],top[27:36]]

        for idx in range(4):
            nums[idx] += str(len([i for i in letters[idx] if i != ' ']))
            
solution = ''
for val in nums:
    ltr = dictionary.get(val, 'A')
    if isinstance(ltr, list):
        ltr = ltr[random.randint(0, len(ltr)-1)]
    solution += ltr

# DEBUGGING/VALIDATE CAPTCHA WAS CORRECTLY DETERMINED
print(solution)

# HACK THE HTML SCRIPT TO REMOVE LOCKS ON ELEMENTS
driver.execute_script("document.getElementById('bookingDefaultReal').removeAttribute('aria-invalid')")
driver.execute_script("document.getElementById('bookingDefaultReal').removeAttribute('autocomplete')")

# GET THE CAPTCHA INPUT TEXTBOX
captcha = driver.find_element("xpath", '//*[@id="bookingDefaultReal"]')

# REQUIRED FOR PROCESSING
time.sleep(1)

# CLICK THE CAPTCHA INPUT BOX AND INPUT THE SOLVED CAPTCHA
actions = ActionChains(driver)
actions.click(captcha)
captcha.send_keys(f'{solution}')

# REQUIRED TIME FOR PROCESSING
time.sleep(5)

# FIND THE SUBMISSION BUTTON REQUESTING ILLEGAL SERVICES
button = driver.find_element("xpath", '//*[@id="btn_submit_booking"]')
button.click()

# REQUIRED TIME FOR PROCESSING SUBMISSION
time.sleep(2)

# IF SUCCESSFUL, THIS HTML ELEMENT WOULD BE INCLUDED IN THE DOM. 
success = driver.find_element(By.CLASS_NAME, "booking_request_box_sent").text

now = datetime.datetime.now()
success = success + " " + now.strftime("%Y-%m-%d %H:%M:%S")

# LOG THE SUCCESSFUL BOT SUBMISSION IN LOGS
with open("./logs.txt", "a") as file:
    file.write(success)
    file.close()

# CLOSE THE CONNECTION
driver.quit()
