import sys
import os
import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from tkinter.filedialog import askopenfilename
import subprocess
from multiprocessing import Process, Queue
from queue import Empty
from turtle import width
import datetime

today = datetime.date.today()
save_path = os.path.join(os.getcwd(),"data\\"+str(today)+'\\')
global file_names
file_names = ''

if not os.path.exists(save_path):
    os.makedirs(save_path)
if not os.path.exists(save_path+'images\\'):
    os.makedirs(save_path+'images\\')

DELAY1 = 60
DELAY2 = 20
q = Queue()


class OCRNets(tk.Tk):
    def __init__(self):
        # initial window after running the code
        super().__init__()
        self.filepath = False
        self.title("OCRNets")
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file='logo.png'))
        self.geometry("1200x550+100+100")

        self.label_1 = tk.Label(self, text="Welcome to OCRNets!",font=(16))
        self.label_1.place(x=600, y=100,anchor='center')

        self.label_2 = tk.Label(self, text="Please upload you image in the next page for text extraction", font=("bold", 11))
        self.label_2.place(x=600, y=140,anchor='center')

        self.btn_1 = ttk.Button(self, text="Proceed", width='20',command=lambda:destroy_widgets() or self.upload_page())
        self.btn_1.place(x=600,y=180,anchor='center')

        def destroy_widgets():
            self.label_1.destroy()
            self.label_2.destroy()
            self.btn_1.destroy()

    def upload_page(self):
        self.label_1 = tk.Label(self,text="Please upload an image of the document you would like to extract text from",font=('bold',12))
        self.label_1.place(x=600,y=100,anchor="center")

        self.btn_1 = ttk.Button(self, text='Open Image',width=25, command=lambda: self.open_file() or destroy_widgets() or self.upload_verification_page())
        self.btn_1.place(x=600,y=140,anchor="center")

        def destroy_widgets():
            self.label_1.destroy()
            self.btn_1.destroy()

    def open_file(self):
        self.filepath = askopenfilename() 

    def upload_verification_page(self):
        if self.filepath:
            self.label_1 = tk.Label(self,text="The File you have uploaded is: "+str(self.filepath),font=('bold',11))
            self.label_1.place(x=600,y=100,anchor="center")
            
            self.btn_1 = ttk.Button(self, text='Change Uploaded File', command=lambda: destroy_widgets() or self.upload_page())
            self.btn_1.place(x=500,y=150,anchor='center')

            self.btn_2 = ttk.Button(self,text="Use this Image",command=lambda: destroy_widgets() or self.extract_text() or self.onStart())
            self.btn_2.place(x=700,y=150,anchor="center")
        else:
            self.upload_page()

        def destroy_widgets():
            self.label_1.destroy()
            self.btn_1.destroy()
            self.btn_2.destroy()
    
    def extract_text(self):
        self.label_1 = tk.Label(self, text='Extracting text from your image......')
        self.label_1.place(x=500, y=100,anchor='center')
        
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate', length=150)        
        self.progress_bar.place(x=700,y=100,anchor='center')    
        
        self.txt = tk.Text(self,width = 80, height = 7)  
        self.txt.place(x=600,y=190,anchor='center')
        self.txt.insert('end', "Logs...."+'\n')

        self.btn_1 = ttk.Button(self, text="Next ", command=lambda: destroy_widgets() or self.display_and_download())
        self.btn_1.place(x=950,y=280,anchor='center')

        def destroy_widgets():
            self.label_1.destroy()
            self.progress_bar.destroy()
            self.txt.destroy()
            self.btn_1.destroy()

    def display_and_download(self):
        os.system("start "+save_path)
        self.label_1 = tk.Label(self, text="Data Successfully Extracted!",font=(16))
        self.label_1.place(x=600, y=130,anchor='center')

        self.label_2 = tk.Label(self,text="The data has been extracted from your image. A pop-up window would have appeared to show you the file location.")
        self.label_2.place(x=600,y=170,anchor="center")

        self.label_3 = tk.Label(self,text="You can find the audio and text files saved at: "+str(save_path))
        self.label_3.place(x=600,y=200,anchor="center")

        self.btn_1 = ttk.Button(self, text="Upload Another Image", command=lambda: destroy_widgets() or self.upload_page())
        self.btn_1.place(x=310, y=320, anchor="center")

        self.btn_2 = ttk.Button(self, text="Quit", command=lambda: self.destroy())
        self.btn_2.place(x=950, y=320, anchor="center")

        def destroy_widgets():
            self.label_1.destroy()
            self.label_2.destroy()
            self.label_3.destroy()
            self.btn_1.destroy()
            self.btn_2.destroy()        
        

    def onStart(self):
        # self.startBtn.config(state=tk.DISABLED)
        self.txt.delete("1.0", tk.END)
        self.process_ = Process(target=image_digitization, args=(q, self.filepath))
        self.process_.start()
        self.progress_bar.start(DELAY2)
        self.after(DELAY1, self.onGetValue)
       
    def onGetValue(self):
       if (self.process_.is_alive()):
        self.after(DELAY1, self.onGetValue)
        return
       else:    
           try:
               self.txt.insert('end', q.get(0))
               self.txt.insert('end', "\n")
               self.progress_bar.stop()
               # self.text_file_name = file_names[0].split('\\')
               # self.audio_file_name = file_names[1].split('\\')
               # print(self.text_file_name, self.audio_file_name)
           except Empty:
                print("queue is empty")

def image_digitization(q, filepath):
    global file_names
    text = subprocess.getstatusoutput('Python image_to_text.py '+filepath+' '+save_path)
    # print(type(text[1]))
    file_names = text[1].split('\n')
    print(file_names[-1])
    q.put(text[1])

if __name__ == "__main__":
    OCRNets().mainloop()