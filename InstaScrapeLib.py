from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def ConnectInsta(username, password):
    driver = webdriver.Chrome(r'chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('https://www.instagram.com')
    driver.find_element_by_xpath('.//button[text()="Accepter tout"]').click()
    driver.find_element_by_xpath('.//input[@name="username"]').send_keys(username)
    driver.find_element_by_xpath('.//input[@name="password"]').send_keys(password)
    btn = driver.find_element_by_xpath ('.//button[@class="sqdOP  L3NKy   y3zKF     "]/div')
    driver.execute_script ("arguments[0].click();",btn)
    btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
    driver.execute_script ("arguments[0].click();",btn)
    btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
    driver.execute_script ("arguments[0].click();",btn)

def StoreFollow(accountName):

        tab1 = [] #Store abonnements
        tab2 = [] #Store abonnés

        driver.get('https://www.instagram.com/'+accountName)

        lnks = driver.find_elements_by_tag_name("a")
        for lnk in lnks: 
            if('following' in lnk.get_attribute('href')):
                driver.execute_script ("arguments[0].click();",lnk)
                break
        pop_up_window = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='isgrP']")))
        time.sleep(2)

        inc = 0; tmpL = 0; lim = 15
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

        inc = 0; tmpL = 0; lim = 15
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