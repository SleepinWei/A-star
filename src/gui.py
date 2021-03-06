import tkinter as tk
from tkinter import Canvas, StringVar, ttk
from tkinter import W, E, S, N
from tkinter import messagebox as mb
import numpy as np
from ttkbootstrap import Style
from A_Star import *


class GUI():
    def __init__(self, window) -> None:
        self.root = window
        self.content = ttk.Frame(self.root)  # 整体看作一个 content 框
        self.root.columnconfigure(0,weight=1)
        self.root.rowconfigure(0,weight=1)
        self.content.rowconfigure(0,weight=1)
        self.content.columnconfigure(0,weight=1)

    def setSrcDstFrame(self):
        """input src and dst matrix"""
        self.srcDstFrame = tk.Frame(self.content)
        self.srcFrame = tk.LabelFrame(
            self.srcDstFrame, text="Src", padx=5, pady=5)
        self.dstFrame = tk.LabelFrame(
            self.srcDstFrame, text="Dst", padx=5, pady=5)
        self.srcEntries = []  # 9 个输入框
        self.dstEntries = []  # 9 个输入框
        self.srcArray = np.ones((3, 3), dtype=int)  # 输入数据
        self.dstArray = np.ones((3, 3), dtype=int)  # 输入数据
        self.srcString = [tk.StringVar() for i in range(9)]
        self.dstString = [tk.StringVar() for i in range(9)]
        self.infoText = " "*50  # ?占位

        self.funcChoiceString = tk.StringVar()
        self.funcChoiceString.set("Manhattan Distance")
        self.comboBoxFrame = ttk.Frame(self.srcDstFrame)

        self.funcComboBox = ttk.Combobox(self.comboBoxFrame,textvariable=self.funcChoiceString)
        self.funcComboBox["values"] = ("Manhattan Distance","Number of misplaced blocks",\
            "Euclidiean Distance","Breadth First")
        self.funcLabel = ttk.Label(self.comboBoxFrame,text="Choose Heuristic Function")

        # set default value for entries
        defaultSrc = [2, 8, 3, 1, 0, 5, 4, 7, 6]
        defaultSrc = [str(i) for i in defaultSrc]
        defaultDst = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        defaultDst = [str(i) for i in defaultDst]
        for i in range(9):
            self.srcString[i].set(defaultSrc[i])
            self.dstString[i].set(defaultDst[i])

        for i in range(9):
            self.srcEntries.append(
                ttk.Entry(self.srcFrame,
                          textvariable=self.srcString[i], width=3)
            )
            self.dstEntries.append(
                ttk.Entry(self.dstFrame,
                          textvariable=self.dstString[i], width=3)
            )

        def checkValid(tensor: np.ndarray):
            # return True
            cnt = [0 for i in range(9)]
            flatTensor = tensor.flatten()
            for i in flatTensor:
                if cnt[int(flatTensor[int(i)])] == 0:
                    cnt[int(flatTensor[int(i)])] += 1
                else:
                    return False
            return True

        def confirmSrcDst():
            pos = [(i, j) for i in range(3) for j in range(3)]
            for i in range(9):
                self.srcArray[pos[i][0], pos[i][1]] = int(
                    self.srcString[i].get() if self.srcString[i].get() != "" else -1)
                self.dstArray[pos[i][0], pos[i][1]] = int(
                    self.dstString[i].get() if self.srcString[i].get() != "" else -1)

            if checkValid(self.srcArray) and checkValid(self.dstArray):
                self.runAStar()
                self.drawSearchTree()
            else:
                # messagebox show error
                mb.showwarning(title="warning", message="输入数字应该在 0-8 之间")

        self.confirm = ttk.Button(
            self.srcDstFrame, text="Confirm", command=confirmSrcDst)

        # layout
        self.srcDstFrame.grid(column=0, row=2, sticky="wens")
        self.srcFrame.grid(column=0, row=0, padx=10, pady=5)
        self.dstFrame.grid(column=1, row=0, padx=10, pady=5)
        # pos = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        pos = [(i, j) for i in range(3) for j in range(3)]
        for i in range(9):
            self.srcEntries[i].grid(
                column=pos[i][1], row=pos[i][0], padx=1, pady=2)
            self.dstEntries[i].grid(
                column=pos[i][1], row=pos[i][0], padx=1, pady=2)
        self.confirm.grid(row=0, column=3, padx=10, pady=2, sticky="nsew")
        self.comboBoxFrame.grid(row=0, column=2, sticky="nsew")
        self.funcLabel.grid(row=0, column=0, sticky="wn", pady=[15, 5])
        self.funcComboBox.grid(row=1, column=0, sticky="wn")

    def runAStar(self):

        self.a = A_Star(Node(self.srcArray.tolist()),
                        Node(self.dstArray.tolist()))

        # a = A_Star(Node([[2, 8, 3], [1, 0, 5], [4, 7, 6]]), Node(
        #     [[1, 2, 3], [4, 5, 6], [7, 8, 0]]))
        funcChoice = self.funcChoiceString.get()
        func = None
        if funcChoice == "Manhattan Distance":
            func = setH1
        elif funcChoice == "Number of misplaced blocks":
            func = setH2
        elif funcChoice == "Euclidiean Distance":
            func = setH3
        elif funcChoice == "Breadth First":
            func = breadthFirstHeuristic

        if self.a.start(func):
            infoText = ""
            infoText += "Number of expanded nodes: " + str(self.a.step) + "\n"
            infoText += "Number of generated nodes: " + \
                str(self.a.generate) + "\n"
            infoText += "Time cost: " + str(self.a.getTime()) + " ms\n"
            infoText += "Function Choice: " + funcChoice + "\n"
            self.infoText.set(infoText)
            # self.infoText += "Path: \n" + str(a.getPathString())
            self.infoTexts = [Matrix2String(n.matrix)
                              for n in self.a.pathlist[::-1]]
            self.matrices.set(self.infoTexts)
            self.listBox.delete("0.0", "end")
            for string in self.infoTexts:
                self.listBox.insert("end", string + "\n")
            # self.listBox = tk.Listbox(self.infoFrame,height=10,listvariable=self.matrices)
        else:
            self.infoText.set("No path found")


    def drawSearchTree(self):
        startNode = self.a.startNode
        self.i = 0
        self.canvas.delete("all")

        def drawNode(node: Node):
            # 画当前节点与连接线
            self.gap = 25 
            self.offset = 20 
            self.canvas.create_text(node.x * self.gap + self.offset,node.y*self.gap+self.offset,\
                text="%.1f"%(node.g + node.h),\
                tags=("node"))

            if node.father:
                if node in self.a.pathlist:
                    color = "green"
                else:
                    color = "black" 
                self.canvas.create_line(node.x * self.gap+self.offset,node.y*self.gap+self.offset,node.father.x*self.gap+self.offset,\
                    node.father.y * self.gap+self.offset,\
                    tags=("line"),fill=color)
                
        def iterSearch(node: Node, depth):
            childLen = len(node.children)
            if childLen == 0:
                node.x = self.i
                node.y = depth
                self.i += 1

            elif childLen == 1:
                iterSearch(node.children[0], depth+1)
                self.i = node.children[0].x
                node.x = self.i
                node.y = depth
                self.i += 1

            elif childLen == 2:
                iterSearch(node.children[0], depth+1)
                node.x = self.i
                node.y = depth
                self.i += 1
                iterSearch(node.children[1], depth+1)

            elif childLen == 3:
                iterSearch(node.children[0], depth+1)
                iterSearch(node.children[1], depth+1)
                self.i = node.children[1].x
                node.x = self.i
                node.y = depth
                self.i += 1

                iterSearch(node.children[2], depth+1)

            elif childLen == 4:
                iterSearch(node.children[0], depth+1)
                iterSearch(node.children[1], depth+1)
                node.x = self.i
                node.y = depth
                self.i += 1

                iterSearch(node.children[2], depth+1)
                iterSearch(node.children[3], depth+1)

        def iterDraw(node: Node):
            if node == None:
                return
            for child in node.children:
                iterDraw(child)
            drawNode(node)

        iterSearch(startNode, 0)
        iterDraw(startNode)

        # event bindings
        def searchNode(startNode, x, y):
            if startNode.x == x and startNode.y == y:
                return startNode
            for child in startNode.children:
                node = searchNode(child, x, y)
                if node:
                    return node
            return None

        def on_click(e):
            self.nodeText.delete("0.0","end")
            x = (e.x - self.offset)//self.gap
            y = (e.y - self.offset)//self.gap
            targetNode = searchNode(self.a.startNode,x,y) 

            if targetNode:
                matrixString = Matrix2String(targetNode.matrix)
                self.nodeText.insert("0.0", matrixString)

        def on_enter(e):
            self.canvas.config(cursor="hand2")

        def on_leave(e):
            self.canvas.config(cursor="")

        nodes = self.canvas.find_withtag("node")
        for node in nodes:
            self.canvas.tag_bind(node, "<Enter>", on_enter)
            self.canvas.tag_bind(node, "<Leave>", on_leave)
        self.canvas.bind("<1>", on_click)

    def setInfoFrame(self):
        self.infoFrame = ttk.LabelFrame(self.content, text="Infos")
        self.textFrame = tk.LabelFrame(self.infoFrame, text="Path")
        self.infoText = StringVar()
        self.label = ttk.Label(
            self.infoFrame, textvariable=self.infoText, state="readonly")
        self.infoTexts = []
        self.matrices = tk.StringVar(value=self.infoTexts)
        self.infoScroll = ttk.Scrollbar(self.textFrame, orient=tk.VERTICAL)
        self.listBox = tk.Text(self.textFrame, width=7,
                               yscrollcommand=self.infoScroll.set)
        self.infoScroll["command"] = self.listBox.yview
        self.nodeTextFrame = ttk.Frame(self.infoFrame)
        self.nodeLabel = ttk.Label(
            self.nodeTextFrame, text="Current Node", state="readonly")
        self.nodeText = tk.Text(self.nodeTextFrame, width=7, height=7)

        # layout
        self.infoFrame.grid(column=2, row=0, rowspan=4,
                            columnspan=2, sticky="nsew", padx=5, pady=10)
        self.textFrame.grid(column=0, row=1, rowspan=2, sticky="wnes")
        self.label.grid(column=0, row=0)
        self.listBox.grid(column=0, row=1, sticky="wns")
        self.infoScroll.grid(column=1, row=1, sticky="wns")
        self.nodeTextFrame.grid(
            column=0, row=4, columnspan=2, sticky="news", padx=5, pady=5)
        self.nodeLabel.grid(column=0, row=0, sticky="w")
        self.nodeText.grid(column=0, row=1, sticky="w")

    def setWindow(self):
        """settings for window"""
        # size
        # self.root["width"] = 600
        # self.root["height"] = 600

        # layout
        self.content.grid(column=0, row=0, sticky=[N, S, E, W])

    def setCanvas(self):
        """settings for canvas"""
        self.canvas = tk.Canvas(self.content)
        self.h = ttk.Scrollbar(self.content, orient=tk.HORIZONTAL)
        self.v = ttk.Scrollbar(self.content, orient=tk.VERTICAL)

        # size
        self.canvas["width"] = 1000
        self.canvas["height"] = 600
        self.canvas["scrollregion"] = (0, 0, 2000, 2000)
        self.canvas.configure(background="LightCyan")

        # commands
        self.h["command"] = self.canvas.xview
        self.v["command"] = self.canvas.yview

        self.canvas["xscrollcommand"] = self.h.set
        self.canvas["yscrollcommand"] = self.v.set

        # layout
        self.canvas.grid(column=0, row=0, sticky=[N, S, E, W])
        self.h.grid(column=0, row=1, sticky=(W, E))
        self.v.grid(column=1, row=0, sticky="ns")

    def run(self):
        self.setWindow()
        self.setCanvas()
        self.setSrcDstFrame()
        self.setInfoFrame()
        # self.runAStar()
        self.root.mainloop()


if __name__ == "__main__":
    # window = tk.Tk()
    style = Style(theme="flatly")
    window = style.master
    window.title("A-star")
    gui = GUI(window)
    gui.run()
