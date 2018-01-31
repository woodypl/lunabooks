#!/usr/bin/env python
import time
import re
import locale
import datetime
import os

from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from passwords import IFIRMA_USER, IFIRMA_PASS


def add_invoice(driver, date, number, name, address, postcode, city, nip, vat8gross):
    elem = driver.find_element_by_xpath("//a[contains(., 'Przychód uniwersalny VAT')]")
    elem.click()
    
    numberfield = driver.find_element_by_xpath("//form//div[label='Numer']//input")
    numberfield.send_keys(number)
    
    subject = driver.find_element_by_xpath("//form//div[label='Opis']//textarea")
    subject.send_keys("Usługa transportowa")
   
    addbutton = driver.find_element_by_xpath("//form//div[contains(@class, 'przyciski')]//a[i[contains(@class, 'fa-plus')]]")
    addbutton.click()
   
    time.sleep(0.8)
    driver.find_element_by_xpath("//a[contains(., 'Wprowadź samodzielnie')]").click()
    time.sleep(0.8)

    buyerfield = driver.find_element_by_xpath("//form//div[label='Identyfikator']//input")
    buyerfield.send_keys("UBER-"+number.split("-")[-1])
    namefield = driver.find_element_by_xpath("//form//div[label='Nazwa firmy']//input")
    namefield.clear()
    namefield.send_keys(name)
    addrfield = driver.find_element_by_xpath("//form//div[label='Ulica, numer']//input")
    addrfield.send_keys(address)
    if nip:
        nipfield = driver.find_element_by_xpath("//form//div[label='Prefiks UE, NIP']//input[@type='text' and @maxlength=16]")
        nipfield.send_keys(nip.group(1))
    codefield = driver.find_element_by_xpath("//form//div[label='Kod pocztowy, Miejscowość']//input[@placeholder='kod pocztowy']")
    codefield.send_keys(postcode)
    cityfield = driver.find_element_by_xpath("//form//div[label='Kod pocztowy, Miejscowość']//input[@placeholder='miejscowość']")
    cityfield.send_keys(city)
    submit = driver.find_element_by_xpath("//form//a[contains(., 'zatwierdź')]")
    submit.click()
    time.sleep(1.9)

    register = driver.find_element_by_xpath("//form//div[label='Kasa fiskalna']//input")
    if bool(nip) == register.is_selected(): #XOR. Toggle the checkbox if needed
        register.click()

    datefield = driver.find_element_by_xpath("//form//div[label='Data wystawienia']//input")
    datefield.clear()
    datefield.send_keys(date)
    
    calc = driver.find_element_by_xpath("//form//div[label='Licz od']//input")
    calc.clear()
    calc.send_keys("brutto\n")
    time.sleep(1.1)

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

    details = re.compile('(.* .*)\n(.*)\n([0-9]{2}-[0-9]{3}) (.*)\n').match(text)
    name = re.compile('(.* .*)\n').match(text).group(1)
    address = re.compile('.* .*\n(.*)\n').match(text).group(1)
    postcode = re.compile('.* .*\n.*\n([0-9]{2}-[0-9]{3}) .*\n').match(text)
    city = re.compile('.* .*\n.*\n[0-9\-].*? (.*)\n').match(text)
    postcode = postcode.group(1) if postcode else '00-000'
    city = city.group(1) if city else 'brak'
    nip = re.compile("NIP: ([0-9]+)\nDane do faktury").search(text)
    number = re.compile("Numer Faktury: (.*)").search(text).group(1)
    datetext = re.compile("Data faktury: (.*)").search(text).group(1).split()
    datetext[1] = datetext[1][:3]
    locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
    date = datetime.datetime.strptime(" ".join(datetext), "%d %b %Y").strftime("%d-%m-%Y")
    grossval = re.compile('Wartość brutto\n\n(.*) PLN').search(text).group(1)

    add_invoice(driver, date, number, name, address, postcode, city, nip, grossval)
    os.remove("invoices/"+filename)

driver.quit()
