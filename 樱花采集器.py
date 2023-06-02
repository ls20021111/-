import ctypes
from tkinter.filedialog import *
import tkinter as tk
from  tkinter import *
from Download import YingHua
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
user32.SetProcessDPIAware()


W, H = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)   #匹配dpi
pro = W / 2560
w = int(1000 * pro)
h = int(600 * pro)



import threading
import requests
import webbrowser
import time
from tkinter.messagebox import showerror


class App(Frame):
    def __init__(self, master,):
        super().__init__(master)
        self.master=master
        self.pack()
        # 导入图片
        self.wx_png = PhotoImage(file="img\wx.png")

        self.canvas = tk.Canvas(master, width=w, height=h)
        # 去除画布的白边框
        self.canvas.config(highlightthickness=0)
        self.canvas.pack()

        self.canvas.create_line(0,450*pro,1000*pro,450*pro)



        self.ui()

    def ui(self):    #创建组件
        #文字大小
        font_size_1 = round(pro * 13)
        font_size_2 = round(pro * 10)
        font_size_3 = round(pro * 12)

        Label(self.master,text='视频链接:',font=('',font_size_1)).place(x=20*pro,y=20*pro)
        self.entyr_url=Entry(self.master,  font=('', font_size_2))
        self.entyr_url.place(x=150*pro, y=15*pro,width=300*pro,height=40*pro)
        Label(self.master, text='视频名称:', font=('', font_size_1)).place(x=20*pro, y=100*pro)
        self.entey_name=Entry(self.master, font=('', font_size_2))
        self.entey_name.place(x=150*pro, y=100*pro, width=300*pro, height=40*pro)
        Label(self.master,text='下载路径:', font=('', font_size_1)).place(x=20*pro, y=180*pro)
        self.entry_fill=Entry(self.master, font=('', font_size_2))
        self.entry_fill.place(x=150*pro, y=180*pro, width=210*pro, height=40*pro)
        Button(self.master, font=('', '10'),text='选择',command=self.open_file).place(x=380*pro, y=180*pro,height=40*pro,width=100*pro)


        Label(self.master, text='驱动地址:', font=('', font_size_1)).place(x=20*pro, y=260*pro)
        self.entry_drive=Entry(self.master, font=('', font_size_2))
        self.entry_drive.place(x=150*pro, y=260*pro, width=210*pro, height=40*pro)
        self.entry_drive.insert('end','driver\msedgedriver.exe')



        Label(self.master, text='进度条:', font=('', font_size_1)).place(x=20*pro, y=340*pro)
        Label(self.master, text='片段数量:', font=('',font_size_3)).place(x=600*pro, y=345*pro)
        Label(self.master, text='剩余片段:', font=('', font_size_3)).place(x=800*pro, y=345*pro)
        #片段数量
        self.sum_entry=Entry(self.master, font=('', font_size_2))
        self.sum_entry.place(x=730*pro, y=340*pro, width=50*pro, height=40*pro)
        #剩余片段
        self.residue_entry=Entry(self.master, font=('', font_size_2))
        self.residue_entry.place(x=930*pro, y=340*pro, width=50*pro, height=40*pro)
        Button(self.master, font=('', font_size_2),text='选择',command=self.open_drive).place(x=380*pro, y=260*pro,height=40*pro,width=100*pro)
        Button(self.master, font=('', font_size_2),text='开始下载',command=self._call_m3u8).place(x=650*pro, y=260*pro,height=40*pro,width=200*pro)
        Button(self.master, font=('', font_size_2),text='进入网站',command=self.open_dm).place(x=400*pro, y=500*pro,height=40*pro,width=200*pro)
        Button(self.master, font=('', font_size_2),text='下载最新驱动',command=self.open_edge).place(x=150*pro, y=500*pro,height=40*pro,width=200*pro)
        Button(self.master, font=('', font_size_2),text='捐赠作者',command=self.Toplevel_money).place(x=650*pro, y=500*pro,height=40*pro,width=200*pro)
        self.Text=Text(self.master)
        self.Text.place(x=500*pro,y=20*pro,width=480*pro,height=230*pro)
        #进度条
        self.progressbar = ttk.Progressbar(root, orient="horizontal", length=400*pro, mode="determinate",)
        self.progressbar.place(x=150*pro,y=340*pro,height=40*pro)

    def open_edge(self):
        webbrowser.open('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')

    def open_dm(self):
        webbrowser.open('https://www.yhdmz.org/')

    #打开文件_驱动程序
    def open_drive(self):

        ilepath = askopenfilename()  # 选择打开什么文件，返回文件名
        print(ilepath)
        self.entry_drive.delete(0,'end')
        self.entry_drive.insert('end',ilepath)
        # 保存文件
    def open_file(self):
        t=str(int(time.time()))
        self.filenewpath = asksaveasfilename(initialfile=f'test{t}.ts')
        self.entry_fill.delete(0,'end')
        self.entry_fill.insert('end',self.filenewpath)

    def _call_m3u8(self):
        self.Text.insert('end','程序启动中...\n')
        t=threading.Thread(target=self.call_m3u8)
        t.daemon=True
        t.start()
    def Toplevel_money(self):
        top=Toplevel(root)
        top.resizable(width=False, height=False)
        w_w=int(400*pro)
        h_h=int(400*pro)
        top.geometry(f'{w_w}x{h_h}+%d+%d' % ((W - w_w) / 2, (H - h_h) / 2))  # 窗口的大小
        top.iconbitmap('img/ico.ico')
        top.title('捐赠作者')
        Label(top,image=self.wx_png).pack()


    #将所有的下载地址导入进来
    def call_m3u8(self):
        try:
            if    self.entry_fill.get()!='':
                Download_m3u8_url=YingHua(self.entyr_url.get(),self.entry_drive.get())
                listurl=Download_m3u8_url.xia_zai_m3u8()
                self.progressbar['maximum'] = len(listurl)

                self.sum_entry.insert('end',str(len(listurl)))
                self.residue_entry.insert('end', str(len(listurl)))
                self.entey_name.insert('end',(Download_m3u8_url.name))
                self.Text.insert('end', '下载中请勿关闭软件\n')

                sum=0
                for i in listurl:
                    video=requests.get(i).content
                    with open(f'{ self.entry_fill.get()}','ab')as w:
                        w.write(video)
                        sum += 1
                    self.progressbar['value'] = sum
                    self.residue_entry.delete(0, 'end')
                    self.residue_entry.insert('end', str(len(listurl) - sum))
            else:
                showerror(title="错误",message="参数错误")
                self.Text.insert('end', '程序出错\n')
        except:
            self.Text.insert('end', '程序出错\n')
            showerror(title="错误",
                      message="1.检擦浏览器驱动\n2.参数错误")



root = tk.Tk()
root.resizable(width=False, height=False)


root.geometry(f'{w}x{h}+%d+%d' % ((W - w) / 2, (H - h) / 2))  # 窗口的大小
root.iconbitmap('img/ico.ico')
root.title('樱花采集器')

app = App(master=root)
root.mainloop()
