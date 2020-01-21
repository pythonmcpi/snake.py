import tkinter
import math

# Tkinter Functions based off of:
# https://www.tutorialspoint.com/python/tk_canvas.htm
# http://www.kosbie.net/cmu/spring-15/15-112/notes/notes-graphics.html

class Engine:
    def __init__(self):
        pass

class Screen:
    def __init__(self,size,pos,title):
        self.windowSizeX = size[0]
        self.windowSizeY = size[1]
        self.windowPosX = pos[0]
        self.windowPosY = pos[1]
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root.geometry(str(self.windowSizeX)+"x"+str(self.windowSizeY)+"+"+str(self.windowPosX)+"+"+str(self.windowPosY))
        self.canvas = tkinter.Canvas(self.root,bd=5,height=self.windowSizeY,width=self.windowSizeX)
        self.canvas.pack()
    def RGB2Hex(self,rgb):
        return "#%02x%02x%02x" % rgb
    def Hex2RGB(self,hexColor):
        return int(hexColor,base=16)
    def fillbg(self,color):
        colorHex = self.RGB2Hex(color)
        self.canvas.create_rectangle(0,0,self.windowSizeX,self.windowSizeY, fill=colorHex)
    def drawrect(self,pos,size,color):
        colorHex = self.RGB2Hex(color)
        posX = pos[0]
        posY = pos[1]
        sizeX = size[0]
        sizeY = size[1]
        self.canvas.create_rectangle(posX,posY,sizeX,sizeY,fill=colorHex)
    def drawline(self,pos1,pos2,color,width=1): # https://kite.com/python/docs/tkinter.Canvas.create_line
        colorHex = self.RGB2Hex(color)
        pos1x = pos1[0]
        pos1y = pos1[1]
        pos2x = pos2[0]
        pos2y = pos2[1]
        self.canvas.create_line(pos1x,pos1y,pos2x,pos2y,fill=colorHex,width=width)
    def write(self,text,pos,color,font=("Arial",12,False,False,False)): # https://stackoverflow.com/questions/17736967/python-how-to-add-text-inside-a-canvas
        colorHex = self.RGB2Hex(color)
        posX = pos[0]
        posY = pos[1]
        fontString = font[0] + " " + str(font[1])
        if font[2]: # Bold
            fontString += " bold"
        if font[3]: # Italics
            fontString += " italic"
        if font[4]: # Underline
            fontString += " underline"
        self.canvas.create_text(posX,posY,text=text,fill=colorHex,font=fontString)
    def bindkey(self,key,function):
        return self.root.bind(key,function)
    def unbindkey(self,bindId):
        self.root.unbind(bindId)
    def mainloop(self):
        self.root.mainloop()
