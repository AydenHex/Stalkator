import os
import socket
import pandas as pd
from datetime import date

from tkinter import *
from tkinter import messagebox
from FileLib import *
from InstaScrapeLib import *

class Interface(Tk):
    def __init__(self):
        super().__init__()
        
        self.targetUsername = ''
        self.stalker_username = ''
        self.stalker_password = ''
        self.IsWorking = False
        self.tab_Client = []
        self.serverThread = None
        
        self.resizable(False,False)
        self.iconbitmap('Assets/icon.ico')
        self.title('Stalkator 0.3')
        self.protocol("WM_DELETE_WINDOW", self.quit_Button)
         # Widgets
        self.clientsButton = Button(self, text='Clients ('+str(len(self.tab_Client))+')', command=lambda: self.openClientsTab(), padx=10, pady=5)
        self.clientsButton.after(10, self.updateText())
        instaButton = Button(self, text='Instagram', command=lambda: self.openInstaTab(), padx=10, pady=5)
        fbButton = Button(self, text='Facebook', command=lambda: myClick(), padx=10, pady=5)
        linkButton = Button(self, text='Linkedin', command=lambda: myClick(), padx=10, pady=5)
        quitButton = Button(self, text='Quit', command=lambda: self.quit_Button(), padx=10, pady=5)
        tarEntry_label = Label(self, text="Target:")
        self.tarEntry = Entry(self, width = 25)
        self.textBox = Text(self, width=40, background="gray100", wrap=WORD, state='disabled')

         # Grid
        self.clientsButton.grid(row=1, column=0, padx=10, pady=5)
        instaButton.grid(row=7, column=0, padx=10, pady=5)
        fbButton.grid(row=8, column=0, padx=10, pady=5)
        linkButton.grid(row=9, column=0, padx=10, pady=5)
        quitButton.grid(row=16, column=0, padx=10, pady=5)

        tarEntry_label.grid(row=0, column=7, padx=0, pady=10)
        self.tarEntry.grid(row=0, column=8, padx=0, pady=10)
        self.textBox.grid(row=1, column=3, columnspan=16, rowspan=16, padx=10, pady=10)
        
        if('Server.conf' in os.listdir(os.getcwd())):
            tabTmp = ParseFile('Server.conf')
            self.stalker_username = tabTmp[0][0]
            self.stalker_password = tabTmp[1][0]
        else:
            self.openConfigTab("Configuration file not found, please fill in the informations required:")
            
        self.Write_textBox('  Welcome to Stalkator !\n\nType a target\'s name and scrape :)')
        
    def quit_Button(self):
        for client in self.tab_Client: client.running = False
        self.serverThread.running = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP
        s.connect(('127.0.0.1', 1111)) #Fake connection to turn off the server
        if('MainReport.txt' in os.listdir(os.getcwd())): os.remove('MainReport.txt')
        QuitDriver()
        self.destroy()
        
    def updateText(self):
        global clientTab
        self.clientsButton['text']=('Clients ('+str(len(self.tab_Client))+')')
        try:
            if(clientTab.state() == "normal"):
                if(len(clientTab.winfo_children()) - len(self.tab_Client) < 2):
                    clientTab.title('Clients ('+str(len(self.tab_Client))+')')
                    for widget in clientTab.winfo_children():
                        widget.destroy()
                    addressLabel = Label(clientTab, text="List of address (IP : Port)", font= ('Helvetica 10 underline'))
                    addressLabel.pack()
                    for i in range(len(self.tab_Client)):
                        clientLabel = Label(clientTab, text="Client "+str(i+1)+": [ "+str(self.tab_Client[i].ip)+' : '+str(self.tab_Client[i].port)+' ]')
                        clientLabel.pack()
                    closeButton = Button(clientTab, text='Close', command=lambda: self.close_ClientsTab(), padx=10, pady=5)
                    closeButton.pack(side=BOTTOM)
        except: pass
        self.clientsButton.after(1000, self.updateText)
        
    def Write_textBox(self, text):
        self.textBox.configure(state='normal')
        self.textBox.insert(END, text)
        self.textBox.configure(state='disabled')

    def Clear_textBox(self):
        self.textBox.configure(state='normal')
        self.textBox.delete(1.0, END)
        self.textBox.configure(state='disabled')
        
    # ===== Configuration Tab ===== #

    def submitConfig(self, tab):
        self.stalker_username = usernameEntry.get()
        self.stalker_password = passwordEntry.get()
        fp = open("Server.conf", 'w')
        fp.write('username = ['+self.stalker_username+']')
        fp.write('\npassword = ['+self.stalker_password+']')
        fp.close()
        self.deiconify()
        tab.destroy()
        
    def openConfigTab(self, text):
        global usernameEntry
        global passwordEntry
        self.withdraw()
        configTab = Toplevel(self)
        configTab.title('Configuration')
        configTab.focus()
        InfoLabel = Label(configTab, text=text)
        usernameLabel = Label(configTab, text="Username:")
        usernameEntry = Entry(configTab, width = 30)
        passwordLabel = Label(configTab, text="Password:")
        passwordEntry = Entry(configTab, width = 30)
        clientsButton = Button(configTab, text='Submit', command=lambda: self.submitConfig(configTab), padx=10, pady=5)
         # Grid
        InfoLabel.grid(row=0, column=0, padx=10, pady=5, columnspan=8)
        usernameLabel.grid(row=1, column=1, padx=0, pady=5)
        usernameEntry.grid(row=1, column=2, padx=0, pady=5)
        passwordLabel.grid(row=2, column=1, padx=0, pady=5)
        passwordEntry.grid(row=2, column=2, padx=0, pady=5)
        clientsButton.grid(row=3, column=2, padx=10, pady=5)

    # ===== Clients Management ===== #
            
    def close_ClientsTab(self):
        global clientTab
        clientTab.destroy()
           
    def openClientsTab(self):
        global clientTab
        try:
            if(clientTab.state() == "normal"): clientTab.focus()
        except:
            clientTab = Toplevel(self)
            clientTab.title('Clients ('+str(len(self.tab_Client))+')')
            clientTab.resizable(False,False)
            clientTab.iconbitmap('Assets/icon.ico')
            clientTab.geometry('350x450')
            addressLabel = Label(clientTab, text="List of address (IP : Port)", font= ('Helvetica 10 underline'))
            addressLabel.pack()
            for i in range(len(self.tab_Client)):
                clientLabel = Label(clientTab, text="Client "+str(i+1)+": [ "+str(self.tab_Client[i].ip)+' : '+str(self.tab_Client[i].port)+' ]')
                clientLabel.pack()
            closeButton = Button(clientTab, text='Close', command=lambda: self.close_ClientsTab(), padx=10, pady=5)
            closeButton.pack(side=BOTTOM)
        
    # ===== Insta ===== #
    
    def GetFollowers_Insta(self):
        self.targetUsername = self.tarEntry.get()
        if(self.targetUsername != ''):
            flag = 1
            if(GetDriverState() == 0):
                self.Clear_textBox()
                self.Write_textBox('Please wait for your browser to load...')
                flag = ConnectInsta(self.stalker_username, self.stalker_password)
                self.Clear_textBox()
                if(flag == 0):
                    QuitDriver()
                    self.openConfigTab('The account specified is not valid, please change the informations !')
            if(flag == 1):
                for client in self.tab_Client:
                    client.scrapeType = 1
                    client.scrapeBool = True
                self.IsWorking = True
                tab1, tab2 = GetFollowers(self.targetUsername)
                if(tab1 != [] or tab2 != []):
                    MakeFile('MainReport.txt', tab1, tab2)
                    follow = {'Followers': tab1, 'Following': tab2}
                    df = pd.DataFrame.from_dict(follow, orient='index').transpose()
                    df.to_csv(str(date.today())+'.csv')
                    self.Write_textBox('  Followers scrapped !\n(check directory for a .csv file)')
                else:
                    messagebox.showerror('Error', 'The taget\'s username is wrong !')
                    instaTab.focus()
                self.IsWorking = False
        else:
            self.Clear_textBox()
            self.Write_textBox('No target specified !')
            messagebox.showerror('Error', 'No target specified !')
            instaTab.focus()

    def GetPhoto_Insta(self):
        self.targetUsername = self.tarEntry.get()
        if(self.targetUsername != ''):
            flag = 1
            if(GetDriverState() == 0):
                self.Clear_textBox()
                self.Write_textBox('Please wait for your browser to load...')
                flag = ConnectInsta(self.stalker_username, self.stalker_password)
                self.Clear_textBox()
                if(flag == 0):
                    QuitDriver()
                    self.openConfigTab('The account specified is not valid, please change the informations !')
            if(flag == 1):
                for client in self.tab_Client:
                    client.scrapeType = 2
                    client.scrapeBool = True
                GetPhotos(self.targetUsername)
                self.Clear_textBox()
                self.Write_textBox('Photos scrapped !')
        else:
            self.Clear_textBox()
            self.Write_textBox('No target specified !')
            messagebox.showerror('Error', 'No target specified !')
            instaTab.focus()

    def openInstaTab(self):
        global instaTab
        try:
            if(instaTab.state() == "normal"): instaTab.focus()
        except:
            instaTab = Toplevel(self)
            instaTab.title('Instagram')
            instaTab.resizable(False,False)
            instaTab.iconbitmap('Assets/icon.ico')
            frame = LabelFrame(instaTab, padx=60, pady=80)
            getFollow_Button = Button(frame, text='Get Followers', command=lambda: self.GetFollowers_Insta(), padx=10, pady=5)
            getPhoto_Button = Button(frame, text='Get Photos', command=lambda: self.GetPhoto_Insta(), padx=10, pady=5)
            getLikes_Button = Button(frame, text='Get Likes/Comments', command=lambda: self.GetPhoto_Insta(), padx=10, pady=5)
            standby_Button = Button(frame, text='Activate automated standby', bg='red', command=lambda: self.GetPhoto_Insta(), padx=10, pady=5)
            frame.pack(padx=5, pady=5)
            getFollow_Button.pack(expand=True, fill=BOTH, pady=10)
            getPhoto_Button.pack(expand=True, fill=BOTH, pady=10)
            getLikes_Button.pack(expand=True, fill=BOTH, pady=10)
            standby_Button.pack(expand=True, fill=BOTH, pady=10)
