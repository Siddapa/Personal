from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os


chrome_options = Options()
chrome_options.add_argument('--incognito')
chrome_driver = os.getcwd() + '\\google_meet_automation\\chromedriver.exe'
print(chrome_driver)

driver = webdriver.Chrome(options=chrome_options, executable_path=chrome_driver)
driver.get('https://meet.google.com/lookup/fzrwffebc2?authuser=1&hs=179')
