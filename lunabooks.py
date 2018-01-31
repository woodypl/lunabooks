#!/usr/bin/env python
import time
import re
import locale
import datetime
import os

from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.action_chains import ActionChains
from passwords import IFIRMA_USER, IFIRMA_PASS


def add_invoice(driver, date, number, consumer, vat8gross):
    elem = driver.find_element_by_xpath("//a[contains(., 'Przychód uniwersalny VAT')]")
    elem.click()
    
    numberfield = driver.find_element_by_xpath("//form//div[label='Numer']//input")
    numberfield.send_keys(number)
    
    subject = driver.find_element_by_xpath("//form//div[label='Opis']//textarea")
    subject.send_keys("Usługa transportowa")
   
    re.compile("NIP: ([0-9]+)\nDane do faktury").search(text)
    
    register = driver.find_element_by_xpath("//form//div[label='Kasa fiskalna']//input")
    if consumer != register.is_selected(): #XOR. Toggle the checkbox if needed
        register.click()


    datefield = driver.find_element_by_xpath("//form//div[label='Data wystawienia']//input")
    datefield.clear()
    datefield.send_keys(date)
    
    calc = driver.find_element_by_xpath("//form//div[label='Licz od']//input")
    calc.clear()
    calc.send_keys("brutto\n")
    time.sleep(0.3)

    vat8grossfield = driver.find_element_by_xpath("//form//tr[td='8%']/td/input[@type='text']")
    vat8grossfield.send_keys(vat8gross)
    
    noreceipt = driver.find_element_by_xpath("//form//div[label='Sprzedaż bezrachunkowa']//input")
    if noreceipt.is_selected():
        noreceipt.click()

    submit = driver.find_element_by_xpath("//form//a[contains(., 'Zatwierdź')]")
    submit.click()
    
    driver.find_element_by_xpath("//a[contains(., 'powrót')]").click()
    
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


for filename in sorted(os.listdir("invoices")):

    f=open("invoices/"+filename,'r')
    text=f.read()
    f.close()

    consumer = not re.compile("NIP: ([0-9]+)\nDane do faktury").search(text)
    number = re.compile("Numer Faktury: (.*)").search(text).group(1)
    datetext = re.compile("Data faktury: (.*)").search(text).group(1).split()
    datetext[1] = datetext[1][:3]
    locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
    date = datetime.datetime.strptime(" ".join(datetext), "%d %b %Y").strftime("%d-%m-%Y")
    grossval = re.compile('Wartość brutto\n\n(.*) PLN').search(text).group(1)

    add_invoice(driver, date, number, consumer, grossval)
    os.remove("invoices/"+filename)

driver.quit()
