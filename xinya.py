
# coding: utf-8


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


outfile = open('xinyawang.csv', 'a')


#deal with detailed infomation for each event
def unit(tag):
    expand_nob = tag.find_element_by_xpath(".//td[7]/a")
    expand_nob.click()
    time.sleep(2)
    driver.switch_to_window(driver.window_handles[-1])
    element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/div[2]/div/div/div[2]/div/dl[1]/dd/a")))
    financier = element.text.encode('utf-8')
    rounds = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[2]/div/dl[2]/dd").text.encode('utf-8')
    quantity = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[2]/div/dl[3]/dd").text.encode('utf-8')
    industry = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[2]/div/dl[4]/dd").text.encode('utf-8')
    date = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[2]/div/dl[5]/dd").text.encode('utf-8')
    title = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[1]/h1").text.encode('utf-8')
    describe = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[3]").text.encode('utf-8')
    investor_block = driver.find_elements(By.XPATH, "/html/body/div[5]/div[3]/div/div[1]/div[1]/div/ul/li")
    investors = []
    for n, i in enumerate(investor_block):
        investor = {}
        investor['name'] = i.find_element_by_xpath(".//div[2]/h3").text.encode('utf-8')
        investor['place'] = i.find_element_by_xpath(".//div[2]/p[1]").text.encode('utf-8')
        investor['stage'] = i.find_element_by_xpath(".//div[2]/p[2]").text.encode('utf-8')
        investors.append(investor)
    investors_string = "["
    for n, i in enumerate(investors):
        if n > 0:
            investors_string += ';'
        investors_string += i['name']
        investors_string += '|' + i['place']
        investors_string += '|' + i['stage']
    investors_string += ']'
    result = pd.DataFrame({'date': [date], 'title': [title], 'financier': [financier], 'quantity': [quantity], 'rounds': [rounds], 'industry': [industry], 'investors': [investors_string]})
    driver.close()
    driver.switch_to_window(driver.window_handles[-1])
    return result



#main flow
url = 'http://www.newseed.cn/invest'
driver = webdriver.Firefox()
driver.set_window_size(1000, 1000)
driver.get(url)
wait = WebDriverWait(driver, 30)
time.sleep(1)
#element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='loginName']")))
#element.send_keys(username)
#element = driver.find_element_by_xpath("//*[@id='pwd']")
#element.send_keys(password + Keys.ENTER)
time.sleep(2)
element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/table/tbody/tr[2]")))
EVENT_LIST = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div[3]/table/tbody/tr")
while True:
    try:
        element = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/div[2]/div[1]/b")
        element.click()
        element = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div[3]/table/tbody/tr[2]")))
        EVENT_LIST = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div[3]/table/tbody/tr")
        DATA = pd.DataFrame({'date': [], 'title': [], 'financier': [], 'quantity': [], 'rounds': [], 'industry': [], 'investors': []})
        current_url = driver.current_url
        for n, li in enumerate(EVENT_LIST):
            try:
                if n < 2:
                    continue
                DATA = pd.concat([DATA, unit(li)])
                time.sleep(2)
            except Exception as e:
                print e
                driver.close()
                driver.switch_to_window(driver.window_handles[-1])
        DATA.to_csv(outfile)
        time.sleep(1)
        nextpage = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div[3]/div[1]/div/a")[-1]
        if nextpage.text == u'下一页':
            nextpage.click()
            time.sleep(5)
        else:
            break
    except Exception as e:
        print e  
driver.quit()
outfile.close()

