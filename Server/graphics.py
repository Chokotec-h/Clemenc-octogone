import tkinter as tk
import socket
from _thread import start_new_thread
import os

server = os.popen('hostname -I').read().split(" ")[0]
gamestatuses = []


currentPlayer = 0


class Window(tk.Tk):
    def __init__(self,thread) -> None:
        super().__init__()

        
        self.title("Server")
        self.iconphoto(True,tk.PhotoImage("logo2.ico"))
        self.geometry("360x360")
        self.resizable(width=False, height=False)
        self.gamestatusestk = tk.Variable()
        self.gamestatusestk.set([])
        tk.Label(self,text="Games",bg="black",fg="white").pack(fill="both")
        tk.Listbox(self,listvariable=self.gamestatusestk,bg="black",fg="white",height=16).pack(fill="both")

        self.Ipadress = tk.Label(self,text="*"*len(server),bg="black",fg="white",height=2)

        self.ip_clear = tk.BooleanVar()
        self.ip_clear.set(False)
        tk.Checkbutton(self, text='Show server IP',variable=self.ip_clear, onvalue=True, offvalue=False, bg = "black",fg="white",selectcolor="black",activebackground="dark gray",activeforeground="white",highlightcolor="white", command=self.showip).pack(fill="both")
        self.Ipadress.pack(fill="both")

        start_new_thread(run_server,(thread,))

    def showip(self):
        self.Ipadress.destroy()

        if self.ip_clear.get() :
            self.Ipadress = tk.Label(self,text=server,bg="black",fg="white",height=2)
        else :
            self.Ipadress = tk.Label(self,text="*"*len(server),bg="black",fg="white",height=2)

        self.Ipadress.pack(fill="both")




def run_server(thread):
    global currentPlayer
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port = 5555


    try :
        s.bind((server,port))
    except socket.error as e :
        str(e)
    s.listen(100)
    print("Waiting for a connection, Server Started")
    while True :
        conn,addr = s.accept()
        print("Connected to :",addr)
        
        start_new_thread(thread,(conn, currentPlayer))
        currentPlayer += 1

