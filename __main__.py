#    <one line to give the program's name and a brief idea of what it does.>
#    Copyright (C) <year>  <name of author>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import tkinter
import argparse
from tkinter import ttk 
from subprocess import Popen, PIPE
from os import path, system, getcwd, chdir

parser = argparse.ArgumentParser()
parser.add_argument("--filepath")
args = parser.parse_args()

DEFWD = getcwd()
DEFAULT = "draw"
BIPARTITE = "draw_bipartite"
CIRCULAR = "draw_circular"
KAMADAKAWAI = "draw_kamada_kawai"
PLANAR = "draw_planar"
RANDOM = "draw_random"
SPECTRAL = "draw_spectral"
SPRING = "draw_spring"
SHELL = "draw_shell"

fileFrame = f"""import networkx
import matplotlib.pyplot as plt

graph = networkx.Graph()
networkx.draw(graph, with_labels=True)
plt.savefig("output.png", format="PNG")"""

if args.filepath == None:
    if not path.exists("file.py"):
        f = open("file.py", "w")
        f.writelines(fileFrame)
        f.close()
        
    filename = "file.py"
    if not path.exists("output.png"):
        system("python file.py")
        if not path.exists("output.png"):
            print("please save graph as PNG at the end of the file with pyplot.savefig() function")
            exit(1)
else:
    if not path.exists(fr"{args.filepath}\file.py"):
        f = open(fr"{args.filepath}\file.py", "w")
        f.writelines(fileFrame)
        f.close()
    filename = fr"{args.filepath}\file.py"
    if not path.exists(fr"{args.filepath}\output.png"):
        wpath = getcwd()
        chdir(args.filepath)
        system(fr"python {args.filepath}\file.py")
        if not path.exists(fr"{args.filepath}\output.png"):
            print("please save graph as PNG at the end of the file with pyplot.savefig() function")
            exit(1)

def changeDir(originalWD: bool):
    if originalWD:
        chdir(DEFWD)
    if not originalWD:
        if args.filepath != None:
            chdir(args.filepath)

def changeDraw(type: str):
    data = readfile(filename)
    exceptations = ["draw", 
                    "draw_bipartite",
                    "draw_circular",
                    "draw_kamada_kawai",
                    "draw_planar",
                    "draw_random",
                    "draw_spectral",
                    "draw_spring",
                    "draw_shell"]
    for i in range(len(data)):
        currentLine = data[i]
        for b in exceptations:
            if b in currentLine:
                data[i] = f"networkx.{type}({graphname}, with_labels=True)\n"
    writefile(data)

class drawType:
    def defaultG():
        changeDraw(DEFAULT)
    def bipartiteG():
        changeDraw(BIPARTITE)
    def circularG():
        changeDraw(CIRCULAR)
    def kamadaKawaiG():
        changeDraw(KAMADAKAWAI)
    def planarG():
        changeDraw(PLANAR)
    def randomG():
        changeDraw(RANDOM)
    def spectralG():
        changeDraw(SPECTRAL)
    def springG():
        changeDraw(SPRING)
    def shellG():
        changeDraw(SHELL)

def removeLines(data: list) -> list:
    l = []
    for i in data:
        if "draw" in i or "savefig" in i:
            pass
        else:
            l.append(i)
    return l

def readfile(filename) -> list:
    f = open(filename, "r")
    data = f.readlines()
    f.close()
    return data

def writefile(data):
    f = open(filename, "w")
    f.writelines(data)
    f.close()

def findGraphName() -> str:
    data = readfile(filename)
    graphLine = ""
    for i in data:
        if ".Graph()" in i:
            graphLine = i
    return graphLine.split("=")[0].strip()

graphname = findGraphName()

def refreshImage():
    if args.filepath == None:
        system("python file.py")
    elif args.filepath != None or args.filepath != "":
        system(fr"python {args.filepath}\file.py")
    global openedImage
    if args.filepath == None:
        openedImage = tkinter.PhotoImage(file="output.png")
    elif args.filepath != None or args.filepath != "":
        openedImage = tkinter.PhotoImage(file=fr"{args.filepath}\output.png")
    graphLabel.config(image=openedImage)

