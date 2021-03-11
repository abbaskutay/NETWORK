import tkinter as tk
import socket
import threading
from tkinter import filedialog
import os
from functools import partial
import sender as tcpsender
import receiver  as tcpreceiver
import receiverudp as udpreceiver
import senderudp as udpsender
import pygame
pygame.init()


sound_data = {'Horn-call.mp3':'1th sound played',"Solo-trumpet.mp3":'2th sound played',"Cinematic.mp3":'3th sound played',
              "Congratulations.mp3":'4th sound played',"Happy-and-positive.mp3":'5th sound played',
              "Reggae-instrumental.mp3":'6th sound played'}

def send_message(mssg):
    
    return mssg

def recieve_message(mssg):
    print(mssg)
    if 'wwwxx' in mssg:
        return True
    for a in sound_data.values():
        if a in mssg:
            playMuisc(mssg)
    return mssg


def playMuisc(name):
    name_sound = list(sound_data.keys())[list(sound_data.values()).index(name.strip('\n'))]
    pygame.mixer.music.load(name_sound)
    pygame.mixer.music.play()


def config_loc_msg(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=tk.NORMAL)
        if chatBox.index('end') != None:
            LineNumber = float(chatBox.index('end'))-1.0
            chatBox.insert(tk.END, "YOU: " + messageText)
            chatBox.tag_add("YOU", LineNumber, LineNumber+0.4)
            chatBox.config(state=tk.DISABLED)
            chatBox.yview(tk.END)

def config_rec_message(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=tk.NORMAL)
        if chatBox.index('end') != None:
            try:
                LineNumber = float(chatBox.index('end'))-1.0
            except:
                pass
            chatBox.insert(tk.END, "PARTNER: " + messageText)
            chatBox.tag_add("PARTNER", LineNumber, LineNumber+0.6)
            chatBox.config(state=tk.DISABLED)
            chatBox.yview(tk.END)

def get_con_info(chatBox, messageText):
    if messageText != '':
        chatBox.config(state=tk.NORMAL)
        if chatBox.index('end') != None:
            chatBox.insert(tk.END, messageText+'\n')
            chatBox.config(state=tk.DISABLED)
            chatBox.yview(tk.END)


