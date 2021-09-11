from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import socket

HOST = '127.0.0.1' #LAN
PORT = 1111

SEND_PATH = os.getcwd()+'\\'

def SendFile(fileName):
        print("Envoi de ", fileName, " ...")
        fileSize = os.path.getsize(SEND_PATH+fileName)
        s.sendall(str(fileSize).encode())
        time.sleep(0.05)
        fp = open(SEND_PATH+fileName, 'rb')
        s.sendall(fp.read())
        fp.close()

def MakeFile(tab_abon, tab_abon2):
    #Make a follow file
    fp = open("ClientReport.txt", 'w')
    fp.write('[')
    for i in range(len(tab_abon)):
        if(i < len(tab_abon)-1):
            fp.write(tab_abon[i]+', ')
        else:
            fp.write(tab_abon[i]+']\n\n[')
    for i in range(len(tab_abon2)):
        if(i < len(tab_abon2)-1):
            fp.write(tab_abon2[i]+', ')
        else:
            fp.write(tab_abon2[i]+']')
    fp.close()

def ParseFile(fileName):
        tabTmp = []
        fp = open(fileName, 'r')
        content = fp.read()
        i = 0
        while(i < len(content)):
            while(i < len(content) and content[i] != '['): i += 1
            tabTmp.append([])
            i += 1
            while(i < len(content) and content[i] != ']'):
                name = ''
                while(content[i] != ',' and content[i] != ']'):
                    name += content[i]
                    i += 1
                tabTmp[len(tabTmp)-1].append(name)
                if(content[i] == ','): i += 2
        fp.close()
        return tabTmp

def StoreFollow(accountName):
    
    tab1 = [] #Store abonnements
    tab2 = [] #Store abonnés
    
    driver.get('https://www.instagram.com/'+accountName)

    #nbrFollowing = driver.find_element_by_xpath('.//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a/span').text
    #nbrFollower = driver.find_element_by_xpath('.//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span').text

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

    MakeFile(tab1, tab2)
    print("Store finished")

#==========================================#
    
stalker_username = ''
stalker_password = ''
if('Client.conf' in os.listdir(os.getcwd())):
    tabTmp = ParseFile('Client.conf')
    stalker_username = tabTmp[0][0]
    stalker_password = tabTmp[1][0]
    HOST = tabTmp[2][0]
else:
    print('Configuration file not found, we will create one for you...')
    HOST = input('Server IP address >> ')
    stalker_username = input('type your username >> ')
    stalker_password = input('type your password >> ')
    fp = open("Client.conf", 'w')
    fp.write('username = ['+stalker_username+']')
    fp.write('\npassword = ['+stalker_password+']')
    fp.write('\serverIP = ['+HOST+']')
    fp.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
s.connect((HOST, PORT))

driver = webdriver.Chrome(r'chromedriver.exe')
driver.implicitly_wait(10)
driver.get('https://www.instagram.com')
driver.find_element_by_xpath('.//button[text()="Accepter tout"]').click()
driver.find_element_by_xpath('.//input[@name="username"]').send_keys(stalker_username)
driver.find_element_by_xpath('.//input[@name="password"]').send_keys(stalker_password)
btn = driver.find_element_by_xpath ('.//button[@class="sqdOP  L3NKy   y3zKF     "]/div')
driver.execute_script ("arguments[0].click();",btn)
btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
driver.execute_script ("arguments[0].click();",btn)
btn = driver.find_element_by_xpath('.//button[text()="Plus tard"]')
driver.execute_script ("arguments[0].click();",btn)

signal = ''
while("Quit" not in signal):
    signal = s.recv(2048).decode()
    if("StartScraping_" in signal):
        StoreFollow(signal[14::])
        SendFile('ClientReport.txt')
print("Client déconnecté !")
driver.quit()
