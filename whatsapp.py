# Download the helper library from https://www.twilio.com/docs/python/install
'''
import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
client = Client('ACfaab33d10bd83f88e9ff761b53de7c71', '387c8d39006f3db2333c86675ce8a04c')

message = client.messages \
    .create(
         body='mal',
         from_='whatsapp:+14155238886',
         to='whatsapp:+77477993986'
     )

print(message.sid)
'''
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(r'C:\Users\18010\Downloads\chromedriver_win32\chromedriver.exe')
driver.get('https://web.whatsapp.com/')

name = input('Enter the name of user or group : ')
msg = input('Enter your message : ')
count = int(input('Enter the count : '))
wait = WebDriverWait(driver = driver, timeout = 900)
time.sleep(5)  # Let the user actually see something!
user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
user.click()

msg_box = driver.find_element_by_class_name('_2S1VP')
#msg += '\n this is a system generated message'

for i in range(count):
        msg_box.send_keys(msg)
        button = driver.find_element_by_class_name('_35EW6')
        button.click()

wait = WebDriverWait(driver = driver, timeout = 600)
driver.close()
'''
from selenium import webdriver

driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
driver.get('http://www.google.com/');
time.sleep(5)  # Let the user actually see something!
search_box = driver.find_element_by_name('q')
search_box.send_keys('ChromeDriver')
search_box.submit()
driver.quit()
'''