def addNode():
    newWindow = tkinter.Toplevel(master)
    newWindow.title("Add New Node")
    newWindow.geometry("250x100")
    changeDir(True)
    plus = tkinter.PhotoImage(file="quickGraphEditor/plus.png")
    changeDir(False)
    newWindow.iconphoto(False, plus)

    entry = tkinter.Entry(newWindow)
    entry.pack()

    def file_addNode():
        data = readfile(filename)
        data.insert(len(data)-2, f"{graphname}.add_node(\"{entry.get()}\")\n")
        writefile(data=data)

    AddButton = ttk.Button(newWindow, text="Add Node", command=file_addNode)
    AddButton.pack()

def killNode():
    newWindow = tkinter.Toplevel(master)
    newWindow.title("Kill Node")
    newWindow.geometry("250x100")
    changeDir(True)
    minus = tkinter.PhotoImage(file="quickGraphEditor/minus.png")
    changeDir(False)
    newWindow.iconphoto(False, minus)

    entry = tkinter.Entry(newWindow)
    entry.pack()

    def file_killNode():
        if entry.get() == "":
            newWindow.destroy()
        data = readfile(filename)
        for i in data:
            if "add_node" in i and entry.get() in i:
                data.remove(i)
        writefile(data=data)
        
    WarningLabel = ttk.Label(newWindow, text="Remember to kill the edges of the node " \
    "you\n are killing to make it disappear.")
    WarningLabel.pack()

    killButton = ttk.Button(newWindow, text="Kill Node", command=file_killNode)
    killButton.pack()

def addEdge():
    newWindow = tkinter.Toplevel(master)
    newWindow.title("Add New Edge")
    newWindow.geometry("250x100")
    changeDir(True)
    plus = tkinter.PhotoImage(file="quickGraphEditor/plus.png")
    changeDir(False)
    newWindow.iconphoto(False, plus)
    
    edge1 = tkinter.Entry(newWindow)
    edge1.pack()

    edge2 = tkinter.Entry(newWindow)
    edge2.pack()

    def file_addEdge():
        data = readfile(filename)
        data.insert(len(data)-2, f"{graphname}.add_edge(\"{edge1.get()}\", \"{edge2.get()}\")\n")
        writefile(data)

    AddButton = ttk.Button(newWindow, text="Add Edge", command=file_addEdge)
    AddButton.pack()

def killEdge():
    newWindow = tkinter.Toplevel(master)
    newWindow.title("Kill Edge")
    newWindow.geometry("250x100")
    changeDir(True)
    minus = tkinter.PhotoImage(file="quickGraphEditor/minus.png")
    changeDir(False)
    newWindow.iconphoto(False, minus)

    edge1 = tkinter.Entry(newWindow)
    edge1.pack()

    edge2 = tkinter.Entry(newWindow)
    edge2.pack()

    def file_killEdge():
        data = readfile(filename)
        for i in data:
            if edge1.get() in i and edge2.get() in i and "add_edge" in i:
                data.remove(i)
        writefile(data)

    killButton = ttk.Button(newWindow, text="Kill Edge", command=file_killEdge)
    killButton.pack()

def printDiameter():
    code = readfile(filename)
    data = readfile(filename)
    data = removeLines(data)
    data.insert(len(data), f"print(networkx.diameter({graphname}))")
    writefile(data)
    diameter = Popen(["python", f"{filename}"], stdout=PIPE)
    output.config(text=f"Diameter Output: {diameter.stdout.readline().decode("utf-8").strip()}")
    writefile(code)

def printDegree():
    newWindow = tkinter.Toplevel(master=master)
    newWindow.title("Print The Degree of A Node")
    newWindow.geometry("300x100")
    changeDir(True)
    printer = tkinter.PhotoImage(file="quickGraphEditor/printer.png")
    changeDir(False)
    newWindow.iconphoto(False, printer)

    nodeName = tkinter.Entry(newWindow)
    nodeName.pack()

    def count():
        counter = 0
        data = readfile(filename)
        for i in data:
            if "add_edge" in i and nodeName.get() in i:
                counter += 1
        output.config(text=f"Degree: {counter}")
    
    calculateDegreeButton = ttk.Button(newWindow, text="Calculate Degree", command=count)
    calculateDegreeButton.pack()

    output = tkinter.Label(newWindow, text="Degree: ", bg="gray60")
    output.pack()

