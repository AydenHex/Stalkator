from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import os
import time

driver = None

def GetDriverState():
    if(driver==None): return 0
    else: return 1

def QuitDriver():
    global driver
    if(driver != None): driver.quit()

def ConnectInsta(username, password):
    global driver
    driver = webdriver.Chrome(r'chromedriver.exe')
    driver.implicitly_wait(5)
    driver.get('https://www.instagram.com')
    try: driver.find_element_by_xpath('.//button[text()="Accepter tout"]').click()
    except: pass
    driver.find_element_by_xpath('.//input[@name="username"]').send_keys(username)
    driver.find_element_by_xpath('.//input[@name="password"]').send_keys(password)
    btn = driver.find_element_by_xpath ('.//button[@class="sqdOP  L3NKy   y3zKF     "]/div')
    driver.execute_script ("arguments[0].click();",btn)
    try:
        btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
        driver.execute_script ("arguments[0].click();",btn)
        btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
        driver.execute_script ("arguments[0].click();",btn)
    except: return 0
    return 1

def GetFollowers(accountName):
        global driver
        tab1 = [] #Store abonnements
        tab2 = [] #Store abonnés

        driver.get('https://www.instagram.com/'+accountName)

        try:
            lnks = driver.find_elements_by_tag_name("a")
            for lnk in lnks: 
                if('following' in lnk.get_attribute('href')):
                    driver.execute_script ("arguments[0].click();",lnk)
                    break
            pop_up_window = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))
            time.sleep(2)
        except:
            return tab2, tab1

        inc = 0; tmpL = 0; lim = 10
        while(inc<lim):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight; var scrolldown=arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;return scrolldown;', pop_up_window)
            time.sleep(0.5)
            elements = driver.find_elements_by_css_selector("*[class='FPmhX notranslate  _0imsa ']")
            tmp = len(elements)
            if(tmp == tmpL):
                inc = inc+1
            else:
                inc = 0
            tmpL = tmp

        elements = driver.find_elements_by_css_selector("*[class='FPmhX notranslate  _0imsa ']")
        for element in elements:
            title = element.get_attribute('title')
            tab1.append(title)

        lnks = driver.find_elements_by_tag_name("a")
        for lnk in lnks: 
            if('followers' in lnk.get_attribute('href')):
                driver.execute_script ("arguments[0].click();",lnk)
                break
        pop_up_window = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))
        time.sleep(2)

        inc = 0; tmpL = 0; lim = 10
        while(inc<lim):
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight; var scrolldown=arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;return scrolldown;', pop_up_window)
            time.sleep(0.5)
            elements = driver.find_elements_by_css_selector("*[class='FPmhX notranslate  _0imsa ']")
            tmp = len(elements)
            if(tmp == tmpL):
                inc = inc+1
            else:
                inc = 0
            tmpL = tmp

        elements = driver.find_elements_by_css_selector("*[class='FPmhX notranslate  _0imsa ']")
        for element in elements:
            title = element.get_attribute('title')
            tab2.append(title)
            
        print("Store finished")
        return tab2, tab1
        
def GetPhotos(accountName):
    global driver
    tabUrl = []

    driver.get('https://www.instagram.com/'+accountName)

    #Scroll
    scrolldown=driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    last_count = 0
    while(last_count!=scrolldown):
        last_count = scrolldown
        time.sleep(1)
        scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        time.sleep(1)
        #elements = driver.find_elements_by_xpath('.//img')
        elements = driver.find_elements_by_css_selector("*[class='FFVAD']")
        for element in elements:
            url = element.get_attribute('src')
            if(type(url) is str and url.find('http') >= 0):
                if(not url in tabUrl):
                    tabUrl.append(url)
            
    driver.get('https://www.instagram.com/'+accountName+'/tagged')
    time.sleep(5)

    scrolldown=driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
    last_count = 0
    while(last_count!=scrolldown):
        last_count = scrolldown
        time.sleep(1)
        scrolldown = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var scrolldown=document.body.scrollHeight;return scrolldown;")
        time.sleep(1)
        elements = driver.find_elements_by_css_selector("*[class='FFVAD']")
        for element in elements:
            url = element.get_attribute('src')
            if(type(url) is str and url.find('http') >= 0):
                if(not url in tabUrl):
                    tabUrl.append(url)
                    
    if(not os.path.isdir(os.getcwd()+'\\Photos')):
        os.mkdir(os.getcwd()+'\\Photos')
    if(not os.path.isdir(os.getcwd()+'\\Photos\\'+accountName)):
        os.mkdir(os.getcwd()+'\\Photos\\'+accountName)
        
    i = 1
    for element in tabUrl:
        response = requests.get(element, timeout=10)
        if(response):
            file = open(os.getcwd()+'\\Photos\\'+accountName+'\\'+accountName + str(i) + '.jpg', 'wb')
            file.write(response.content)
            file.close()
            i = i+1