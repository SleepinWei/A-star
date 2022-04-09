import tkinter as tk 
from tkinter import ttk
from tkinter import W,E,S,N
from tkinter import messagebox as mb
import numpy as np

class GUI():
    def __init__(self,window) -> None:
        self.root = window 
        self.content = ttk.Frame(self.root) # 整体看作一个 content 框

    def setSrcDstFrame(self):
        """input src and dst matrix"""
        self.srcDstFrame = tk.Frame(self.content)
        self.srcFrame = tk.LabelFrame(self.srcDstFrame,text="Src",padx=5,pady=5)
        self.dstFrame = tk.LabelFrame(self.srcDstFrame,text="Dst",padx=5,pady=5)
        self.srcEntries = [] # 9 个输入框
        self.dstEntries = [] # 9 个输入框
        self.srcArray = np.ones((3,3)) # 输入数据
        self.dstArray = np.ones((3,3)) # 输入数据
        self.srcString = [tk.StringVar() for i in range(9)] 
        self.dstString = [tk.StringVar() for i in range(9)]

        for i in range(9):
            self.srcEntries.append(
                ttk.Entry(self.srcFrame,textvariable=self.srcString[i],width=3)
            )
            self.dstEntries.append(
                ttk.Entry(self.dstFrame,textvariable=self.dstString[i],width=3)
            )
        
        def checkValid(tensor:np.ndarray):
            cnt = [0 for i in range(9)]
            flatTensor = tensor.flatten()
            for i in flatTensor: 
                if flatTensor[int(i)] == 0:
                    cnt[int(flatTensor[int(i)])] +=1 
                else: 
                    return False
            return True
            
        def confirmSrcDst():
            pos = [(i,j) for i in range(3) for j in range(3)]
            for i in range(9):
                self.srcArray[pos[i][0],pos[i][1]] = int(self.srcString[i].get() if self.srcString[i].get()!="" else -1)
                self.dstArray[pos[i][0],pos[i][1]] = int(self.dstString[i].get() if self.srcString[i].get()!="" else -1)

            if checkValid(self.srcArray) and checkValid(self.dstArray):
                pass
            else:
                # messagebox show error 
                mb.showwarning(title="warning",message="输入数字应该在 0-8 之间")
                pass
            
        self.confirm = ttk.Button(self.srcDstFrame,text="Confirm",command=confirmSrcDst)

        # layout 
        self.srcDstFrame.grid(column=0,row=2,sticky="wens")
        self.srcFrame.grid(column=0,row=0,padx=10,pady=5)        
        self.dstFrame.grid(column=1,row=0,padx=10,pady=5)
        # pos = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        pos = [(i,j) for i in range(3) for j in range(3)]
        for i in range(9):
            self.srcEntries[i].grid(column=pos[i][1],row=pos[i][0],padx=1,pady=2)
            self.dstEntries[i].grid(column=pos[i][1],row=pos[i][0],padx=1,pady=2)
        self.confirm.grid(row=1,column=0,padx=5,pady=5)

    def setInfoFrame(self):
        self.infoFrame = tk.LabelFrame(self.content,text="Infos",width=300)
        self.label = ttk.Label(self.infoFrame,text="INFO")

        # layout
        self.infoFrame.grid(column=2,row=0,rowspan=2,columnspan=2,sticky="nsew")
        self.label.grid(column=0,row=0)

    def setWindow(self):
        """settings for window"""
        # size
        # self.root["width"] = 600
        # self.root["height"] = 600

        # layout
        self.content.grid(column=0,row=0,sticky=[N,S,E,W])
    
    def setCanvas(self):
        """settings for canvas"""
        self.canvas = tk.Canvas(self.content)
        self.h = ttk.Scrollbar(self.content,orient=tk.HORIZONTAL)

        # size
        self.canvas["width"] = 400
        self.canvas["height"] = 400
        self.canvas["scrollregion"]=(0,0,1000,1000)
        self.canvas.configure(background="LightCyan")

        # commands
        self.h["command"] = self.canvas.xview
        self.canvas["xscrollcommand"] = self.h.set
        # self.canvas.create_rectangle((10,10,30,30),fill="LightCyan")
        self.canvas.create_line(10,10,200,50)

        # layout
        self.canvas.grid(column=0,row=0,sticky=[N,S,E,W])
        self.h.grid(column=0,row=1,sticky=(W,E))

    def run(self):
        self.setWindow()
        self.setCanvas()
        self.setSrcDstFrame() 
        self.setInfoFrame()
        self.root.mainloop()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("A-star")
    gui = GUI(window)
    gui.run()
