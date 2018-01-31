#!/usr/bin/env python
import time
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.action_chains import ActionChains
from passwords import IFIRMA_USER, IFIRMA_PASS

service = service.Service('/usr/bin/chromedriver')
service.start()
capabilities = {}#'chrome.binary': '/path/to/custom/chrome'}
driver = webdriver.Remote(service.service_url, capabilities)


driver.get('https://www.ifirma.pl/app')

elem = driver.find_element_by_name("login")
elem.send_keys(IFIRMA_USER)
elem = driver.find_element_by_name("password")
elem.send_keys(IFIRMA_PASS)
elem.submit()

elem = driver.find_element_by_xpath("//ul//a[contains(., 'Faktury')]")
ActionChains(driver).move_to_element(elem).perform()

time.sleep(0.1)

elem = driver.find_element_by_xpath("//ul//a[contains(., 'Inne przychody')]")
elem.click()

while True:

    elem = driver.find_element_by_xpath("//a[contains(., 'RADFVUDI-03-')]")
    elem.click()
    
    delete = driver.find_element_by_xpath("//a[contains(., 'usuń')]")
    delete.click()
    
    yes = driver.find_element_by_xpath("//a[contains(., 'tak')]")
    yes.click()
    

time.sleep(5) # Let the user actually see something!
driver.quit()

