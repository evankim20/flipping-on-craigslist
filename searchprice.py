from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re 
import numpy as np 

def find_prices(item, zipcode):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver')

    #get the site
    driver.get('https://searchtempest.com')
    time.sleep(5)

    #input our information for the item
    driver.find_element_by_xpath('//*[@id="keywords"]').send_keys(item) #use item name provided
    driver.find_element_by_xpath('//*[@id="location"]').send_keys(zipcode)#use zipcode provided
    miles_dropdown = Select(driver.find_element_by_xpath('//*[@id="radius"]'))
    miles_dropdown.select_by_visible_text('any distance')
    driver.find_element_by_class_name("_3esBk").click()
    time.sleep(5)
    element = driver.find_element_by_id('hybridSearchPreferencesToggle')
    element.click()

    element = driver.find_element_by_xpath("//input[@id='showcl_hybrid']/parent::div")
    time.sleep(3)
    element.click()

    element = driver.find_element_by_xpath("//input[@id='showat_hybrid']/parent::div")
    element.click()

    element = driver.find_element_by_xpath("//input[@id='showaz_hybrid']/parent::div")
    element.click()

    element = driver.find_element_by_xpath("//input[@id='showzr_hybrid']/parent::div")
    element.click()

    driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div/div/header/nav[2]/button').click()

    time.sleep(5)    
    text_list = driver.find_elements_by_class_name('result-item')
    ebay_price = []
    for n in text_list:
        a = re.findall(r"\$[^\]]+\n", n.text)
        try:
            str_a = ''.join(a) 
            bid_ind = str_a.index('(')
            str_a = str_a[1:bid_ind]
            str_a = str_a.replace(',','') 
            price = float(str_a)
        except:
            str_a = a[0][1:-1]
            str_a = str_a.replace(',', '')
            price = float(str_a)
        ebay_price.append(price)

    driver.close()
    if len(ebay_price) != 0:
        upper_appx = np.percentile(ebay_price, 75)
        lower_appx = np.percentile(ebay_price, 25)
        median_appx = np.percentile(ebay_price, 50)
        driver.quit()
        return [lower_appx, median_appx, upper_appx]
    else:
        driver.quit()
        return [None, None, None]

