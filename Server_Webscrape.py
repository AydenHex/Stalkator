    # Stalkator version 0.2 #

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import os
import time
import pandas as pd
from datetime import date
import socket
import threading

DOWNLOAD_PATH = (os.getcwd()+'\\')

def MakeFile(tab_abon, tab_abon2):
        fp = open("MainReport.txt", 'w')
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

        follow = {'Followers': tab1, 'Following': tab2}
        df = pd.DataFrame.from_dict(follow, orient='index').transpose()
        df.to_csv(str(date.today())+'.csv')

        print("Store finished")
    
#==========================================#

def CompileReports(reportName):
        tabTmp = ParseFile('MainReport.txt')
        tab_abon1 = tabTmp[0]; tab_abon2 = tabTmp[1]
        tabTmp = ParseFile(reportName)
        tab_abon12 = tabTmp[0]; tab_abon22 = tabTmp[1]

        for i in range(len(tab_abon1)):
            if(tab_abon12[i] not in tab_abon1):
                tab_abon1.append(tab_abon12[i])

        for i in range(len(tab_abon22)):
            if(tab_abon22[i] not in tab_abon2):
                tab_abon2.append(tab_abon22[i])

        MakeFile(tab_abon1, tab_abon2)

        follow = {'Followers': tab_abon2, 'Following': tab_abon1}
        df = pd.DataFrame.from_dict(follow, orient='index').transpose()
        df.to_csv(str(date.today())+'.csv')

        os.remove(reportName)
    
def DownloadFile(self, dirPath):
        fileSize = int(self.clientsocket.recv(2048).decode())
        dataSize = 0
        with open(dirPath+'Report'+self.ip+'.txt', 'wb') as file:
            while dataSize < fileSize:
                data = self.clientsocket.recv(4096)
                dataSize += len(data)
                file.write(data)
            file.close()
            print("[%s]: Report received !" % (self.ip))
        
class ClientThread(threading.Thread):
    
        def __init__(self, ip, port, clientsocket):
            threading.Thread.__init__(self)
            self.ip = ip
            self.port = port
            self.clientsocket = clientsocket
            self.scrapeBool = False
            self.running = True
            print("\n[+] Connection of %s %s" % (self.ip, self.port))

        def run(self):
            global username
            while(self.running):
                if(self.scrapeBool):
                    self.clientsocket.sendall((str('StartScraping_')+username).encode())
                    DownloadFile(self, DOWNLOAD_PATH)
                    while(not os.path.isfile('MainReport.txt')): time.sleep(1)
                    CompileReports('Report'+self.ip+'.txt')
                    print("[%s]: Reports compiled" % (self.ip))
                    self.scrapeBool = False
            self.clientsocket.sendall(str('Quit').encode())
            print("[%s]: Client disconnected..." % (self.ip))
        
tab_Client = []
        
class ServerThread(threading.Thread):
    
        def __init__(self, port):
            threading.Thread.__init__(self)
            self.running = True
            self.port = port

        def run(self):
            tcpSvr = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #SOCK_STREAM = TCP/SOCK_DGRAM = UDP #AF_INET = IPv4/AF_INET6 = IPv6
            tcpSvr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            tcpSvr.bind(("", self.port)) #Associe le port 1111 au programme (Socket)
            while(self.running):
                tcpSvr.listen(10)
                print( "\nServer: Listening...")
                (clientsocket, (ip, port)) = tcpSvr.accept()
                newthread = ClientThread(ip, port, clientsocket)
                tab_Client.append(newthread)
                newthread.daemon = True
                newthread.start()
            print('Server: Shutdown sucessfull !')
        
#===============================================================#
    
serverThread = ServerThread(1111)
serverThread.start()

stalker_username = ''
stalker_password = ''
if('Server.conf' in os.listdir(os.getcwd())):
        tabTmp = ParseFile('Server.conf')
        stalker_username = tabTmp[0][0]
        stalker_password = tabTmp[1][0]
else:
        print('Configuration file not found, we will create one for you...')
        stalker_username = input('type your username >> ')
        stalker_password = input('type your password >> ')
        fp = open("Server.conf", 'w')
        fp.write('username = ['+stalker_username+']')
        fp.write('\npassword = ['+stalker_password+']')
        fp.close()

print("\nPlease wait for your browser to load...")

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

username = ''; message = ''
print('\n     =====================')
print('     === Stalkator 0.2 ===')
print('     =====================')
while(not '2' in message):
        print('\nPlease type a number')
        print('0- Set target')
        print('1- StartScraping (target = '+username+')')
        print('2- Quit')
        message = input(" >> ")
        if(message == '0'): username = input('Set username >> ')
        elif(message == '1' and username != ''):
            for client in tab_Client: client.scrapeBool = True
            StoreFollow(username)
for client in tab_Client: client.running = False
serverThread.running = False
driver.quit()