class Chat_GUI:
    def     __init__(self,connection='', ip='', selected_prot=''):
        self.base = tk.Tk()
        self.base.title("Chat Window")
        self.base.geometry("430x450")
        self.base.resizable(width="false", height="false")
        self.base.resizable(width="false", height="false")
        self.base.configure(bg="lavender")
        self.s_connection = connection
        self.s_ip = ip
        self.s_port = 5555
        self.c_port = 5556
        self.s_protocol = selected_prot

        self.path = ""
        self.server_socket = connection
        threading.Thread(target=self.receive_start).start()
        
        self.chatBox = tk.Text(self.base, bd=0, height="8", width="40", font="Helvetica", )
        self.chatBox.config(state="disabled")
        self.sb = tk.Scrollbar(self.base, command=self.chatBox.yview)

        self.nameLabel = tk.Label(self.base, bg='snow', width=10, text='No files sent or received yet.')

        self.browseButton = tk.Button(self.base, font="Helvetica", text=u"Browse", width="40", height=5,
                                      bd=0, activebackground="#BDE096", justify="center",
                                      command=self.browse_function)
        self.cancelButton = tk.Button(self.base, text='Cancel Upload', command=self.cancel_function)

        self.downloadButton = tk.Button(self.base, text='Download File', command=self.download_function)

        self.chatBox['yscrollcommand'] = self.sb.set
        
        self.sendButton = tk.Button(self.base, font="Helvetica", text=u"SEND", width="50", height=5,
                            bd=0, activebackground="#BDE096", justify="center",
                            command=self.onClick)
        
        self.select_sound = tk.Button(self.base, font="Helvetica", text="\u266a", width="50", height=5,
                                    bd=0, activebackground="#BDE096", justify="center",
                                    command=self.generate_sound)

        self.textBox = tk.Text(self.base, bd=0,  width="17", height="5", font="Helvetica")
        self.textBox.bind("<Return>", self.removeKeyboardFocus)
        self.textBox.bind("<KeyRelease-Return>", self.onEnterButtonPressed)
        self.sb.place(x=370, y=5, height=350)
        self.chatBox.place(x=15, y=5, height=350, width=355)


        self.browseButton.place(x=365, y=390, height=50, width=60)
        self.nameLabel.place(x=15, y=360, height=25, width=180)
        self.sendButton.place(x=255, y=390, height=50, width=50)
        self.select_sound.place(x=310, y=390, height=50, width=50)
        self.textBox.place(x=15, y=390, height=50, width=240)

        # threading.Thread(target=self.ReceiveData).start()

        self.base.mainloop()

    def browse_function(self):
        path=filedialog.askopenfilename()
        self.nameLabel.config(text=(os.path.basename(path)))
        self.path=path
        self.cancelButton.place(x=250,y=360,height=25,width=160)

    def cancel_function(self):
        self.path=''
        self.nameLabel.config(text='')
        self.cancelButton.destroy()
        self.cancelButton = tk.Button(self.base, text='Cancel Upload', command=self.cancel_function)


    def on_receive(self,name):
        self.nameLabel.config(text=name)
        self.downloadButton.place(x=250,y=360,height=25,width=160)

    def download_function(self):
        path = filedialog.asksaveasfilename()
        if self.s_protocol == "tcp":
            self.server_socket.sendall(send_message("wwwxx").encode("utf-8"))
            tcpreceiver.connectTCP(path)

        elif self.s_protocol == "udp":
            self.server_socket.sendto(send_message("wwwxx").encode("utf-8"),(self.s_ip,self.c_port))
            udpreceiver.receiverudp(path)

        self.downloadButton.destroy()
        self.downloadButton = tk.Button(self.base, text='Download File', command=self.download_function)
        self.nameLabel.config(text="Received successfully.")

    def sender_function(self):
        print(3213123)
        if self.s_protocol=='tcp':
            print(self.s_ip)
            self.file_tcp_sender = tcpsender.TcpSender(self.s_ip[0],self.path)

        else:
            self.file_udp_sender=udpsender.UdpSender(self.s_ip,self.path)

        self.nameLabel.config(text='Sent succseffully.')
        self.cancelButton.destroy()
        self.cancelButton = tk.Button(self.base, text='Cancel Upload', command=self.cancel_function)
        print('hiii')

    def receive_start(self):
        if self.s_protocol == "tcp":
            while 1:
                try:
                    data = self.server_socket.recv(1024).decode("utf-8")
                except Exception as m:
                    get_con_info(self.chatBox, '\n partner left \n')
                    break
                if data != '':
                    print(data)
                    data1 = recieve_message(data)

                    if data1 == True: #if we got file
                        print(1111111)
                        if self.path!="":
                            self.sender_function()

                    elif "adanax_" in data1:
                        name=data1.split("adanax_")[-1]
                        name = os.path.basename(name)
                        name2 = data1.split("adanax_")[0]
                        self.on_receive(name)
                        config_rec_message(self.chatBox, name2)

                    else:
                        config_rec_message(self.chatBox, data1)
                else:
                    get_con_info(self.chatBox, '\n partner left \n')
                    self.server_socket.close()
                    break


        elif self.s_protocol == "udp":
            print('hi')
            while 1:
                try:
                    data, address = self.server_socket.recvfrom(1024)
                    data = data.decode("utf-8")
                    print("wowamk")
                except:
                    get_con_info(self.chatBox, '\n partner left\n')
                    print("tÃ¼hamk")
                    break

                if data != '':
                    print(data)
                    data1 = recieve_message(data)
                    if data1 == True: #if we got file
                        print(1111111)
                        if self.path!="":
                            print(99999)
                            self.sender_function()

                    elif "adanax_" in data1:
                        name=data1.split("adanax_")[-1]
                        name = os.path.basename(name)
                        name2 = data1.split("adanax_")[0]
                        self.on_receive(name)
                        config_rec_message(self.chatBox, name2)

                    else:
                        config_rec_message(self.chatBox,data1)

                else:
                    get_con_info(self.chatBox, '\n partner left \n')
                    break

    def onClick(self):
        messageText = str(self.textBox.get("0.0", tk.END))
        if self.path !='':
            messageText+='adanax_{}'.format(self.path)

        config_loc_msg(self.chatBox, messageText.split('adanax_')[0])
        self.chatBox.yview(tk.END)
        self.textBox.delete("0.0", tk.END)
        if self.s_protocol == "tcp":
            self.server_socket.sendall(send_message(messageText).encode("utf-8"))

        else:
            self.server_socket.sendto(send_message(messageText).encode("utf-8"),(self.s_ip,self.c_port))

    def onEnterButtonPressed(self, event):
        self.textBox.config(state="normal")
        self.onClick()

    def removeKeyboardFocus(self, event):
        self.textBox.config(state="disabled")

    def generate_sound(self):
        self.base1 = tk.Tk()
        self.base1.title("Select an Sound")
        self.base1.geometry("550x150")



        self.j = 1
        for i, v in sound_data.items():
            tk.Button(self.base1, font="Helvetica", text=v, bd=0, activebackground="#BDE096", justify="left",
                               command=partial(self.genrate_sound_index,i)).pack(side="left")
            self.j +=1

    def genrate_sound_index(self,ind):
        self.textBox.insert('end',sound_data[ind])
        self.textBox.tag_add('start',"1.0","1.06")
        self.textBox.tag_config("start",foreground='blue')

