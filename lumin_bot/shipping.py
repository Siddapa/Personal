from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from time import sleep

url = 'https://www.luminskin.com/checkout/P1vaDlIluxeOky5CvDQQfKo581ExiRoC'
text_tag = 'css-5n0o6f'
select_tag = 'css-u3h2ay'
checkbox_tag = 'css-9087pv'
confirm_tag = 'css-c0j2xj'
filler_fields = ['', 'Blah', 'Boi', '1234 Tablechair Ave', '', 'New York City', '52722', '5634206969']
select_fields = ['US', 'IA', '+1']

options = Options()
options.add_argument("window-size=1920,1080")
driver = webdriver.Chrome(chrome_options=options)
driver.delete_all_cookies()
driver.get(url)

text_elems = driver.find_elements_by_class_name(text_tag)
for index, elem in enumerate(text_elems):
    elem.send_keys(filler_fields[index])

select_elems = driver.find_elements_by_class_name(select_tag)
for index, elem in enumerate(select_elems):
    select_obj = Select(elem)
    select_obj.select_by_value(select_fields[index])

checkbox_elem = driver.find_element_by_class_name(checkbox_tag)
checkbox_elem.click()

confirm_shipping_elem = driver.find_element_by_class_name(confirm_tag)
confirm_shipping_elem.click()

sleep(1)
driver.close()