def changeDrawStyle():
    newWindow = tkinter.Toplevel(master=master)
    newWindow.title("Change Draw Layout")
    newWindow.geometry("260x100")
    newWindow.resizable(False, False)
    
    default = ttk.Button(newWindow, text="Default", width=20, command=drawType.defaultG)
    default.grid(column=0, row=0)
    bipartite = ttk.Button(newWindow, text="Bipartite", width=20, command=drawType.bipartiteG)
    bipartite.grid(column=0, row=1)
    circular = ttk.Button(newWindow, text="Circular", width=20, command=drawType.circularG)
    circular.grid(column=0, row=2)
    kamadaKawai = ttk.Button(newWindow, text="KamadaKawai", width=20, command=drawType.kamadaKawaiG)
    kamadaKawai.grid(column=0, row=3)
    planar = ttk.Button(newWindow, text="Planar", width=20, command=drawType.planarG)
    planar.grid(column=1, row=0)
    random = ttk.Button(newWindow, text="Random", width=20, command=drawType.randomG)
    random.grid(column=1, row=1)
    spectral = ttk.Button(newWindow, text="Spectral", width=20, command=drawType.spectralG)
    spectral.grid(column=1, row=2)
    spring = ttk.Button(newWindow, text="Spring", width=20, command=drawType.springG)
    spring.grid(column=1, row=3)

master = tkinter.Tk()
master.title("Networkx Quick Graphic Editor")
master.geometry("780x485")
master.resizable(False, False)
changeDir(True)
pepe = tkinter.PhotoImage(file="quickGraphEditor/pepe.png")
changeDir(False)
master.iconphoto(False, pepe)

#Graph LEFTSIDE
GraphFrame = tkinter.Frame(master, bg="SlateGray4")
GraphFrame.pack(side="left")

if args.filepath == None:
    photo = tkinter.PhotoImage(file="output.png")
elif args.filepath != None or args.filepath != "":
    photo = tkinter.PhotoImage(file=fr"{args.filepath}\output.png")
graphLabel = ttk.Label(GraphFrame, image=photo)
graphLabel.pack(expand=True, padx=2, pady=2)

#Buttons RIGHTSIDE
rightFrame = tkinter.Frame(master, width=15, height=10)
rightFrame.pack(expand=True)

refreshButton = ttk.Button(rightFrame, text="Refresh", width=17, command=refreshImage)
refreshButton.pack(expand=True, padx=5, pady=5)

addNodeButton = ttk.Button(rightFrame, text="Add Node", width=17, command=addNode)
addNodeButton.pack(expand=True, padx=5, pady=5)

killNodeButton = ttk.Button(rightFrame, text="Kill Node", width=17, command=killNode)
killNodeButton.pack(expand=True, padx=5, pady=5)

addEdgeButton = ttk.Button(rightFrame, text="Add Edge", width=17, command=addEdge)
addEdgeButton.pack(expand=True, padx=5, pady=5)

killEdgeButton = ttk.Button(rightFrame, text="Kill Edge", width=17, command=killEdge)
killEdgeButton.pack(expand=True, padx=5, pady=5)

printGraphDiameterButton = ttk.Button(rightFrame, text="Print Diameter", width=17, command=printDiameter)
printGraphDiameterButton.pack(expand=True, padx=5, pady=5)

printNodeDegreeButton = ttk.Button(rightFrame, text="Print Node Degree", width=17, command=printDegree)
printNodeDegreeButton.pack(expand=True, padx=5, pady=5)

changeGraphButton = ttk.Button(rightFrame, text="Change Draw Layout", width=17, command=changeDrawStyle)
changeGraphButton.pack(expand=True, padx=5, pady=5)

#Console BOTTOMSIDE
bottomFrame = ttk.Frame(master)
bottomFrame.pack(side="bottom")

output = tkinter.Label(bottomFrame, text="Diameter Output:", bg="gray60")
output.pack(fill="x")

master.mainloop()