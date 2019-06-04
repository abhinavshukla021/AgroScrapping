from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os.path
from os import path

options = Options()
options.headless = True

district = input()
x=pd.read_csv( district + '1.csv')

browser = webdriver.Firefox()
browser.get('https://soilhealth8.dac.gov.in/HealthCard/HealthCard/HealthCardPNew?Stname=Maharashtra')
browser.implicitly_wait(25)

dist = Select(browser.find_element_by_xpath('//*[@id="Dist_cd2"]'))
dist.select_by_visible_text(district)

for mandal, village in zip(x['Mandal'], x['Village']):

    man = Select(browser.find_element_by_xpath('//*[@id="Sub_dis2"]'))
    man.select_by_visible_text(mandal)

    vil = Select(browser.find_element_by_xpath('//*[@id="village_cd2"]'))
    vil.select_by_visible_text(village)

    if(path.exists(village + ".csv")==True):
        continue
    if(mandal != 'Sillod'):
        continue

    header = ['Sample No.', 'Village Grid No.', 'Farmer Name', 'Date', 'Farm-Size', 'Lat-Long', 'Soil-Type', 'ph', 'Remarks', 'EC', 'Remarks', 'C', 'Remarks', 'N', 'Remarks', 'P', 'Remarks', 'K', 'Remarks', 'S', 'Remarks', 'Zn', 'Remarks', 'B', 'Remarks', 'Fe', 'Remarks', 'Mn', 'Remarks', 'Cu', 'Remarks']
    filename = village + '.csv'
    with open(filename, 'w+') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)

        # Clicking on the Search Button
        browser.find_element_by_xpath('//html/body/div[2]/div/div[3]/div/div[2]/form/div[3]/table/tbody/tr[7]/td/a[1]').click()
        browser.implicitly_wait(20)
        # Necessary Script
        element = browser.find_element_by_xpath("//div[@class='blockUI blockOverlay']")
        browser.execute_script("arguments[0].style.visibility='hidden'", element)

        while (1):
            for var in [1,2,3]:
                list = []
                try:
                    k=7

                    button = browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[6]/div/table/tbody/tr[' + str(var) + ']/td[11]/a')
                    browser.execute_script("arguments[0].scrollIntoView();", button)
                    button.click()
                    village_grid = browser.find_element_by_xpath('/html/body/div[2]/div/div[3]/div/div[2]/form/div[6]/div/table/tbody/tr[1]/td[2]')
                    village_grid = (BeautifulSoup(village_grid.get_attribute('outerHTML'), 'lxml').text)
                    iframe = WebDriverWait(browser, 15).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[3]/div/div[2]/form/div[5]/div/iframe")))
                    browser.switch_to.frame(iframe)
                    sample_no = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[6]/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr[5]/td[2]')
                    sample_no = (BeautifulSoup(sample_no.get_attribute('outerHTML'), 'lxml').find('div').text)
                    farmer_name = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[6]/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr[8]/td[3]')
                    farmer_name = (BeautifulSoup(farmer_name.get_attribute('outerHTML'), 'lxml').find('div').text)
                    date = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[6]/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr[15]/td[3]')
                    date = (BeautifulSoup(date.get_attribute('outerHTML'), 'lxml').find('div').text)
                    farm_size = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[6]/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr[17]/td[3]')
                    farm_size = (BeautifulSoup(farm_size.get_attribute('outerHTML'), 'lxml').find('div').text)
                    gps = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[6]/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr[18]/td[3]')
                    gps = (BeautifulSoup(gps.get_attribute('outerHTML'), 'lxml').find('div').text)
                    soil_taste = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr[9]/td[2]')
                    soil_taste = (BeautifulSoup(soil_taste.get_attribute('outerHTML'), 'lxml').find('div').text)

                    list.insert(0,sample_no)
                    list.insert(1,village_grid)
                    list.insert(2,farmer_name)
                    list.insert(3,date)
                    list.insert(4,farm_size)
                    list.insert(5,gps)
                    list.insert(6,soil_taste)

                    for i in range(12):
                        try:
                            value = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr[10]/td[2]/table/tbody/tr/td/table/tbody/tr[' + str(i+3) + ']/td[4]')
                            if BeautifulSoup(value.get_attribute('outerHTML'), 'lxml').find('div') is None:
                                value = ' '
                            else:
                                value = (BeautifulSoup(value.get_attribute('outerHTML'), 'lxml').find('div').text)
                            value1 = browser.find_element_by_xpath('/html/body/form/div[3]/span/div/table/tbody/tr[4]/td[3]/div/div[1]/div/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[2]/td[3]/table/tbody/tr/td/table/tbody/tr[10]/td[2]/table/tbody/tr/td/table/tbody/tr[' + str(i+3) + ']/td[6]')
                            if BeautifulSoup(value1.get_attribute('outerHTML'), 'lxml').find('div') is None:
                                value1 = ' '
                            else:
                                value1 = (BeautifulSoup(value1.get_attribute('outerHTML'), 'lxml').find('div').text)
                            list.insert(k, value)
                            list.insert(k+1, value1)
                            k=k+2
                        except:
                            print('1')
                            break
                    browser.switch_to.default_content()
                    csvwriter.writerow(list)
                except:
                    print('2')
                    browser.switch_to.default_content()
                    continue
            try:
                 browser.find_element_by_link_text('Next >').click()
                 browser.implicitly_wait(20)
            except:
                print('3')
                break
