import time
import os
import socket

from InstaScrapeLib import *
from FileLib import *

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

ConnectInsta(stalker_username, stalker_password)

signal = ''
while("Quit" not in signal):
    signal = s.recv(2048).decode()
    if("StartScraping_" in signal):
        StoreFollow(signal[14::])
        SendFile('ClientReport.txt')
print("Client déconnecté !")
if('ClientReport.Conf' in os.listdir(os.getcwd())): os.remove('ClientReport.txt')
driver.quit()