class Main_GUI(tk.Frame):
    def __init__(self,parent):
        self.parent = parent
        tk.Label(self.parent, text="Abbas and Harun Chat Tool v1.0",bg='lavender', fg="black", font=("arial", 15, "bold italic")) \
            .grid(column=0, row=0, sticky="WE", padx=0,columnspan=4)
        tk.Label(self.parent, text="Destination IP: ", fg="black",bg='lavender', font=("arial", 10)) \
            .grid(column=0, row=1)
        self.destinationIP = tk.Entry(self.parent)
        self.destinationIP.insert(tk.END,'192.168.1.106')
        self.destinationIP.grid(column=2, row=1)
        self.frame2=tk.Frame(self.parent,highlightbackground="black",bg='lavender', highlightcolor="black", highlightthickness=2,width=280, height=100)
        self.frame2.grid(row=2,column=0,columnspan=3,pady=10)
        self.frame2.grid_propagate(False)
        tk.Label(self.frame2, text="Desired Protocol: ", fg="black", font=("arial", 10),bg='lavender') \
            .grid(column=0, row=2,columnspan=1)
        self.var_protocol = tk.StringVar()
        self.var_protocol.set('tcp')
        self.protocol_type1 = tk.Radiobutton(self.frame2, text="TCP", variable=self.var_protocol,bg='lavender', value="tcp") \
            .grid(column=1, row=2)
        self.protocol_type2 = tk.Radiobutton(self.frame2, text="UDP", variable=self.var_protocol, bg='lavender',value="udp") \
            .grid(column=2, row=2)
        self.remaining=0
        self.submit_button = tk.Button(self.frame2, text=u'Start Chatting',command=self.countdown, bg='lavender',width=20)
        self.submit_button.grid(row=3,column=1,pady=10,columnspan=2)
        self.parent.mainloop()

    def countdown(self):
        self.label11 = tk.Label(self.frame2, text="Waiting for Connection", fg="red",
                                font=("arial", 12),bg='lavender').grid(column=1, row=4,columnspan=3)
        host_ip = self.destinationIP.get()
        host_port = 5555
        selected_prot = self.var_protocol.get()
        threading.Thread(target=self.start_connection, args=(host_ip, host_port, selected_prot)).start()

    def start_connection(self,host, port, protocol):
        self.l=[]
        self.host = host
        self.port = port
        self.protocol = protocol
        self.server_socket = None
        if self.protocol == "tcp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            self.server_socket.listen(1)
            self.label11 = tk.Label(self.frame2, text="Waiting for Connection", bg='lavender',fg="red",
                                    font=("arial", 12)).grid(column=1, row=4,columnspan=3)
            while True:
                conn, address = self.server_socket.accept()
                self.label11 = tk.Label(self.parent, text="Connected....").grid(column=1, row=4)

                Chat_GUI(conn, address, self.protocol)

        elif self.protocol == "udp":
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", int(self.port)))
            while True:
                # a=p1_server_gui_chat.Chat_GUI()
                # message, addr =threading.Thread(target=self.server_socket.recvfrom(1024)).start()
                # p1_server_gui_chat.Chat_GUI,args=("", self.host, self.protocol)
                message, addr = self.server_socket.recvfrom(1024)
                self.label11 = tk.Label(self.parent, text="Connected....").grid(column=1,row=4)

                # p1_server_gui_chat.Chat_GUI("", self.host, self.protocol)
                if message.decode("utf-8") == "udp":
                    ab=Chat_GUI(self.server_socket, self.host, self.protocol)
                    # threading.Thread(target=ab,args=("", self.host, self.protocol)).start()
                # ab.chatBox.insert('end',message)
                #     threading.Thread(target=p1_server_gui_chat.Chat_GUI,args=("", self.host, self.protocol)).start()
                    # a=p1_server_gui_chat.Chat_GUI('', self.host, self.protocol)
            # a.chatBox.insert(tk.END, message)
                # threading.Thread(target=self.start_connection, args=(host_ip, host_port, selected_prot)).start()
                # threading.Thread(target=p1_server_gui_chat.Chat_GUI,args=("", self.host, self.protocol)).start()
        else:
            print("try connection again")

def main():
    root = tk.Tk()
    root.title("Chat Tool v1.0--Server")
    # root.wm_attributes('-transparentcolor', root['bg'])
    root.configure(bg='lavender')
    app = Main_GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
    # a=Chat_GUI('tcp','localhost','1111')