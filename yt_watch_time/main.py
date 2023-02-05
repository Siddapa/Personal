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
    sleep(4)
    
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
    # Every 200 is about one month's worth of videos
    for i in range(0, 10):
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        sleep(.1)
        print(i)
    
    watch_times = driver.find_elements(By.ID, 'progress')
    watch_times = list(map(splice_watch_time, watch_times))
    watch_times = watch_times[0:watch_times.index(0)] # Removes extraneous 0% watch times

    video_lengths = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-thumbnail-overlay-time-status-renderer')
    video_lengths = list(map(splice_video_length, video_lengths))
    video_lengths = video_lengths[0:video_lengths.index((0, 0))] # Removes extraneous 0 second video lengths 

    print(watch_times)
    print(video_lengths)
    print(len(watch_times))
    print(len(video_lengths))
    final_time_watched = total_watch_time(watch_times, video_lengths) / 60 / 60
    print(final_time_watched)


def total_watch_time(watch_times, video_lengths):
    total_watch_time = 0
    for i, watch_time in enumerate(watch_times):
        if i <= len(video_lengths) - 1:
            # Video lengths indexed to grab seconds, not time stamp
            total_watch_time += watch_time * video_lengths[i][1]
            print(str(watch_time) + ' - ' + str(video_lengths[i][0]))
    return total_watch_time


def splice_watch_time(video):
    attribute = video.get_attribute('style')
    if attribute == '':
        return 0
    decimal = float(attribute[7:-2]) / 100
    return decimal


def splice_video_length(n):
    n = n.text
    if n == 'SHORTS':
        return 0
    times = n.split(":") # Seconds, Minutes, Hours
    if times[0] == '':
        return (0, 0)
    seconds = 0
    minutes = 0
    hours = 0
    if len(times) == 1:
        seconds = int(times[0])
    if len(times) == 2:
        seconds = int(times[1])
        minutes = int(times[0])
    if len(times) == 3:
        seconds = int(times[2])
        minutes = int(times[1])
        hours = int(times[0])
    return (n, seconds + minutes * 60 + hours * 3600)



if __name__ == '__main__':
    start_headless_browser()