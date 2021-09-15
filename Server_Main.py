import pandas as pd
from datetime import date
import socket
import threading

from InstaScrapeLib import *
from FileLib import *

#Global variables
IsWorking = False

def CompileReports(reportName):
        tabTmp = ParseFile('MainReport.txt')
        tab_abon1 = tabTmp[0]; tab_abon2 = tabTmp[1]
        tabTmp = ParseFile(reportName)
        tab_abon12 = tabTmp[0]; tab_abon22 = tabTmp[1]

        for i in range(len(tab_abon12)):
            if(tab_abon12[i] not in tab_abon1):
                tab_abon1.append(tab_abon12[i])

        for i in range(len(tab_abon22)):
            if(tab_abon22[i] not in tab_abon2):
                tab_abon2.append(tab_abon22[i])

        MakeFile('MainReport.txt', tab_abon1, tab_abon2)

        follow = {'Followers': tab_abon1, 'Following': tab_abon2}
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
            self.scrapeType = 0
            self.running = True
            print("\n[+] Connection of %s %s" % (self.ip, self.port))

        def run(self):
            global username
            global IsWorking
            while(self.running):
                if(self.scrapeBool):
                    self.clientsocket.sendall((str('StartScraping_')+str(self.scrapeType)+username).encode())
                    DownloadFile(self, os.getcwd()+'\\')
                    while(IsWorking): time.sleep(1)
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

ConnectInsta(stalker_username, stalker_password)

username = ''; message = ''
print('\n     ======================')
print('     === Stalkator 0.2b ===')
print('     ======================')
while(message != '3'):
        print('\nPlease type a number')
        print('0- Set target')
        print('1- Get Followers (target = '+username+')')
        print('2- Get Photos')
        print('3- Quit')
        message = input(" >> ")
        if(message == '0'): username = input('Set username >> ')
        elif(message == '1' and username != ''):
            for client in tab_Client:
                client.scrapeType = int(message)
                client.scrapeBool = True
            IsWorking = True
            tab1, tab2 = GetFollowers(username)
            MakeFile('MainReport.txt', tab1, tab2)
            follow = {'Followers': tab1, 'Following': tab2}
            df = pd.DataFrame.from_dict(follow, orient='index').transpose()
            df.to_csv(str(date.today())+'.csv')
            IsWorking = False
        elif(message == '2' and username != ''):
            for client in tab_Client:
                client.scrapeType = int(message)
                client.scrapeBool = True
            GetPhotos(username)
for client in tab_Client: client.running = False
serverThread.running = False
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
s.connect(('127.0.0.1', 1111)) #Fake connection to turn off the server
if('MainReport.txt' in os.listdir(os.getcwd())): os.remove('MainReport.txt')
driver.quit()
