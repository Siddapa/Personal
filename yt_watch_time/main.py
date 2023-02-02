from selenium import webdriver 
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def start_headless_browser():
    driver = uc.Chrome()
    login = r'https://accounts.google.com/signin/v2/identifier?continue='
    driver.get(login)

    username = driver.find_element(By.CLASS_NAME, 'zHQkBf')
    username.click()
    username.send_keys('vishnuschalla@gmail.com')
    sleep(1)

    next = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ')
    next.click()
    sleep(3)
    
    password = driver.find_element(By.CLASS_NAME, 'zHQkBf')
    password.click()
    password.send_keys('siddappavam11$')
    sleep(1)

    submit = driver.find_element(By.CLASS_NAME, 'VfPpkd-LgbsSe-OWXEXe-k8QpJ')
    submit.click()
    sleep(4)

    history_feed = r'https://www.youtube.com/feed/history'
    driver.get(history_feed)
    
    screen_height = driver.execute_script("return window.screen.height;")
    print(screen_height)
    # Every 200 is about one month's worth of videos
    for i in range(0, 10):
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        sleep(.1)
        print(i)
    
    percent_watched = driver.find_elements(By.ID, 'progress')
    for video in percent_watched:
        print(video.get_attribute('style'))

    video_length = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-thumbnail-overlay-time-status-renderer')
    for video in video_length:
        print(video.text)

    sleep(10)


if __name__ == '__main__':
    start_headless_browser()