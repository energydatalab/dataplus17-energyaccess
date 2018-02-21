from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
browser.get('https://garv.gov.in/garv2/dashboard/village/597114')
wait = WebDriverWait(browser, 10)
important = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".gridtotal")))

totalhh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right").get_attribute('innerHTML'))
totaleh = int(important.find_element_by_css_selector(".gridtotallabel+ .text-right + .text-right").get_attribute('innerHTML'))
print(totalhh)
print(totaleh)
#print(browser.page_source)