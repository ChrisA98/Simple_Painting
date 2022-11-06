# -*- coding: utf-8 -*-
"""
Christopher Adkins
CSC 550
Final Exam - drawing program prototype
"""
import pygame, sys
import os
from pygame.locals import *
import pygame.gfxdraw
import tkinter as tk
from tkinter import filedialog
import math
import random
import numpy as np

pygame.init()
print("Program Initializing")

      
class shape():
    #<<Math References>>
    #bezier matrices
    quad_matrix = [[1,-2,1],
               [-2,2,0],
               [1,0,0]]
    cubic_matrix = [[-1,3,-3,1],
               [3,-6,3,0],
               [-3,3,0,0],
               [1,0,0,0]]
    quart_mat = [[1,-4,6,-4,1],
                 [-4,12,-12,4,0],
                 [6,-12,6,0,0],
                 [-4,4,0,0,0],
                 [1,0,0,0,0]]  
    bez_mats = [quad_matrix,cubic_matrix,quart_mat]
    
    
    def __init__(self, shape_, lineWidth, color_):
        self.shape = shape_
        self.size = lineWidth
        self.color = color_
        self.points = []
        if (self.shape =="Pixel Draw"):
            self.pointLim = 10000
        elif (self.shape =="Line"):
            self.pointLim = 2
        elif (self.shape =="Bez Line"):
            self.pointLim = 5
        elif (self.shape =="Triangle"):
            self.pointLim = 3
        elif (self.shape =="Rectangle"):
            self.pointLim = 2
        elif (self.shape =="Fill Rect."):
            self.pointLim = 2
        elif (self.shape =="Ellipse"):
            self.pointLim = 3
        else:
            self.pointLim = 2
        
        
    def addPoint(self, point_, index = -1):  
        if (index == -1):
            index = len(self.points)
        if(index != len(self.points)):
            self.nPoint = pygame.Vector2()
            self.nPoint.xy = point_[0], point_[1]
            self.points[index] = self.nPoint           
        elif (len(self.points)+1 <= self.pointLim):
            self.nPoint = pygame.Vector2()
            self.nPoint.xy = point_[0], point_[1]
            self.points.append(self.nPoint)
        else:
            self.nPoint = pygame.Vector2()
            self.nPoint.xy = point_[0], point_[1]
            self.points[-1] = self.nPoint
        if(self.shape =="Pixel Draw" and len(self.points)>1):
            self.fillSpace(self.points[index],index)
    def fillSpace(self, point, index):
        dis = abs(self.points[index].distance_to(self.points[index-1]))
        if(dis>0.05):
            self.points.insert(index-1, self.points[index-1].lerp(self.points[index], .6))
            self.fillSpace(self.points[index],index)
        else:
            return
            
class button():
    def __init__(self, origin_, name_):
        self.name = name_
        self.scaleX = 25
        self.scaleY = 25
        self.origin = pygame.Vector2()
        self.origin.xy = origin_[0],origin_[1]
        self.color = Colors.black
        self.active = False
        self.off_color = Colors.dark_grey
        self.on_color = Colors.off_black
        self.off_l_color = Colors.off_black
        self.on_l_color = Colors.white
        self.pixels = ([])
        for i in range(25):
            self.pixels.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        
    def design_button(self, pixels):
        #define button design
        self.pixels = pixels
        
    def draw_button(self, act_tool):
        #draw backing of button
        frame_point(self.origin.x-13, self.origin.y-13, 27, 27, Colors.grey)
        if(act_tool == self.name):     
            frame_point(self.origin.x-13, self.origin.y-13, 27, 27, self.on_l_color)       
            frame_point(self.origin.x-12, self.origin.y-12, 25, 25, self.on_color)
        else:
            frame_point(self.origin.x-13, self.origin.y-13, 27, 27, self.off_l_color )
            frame_point(self.origin.x-12, self.origin.y-12, 25, 25, self.off_color)
        #draw button icon
        for i in range(25):
            for j in range(25):
                if (self.pixels[i][j] == 1):
                    frame_point(self.origin.x-12+j, self.origin.y-12+i, 1, 1, Colors.grey)
                    
    def set_colors(self, off_color, on_color, on_l_color, off_l_color=(20,20,20)):
        self.off_color = off_color
        self.on_color = on_color
        self.off_l_color = off_l_color
        self.on_l_color = on_l_color
    def setPosition(self,pos):
        self.origin = pygame.Vector2()
        self.origin.xy = pos[0],pos[1]
        
    def import_design(self,filename):
        for i, line in enumerate(open("Icons"+ "\\" + filename + ".xpm")):
            if(i < 5):
                continue
            for j, ch in enumerate(line):
                if(ch == '.'):
                    self.pixels[i-5][j-1] = 1
                
class slider():
    
    def __init__(self, top_, height_, val):
        self.top = pygame.Vector2()
        self.top.xy = top_[0], top_[1]
        self.height = height_
        self.value = val
    
    def draw_slider(self):
        frame_point(self.top.x-1,self.top.y,6,self.height,Colors.grey)
        frame_point(self.top.x,self.top.y,4,self.height,Colors.off_black)
        sliderSpot = pygame.Vector2()
        sliderSpot.y = self.top.y+self.height-(self.height*self.value)-5
        sliderSpot.x = self.top.x-3
        frame_point(sliderSpot.x,sliderSpot.y,11,11,Colors.grey)
        frame_point(sliderSpot.x+2,sliderSpot.y+2,7,7,Colors.white)
        self.center = pygame.Vector2()
        self.center.xy = sliderSpot.x+5, sliderSpot.y+5
        self.color = round(self.value * 255)
        
class sliderHorizontal():
    
    def __init__(self, left_, width_, val):
        self.left = pygame.Vector2()
        self.left.xy = left_[0], left_[1]
        self.width = width_
        self.value = val
    
    def draw_slider(self):
        frame_point(self.left.x, self.left.y-1,self.width,5,Colors.grey)
        frame_point(self.left.x, self.left.y, self.width,3,Colors.off_black)
        sliderSpot = pygame.Vector2()
        sliderSpot.y = self.left.y-4
        sliderSpot.x = self.left.x+(self.width*self.value)-4
        frame_point(sliderSpot.x,sliderSpot.y,11,11,Colors.grey)
        frame_point(sliderSpot.x+2,sliderSpot.y+2,7,7,Colors.white)
        self.center = pygame.Vector2()
        self.center.xy = sliderSpot.x+5, sliderSpot.y+5
        if (self.value < 0.01):
            self.value=0.01

class frame():
    
    def _init_(self):
        self=self
    def clean_array(self):
        self.points = ([])
        for i in range(25):
            self.points.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    def draw_button_points(mat, xs, xe, ys, ye):
        for i in range(xs,xe):
            for j in range(ys,ye):
                mat[j][i] = 1
    
    def erase_button_points(mat, xs, xe, ys, ye):
        for i in range(xs,xe):
            for j in range(ys,ye):
                mat[j][i] = 0
    
    def construct_frame(self):
        self.actTool = "None"
        self.all_buttons = []
        
        #line tool  
        self.line_button = button((30,40),"Line")
        self.line_button.import_design("Line")
        self.all_buttons.append(self.line_button)
        
        #bezier  tool                
        self.bez_button = button((60,40),"Bez Line")
        self.bez_button.import_design("Bezier")
        self.all_buttons.append(self.bez_button)    
           
        #Pixel tool        
        self.pix_button = button((90,40),"Pixel Draw")
        self.pix_button.import_design("Pixel")
        self.all_buttons.append(self.pix_button)   
        
        #triangle tool
        self.tri_button = button((120,40),"Triangle")
        self.tri_button.import_design("Triangle")
        self.all_buttons.append(self.tri_button)     
        
        #rect tool
        self.pix_button = button((30,70),"Rectangle")
        self.pix_button.import_design("Rect")
        self.all_buttons.append(self.pix_button)
        
        #filled rect tool        
        self.pix_button = button((60,70),"Fill Rect.")
        self.pix_button.import_design("Filledrect")
        self.all_buttons.append(self.pix_button)
        
        #Ellipse tool
        self.cir_button = button((90,70),"Ellipse")
        self.cir_button.import_design("Ellipse")
        self.all_buttons.append(self.cir_button)
        
        #fill tool    
        self.pix_button = button((120,70),"Fill Back")
        self.pix_button.import_design("Fill")
        self.all_buttons.append(self.pix_button) 
        
        #save button tool
        self.pix_button = button((30,100),"Saving")
        self.pix_button.import_design("Save")
        self.all_buttons.append(self.pix_button) 
        
        
        #Load button tool        
        self.pix_button = button((60,100),"Load")
        self.pix_button.import_design("Load")
        self.all_buttons.append(self.pix_button) 
        
        #Export button tool
        self.pix_button = button((90,100),"Exporting")
        self.pix_button.import_design("Export")
        self.all_buttons.append(self.pix_button) 
        
        #import button tool
        self.pix_button = button((120,100),"Importing")
        self.pix_button.import_design("Import")
        self.all_buttons.append(self.pix_button) 
        
        #layer down
        self.pix_button = button((1368,557),"Layer Down")
        self.pix_button.import_design("LayerDown")
        self.all_buttons.append(self.pix_button) 
        
        #layer up
        self.pix_button = button((1398,557),"Layer Up")
        self.pix_button.import_design("LayerUp")
        self.all_buttons.append(self.pix_button) 
        
        #Undo button tool
        self.pix_button = button((30,130),"Undo")
        self.pix_button.import_design("Undo")
        self.all_buttons.append(self.pix_button) 
        
        #Undo button tool
        self.pix_button = button((60,130),"Redo")
        self.pix_button.import_design("Redo")
        self.all_buttons.append(self.pix_button) 
        
        #remove layer
        self.pix_button = button((1428,557),"Rem Layer")
        self.pix_button.import_design("RemLayer")
        self.all_buttons.append(self.pix_button) 
        
        #add layer
        self.pix_button = button((1458,557),"Add Layer")
        self.pix_button.import_design("AddLayer")
        self.all_buttons.append(self.pix_button) 
        
        #confirm button
        self.clean_array()       
        
        self.add_button = button((90,130),"Added!")
        self.add_button.set_colors(Colors.green, Colors.dark_green, Colors.white)
        self.add_button.design_button(self.points)
        self.all_buttons.append(self.add_button)
        
        #cancel button
        self.clean_array()       
        
        self.rem_button = button((120,130),"Canceled!")
        self.rem_button.set_colors(Colors.red, Colors.darkRed, Colors.white)
        self.rem_button.design_button(self.points)
        self.all_buttons.append(self.rem_button) 
        
               
        #build sliders        
        self.redSlid = slider((30,350),100,0)
        self.greenSlid = slider((70,350),100,0)
        self.blueSlid = slider((110,350),100,0)
        
        self.zoomSlid = slider((65,580),100,0)        
        self.sizeSlid = sliderHorizontal((20,500), 100, 1)
        
        self.sliders =[self.redSlid, self.greenSlid, self.blueSlid, self.zoomSlid]
        
    
    def draw_frame(self):      
        global activeColor
        global is_drawing
        global layers
        global current_layer
        #frame Backdrop
        frame_point(0,0,150,720,Colors.dark_grey)
        #right frame
        frame_point(1280,0,200,720,Colors.dark_grey)
        #layer box
        frame_point(1290,40,180,500,Colors.off_black)
        
        # draw layers title
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Layers", True, Colors.black)      
        textRect = text.get_rect()
        textRect.center = (1380,21)
        gameDisplay.blit(text, textRect)
        text = font.render("Layers", True, Colors.grey)    
        textRect.center = (1380,19)
        gameDisplay.blit(text, textRect)
        
        #draw layers
        for ht, layer in enumerate(layers):
            layer.draw((ht == current_layer),(1365,55+(ht*30)))
            
        #layer box dividers
        frame_point(1292,40,2,500,Colors.off_black)
        frame_point(1290,40,2,500,Colors.dark_grey)
        frame_point(1288,40,2,500,Colors.grey)
        frame_point(1472,40,2,500,Colors.off_black)
        frame_point(1470,40,2,500,Colors.dark_grey)
        frame_point(1468,40,2,500,Colors.grey)
        self.divHeight = 540
        frame_point(1290,self.divHeight,180,1,Colors.grey)
        frame_point(1290,self.divHeight+1,180,1,Colors.dark_grey)
        frame_point(1290,self.divHeight+2,180,2,Colors.off_black)
        self.divHeight = 40
        frame_point(1290,self.divHeight,180,1,Colors.grey)
        frame_point(1290,self.divHeight+1,180,1,Colors.dark_grey)
        frame_point(1290,self.divHeight+2,180,2,Colors.off_black)      
        
        
        # draw buttons
        if (is_drawing and self.actTool != "Pixel Draw"):
            for i in range(len(self.all_buttons)):
                self.all_buttons[i].draw_button(self.actTool)
        else:
            for i in range(len(self.all_buttons)-2):
                self.all_buttons[i].draw_button(self.actTool)
            
        #divider
        self.divHeight = 150
        frame_point(0,self.divHeight,150,1,Colors.grey)
        frame_point(0,self.divHeight+1,150,1,Colors.dark_grey)
        frame_point(0,self.divHeight+2,150,2,Colors.off_black)
        
        #divider
        self.divHeight = 190
        frame_point(0,self.divHeight,150,1,Colors.grey)
        frame_point(0,self.divHeight+1,150,1,Colors.dark_grey)
        frame_point(0,self.divHeight+2,150,2,Colors.off_black)
        
        #left border
        frame_point(148,0,2,720,Colors.off_black)
        frame_point(150,0,2,720,Colors.dark_grey)
        frame_point(152,0,2,720,Colors.grey)        
        
        #right border
        frame_point(1282,0,2,720,Colors.off_black)
        frame_point(1280,0,2,720,Colors.dark_grey)
        frame_point(1278,0,2,720,Colors.grey)
        
        # draw tool title
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Tools", True, Colors.black)      
        textRect = text.get_rect()
        textRect.center = (77,17)
        gameDisplay.blit(text, textRect)
        text = font.render("Tools", True, Colors.grey)    
        textRect.center = (75,15)
        gameDisplay.blit(text, textRect)
        
        
        # draw actvive tool text
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Using: "+self.actTool, True, Colors.black) 
        textRect.center = (44,176)
        gameDisplay.blit(text, textRect)
        text = font.render("Using: "+self.actTool, True, Colors.grey) 
        textRect.center = (42,174)
        gameDisplay.blit(text, textRect)        
        
        #draw color sample
        frame_point(15,200,120,120,activeColor)
        frame_point(15,315,120,5,Colors.white)
        frame_point(132,200,5,120,Colors.off_black)
        frame_point(132,315,5,5,Colors.grey)
        
        # write actvive color value text
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render("R: "+(str)(activeColor[0])+ "  G: "+(str)(activeColor[1])+" B: "+(str)(activeColor[2]), True, Colors.black) 
        textRect.center = (27,340)
        gameDisplay.blit(text, textRect)
        text = font.render("R: "+(str)(activeColor[0])+ "  G: "+(str)(activeColor[1])+" B: "+(str)(activeColor[2]), True, Colors.grey) 
        textRect.center = (29,340)
        gameDisplay.blit(text, textRect)
        
        #draw sliders
        self.redSlid.draw_slider()
        self.greenSlid.draw_slider()
        self.blueSlid.draw_slider()  
        
        #divider 2
        self.divHeight = 460
        frame_point(0,self.divHeight,150,1,Colors.grey)
        frame_point(0,self.divHeight+1,150,1,Colors.dark_grey)
        frame_point(0,self.divHeight+2,150,2,Colors.off_black)
        
        # draw actvive line width text
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Line Size: "+(str)(activeWidth), True, Colors.black) 
        textRect.center = (44,482)
        gameDisplay.blit(text, textRect)
        text = font.render("Line Size: "+(str)(activeWidth), True, Colors.grey) 
        textRect.center = (42,480)
        gameDisplay.blit(text, textRect)
        self.sizeSlid.draw_slider()
        
        #divider 3
        self.divHeight = 530
        frame_point(0,self.divHeight,150,1,Colors.grey)
        frame_point(0,self.divHeight+1,150,1,Colors.dark_grey)
        frame_point(0,self.divHeight+2,150,2,Colors.off_black)
        
        
        self.zoomSlid.draw_slider()
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("+", True, Colors.black) 
        textRect.center = (87,566)
        gameDisplay.blit(text, textRect)
        text = font.render("-", True, Colors.black) 
        textRect.center = (90,690)
        gameDisplay.blit(text, textRect)
        
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Zoom: "+(str)(round(scale)), True, Colors.black) 
        textRect.center = (62,552)
        gameDisplay.blit(text, textRect)
        text = font.render("Zoom: "+(str)(round(scale)), True, Colors.grey) 
        textRect.center = (60,550)
        gameDisplay.blit(text, textRect)
        
        
        #draw mouse point        
        activeX = pygame.mouse.get_pos()[0]-150
        if(activeX < 0):
            activeX=0
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("X: "+(str)(activeX)+", Y: "+(str)(pygame.mouse.get_pos()[1]), True, Colors.grey) 
        textRect.center = (200,30)
        gameDisplay.blit(text, textRect)   
        
        # draw layers title
        font = pygame.font.Font('freesansbold.ttf',15)
        text = font.render("Simple Drawing v 1.0.1", True, Colors.grey)      
        textRect = text.get_rect()
        textRect.center = (1390,710)
        gameDisplay.blit(text, textRect)
        
class Colors:
    #basic colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    grey = (190, 190, 190)
    dark_grey = (75, 75, 75)
    dark_green = (0, 150, 0)
    off_black = (20, 20, 20)
    red = (255, 0, 0)
    orange = (255,117,0)
    darkRed = (155, 0, 0)
    yellow = (255,255,0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    violet = (117,0,255)    

class content_layer():
    
    def __init__(self, name):
        self.shape_list = [] #ist of shapes
        self.name = name
        
        self.all_buttons = []
        self.visible = True
        
        self.pix_button = button((-60,0),"visible")
        self.pix_button.import_design("Visible")
        self.all_buttons.append(self.pix_button)   
        
        self.pix_button = button((-60,0),"close")
        self.pix_button.import_design("NotVisible")
        self.all_buttons.append(self.pix_button)   
        
        self.position = (0,0)
    
    def draw(self, active, position):
        self.position = position
        frame_point(position[0]-75,position[1]-15,180,30,Colors.white)
        if (active):
            frame_point(position[0]-74,position[1]-14,178,28,Colors.dark_grey)
        else:            
            frame_point(position[0]-74,position[1]-14,178,28,Colors.off_black)
       
        #visibility button
        if(self.visible == True):           
            self.all_buttons[0].setPosition((position[0]-60,position[1]))
            self.all_buttons[0].draw_button("na")
        else:           
            self.all_buttons[1].setPosition((position[0]-60,position[1]))
            self.all_buttons[1].draw_button("na")
        
            
        
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render(self.name, True, Colors.black)      
        textRect = text.get_rect()
        textRect.center = (position[0]-15,position[1]+2)
        gameDisplay.blit(text, textRect)
        text = font.render(self.name, True, Colors.grey)    
        textRect.center = (position[0]-15,position[1]+2)
        gameDisplay.blit(text, textRect)
            

#info about current drawing
activeColor = Colors.black
activeWidth = 50
is_drawing = False

#things to save
backgroundColor = Colors.white
layers = [content_layer("Layer_0")]
current_layer = 0
redoCache = []
saving = False

scale = 10 # default screen scale
worldOrigin = [0,0] #center of screen for moving graphs
activeP = 0    #active point being edited
tDown = False  #keep track of previous tab input
prevMouse = 0 #keep track of previous mouse inputs
previous_keys = pygame.key.get_pressed()   #keep track of previous key inputs

screenRes = [1480,720]
gameDisplay = pygame.display.set_mode((screenRes[0],screenRes[1]))
pygame.display.set_caption("Simple Drawing")


#create frame
main_fr = frame()
main_fr.construct_frame()

def frame_point (pX,pY,width,height,color):
    pygame.draw.rect(gameDisplay,color,[pX,pY,width,height])
    
def point (pX,pY,width,height,color, shape = "rect"):
    global scale
    width *= scale/10
    height *= scale/10
    if(shape == "rect"):
        pygame.gfxdraw.box(gameDisplay,Rect(int(pX),int(pY),int(width),int(height)),color)
    if(shape == "ell"):
        pygame.gfxdraw.filled_ellipse(gameDisplay,int(pX),int(pY),int(width),int(height),color)

#simple call for main draw function
def draw_line(line, guides = False):
    draw_line_from_points(line.points,line.color,line.size,guides)
    
#complex method for drawing within other shapes
def draw_line_from_points(points, color, size, guides = False, resolution = 0.01):
    global scale
    global activeP
    global activeWidth
    global worldOrigin
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(points)):
        pointMatX.append(points[i].x + worldOrigin[0])
        pointMatY.append(points[i].y - worldOrigin[1])
    
    ##define Range
    tB = 0*scale # begin of range
    tE = 1*scale # end of range
    sT = tB      # set range traversal
     
    #define draw points
    drawPoint = pygame.Vector2()    
    
    ##Draw line
    if(len(pointMatX) == 2):
        while sT <= tE:
            t = sT/scale
            
            drawPoint.xy = float(((1-t) * pointMatX[0] + t * pointMatX[1])), float(((1-t) * pointMatY[0] + t * pointMatY[1]))
            drawPoint.xy = float(drawPoint.x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - drawPoint.y*scale)
            point(drawPoint.x-((size*scale/10)/2),drawPoint.y-((size*scale/10)/2), size, size, color, "ell")
            sT += resolution
            
    if (guides == True):    
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])       
        #draw previous points
        for i in range(len(pointMatX)):
            drawPoint.xy = float(pointMatX[i]*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - pointMatY[i]*scale)
            point(drawPoint.x,drawPoint.y,3,3,guides_color)   
        ##draw active move point     
        if(len(pointMatX) > activeP):
            drawPoint.xy = float(pointMatX[activeP]*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - pointMatY[activeP]*scale)
            point(drawPoint.x,drawPoint.y,5,5,guides_color)    
    
def draw_bez_line(line, guides):
    global scale
    global activeP
    global worldOrigin
    
    pointMatX = []
    pointMatY = []
    
    size = line.size
    #enter points to be drawn and adjusted
    for i in range (len(line.points)):
        pointMatX.append(line.points[i].x + worldOrigin[0])
        pointMatY.append(line.points[i].y - worldOrigin[1])
    
    #set matrix based on points given and create calc mats
    if(len(pointMatX) >= 3):
        refMat = line.bez_mats[len(pointMatX)-3]
        calcMatX = (np.matmul(pointMatX , refMat))
        calcMatY = (np.matmul(pointMatY , refMat))       
    
    
    ##define Range
    tB = 0*scale # begin of range
    tE = 1*scale # end of range
    sT = tB      # set range traversal
     
    #define draw points
    drawPoint = pygame.Vector2()    
    
    if(len(pointMatX) >= 3):
        ##Draw curve
        while sT <= tE:
            t = sT/scale
            if(len(pointMatX) == 3):
               tMatrix = [[t**2],
                          [t],
                          [1]]
            elif(len(pointMatX) == 4):
                tMatrix = [[t**3],
                          [t**2],
                          [t],
                          [1]]
            elif(len(pointMatX) == 5):
                tMatrix = [[t**4],
                          [t**3],
                          [t**2],
                          [t],
                          [1]]
            
            #Draw curve
            drawPoint.x = (np.matmul(calcMatX , tMatrix))[0]
            drawPoint.y = (np.matmul(calcMatY , tMatrix))[0]
            drawPoint.xy = float(drawPoint.x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - drawPoint.y*scale) 
            point(drawPoint.x-((size*scale/10)/2),drawPoint.y-((size*scale/10)/2), size, size, line.color,"ell")
            
            sT += 0.01
    
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])     
        #draw guide lines
        for i in range(len(pointMatX)-1):  
            guideLines = [line.points[i],line.points[i+1]]
            draw_line_from_points(guideLines, guides_color, 3, guides = False)                
        #draw previous points
        for i in range(len(pointMatX)):
            drawPoint.xy = float(pointMatX[i]*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - pointMatY[i]*scale)
            point(drawPoint.x,drawPoint.y,3,3,guides_color)   
        ##draw active move point     
        if(len(pointMatX) > activeP):
            drawPoint.xy = float(pointMatX[activeP]*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - pointMatY[activeP]*scale)
            point(drawPoint.x,drawPoint.y,5,5,guides_color)       

def draw_pixel_array(pixels):    
    global scale
    global activeP
    global worldOrigin
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(pixels.points)):
        pointMatX.append(pixels.points[i].x + worldOrigin[0])
        pointMatY.append(pixels.points[i].y - worldOrigin[1])
    
    #define draw points
    drawPoint = pygame.Vector2()    
    
    #draw previous points
    for i in range(len(pointMatX)-1):
        drawPoint.xy = float(pointMatX[i]*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - pointMatY[i]*scale)         
        point(drawPoint.x-(pixels.size/2),drawPoint.y-(pixels.size/2), pixels.size, pixels.size, pixels.color, "ell")
        
def draw_triangle(shape, guides):
    global worldOrigin
    #draw line AB
    if(len(shape.points)>=2):
        points = [shape.points[0],shape.points[1]]
        draw_line_from_points(points,shape.color,shape.size, False)
    #draw line BC
    
    if(len(shape.points)>=3):
        points = [shape.points[1],shape.points[2]]
        draw_line_from_points(points,shape.color,shape.size, False)
        
        #draw line CA
        points = [shape.points[2],shape.points[0]]
        draw_line_from_points(points,shape.color,shape.size, False)
        
    #draw guide points
    drawPoint = pygame.Vector2()
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])          
        #draw previous points
        for i in range(len(shape.points)):
            drawPoint.xy = float(shape.points[i].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[i].y*scale)
            point(drawPoint.x-2,drawPoint.y-2,3,3,guides_color)   
        ##draw active move point     
        if(len(shape.points) > activeP):
            drawPoint.xy = float(shape.points[activeP].x*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - shape.points[activeP].y*scale)
            point(drawPoint.x-3,drawPoint.y-3,5,5,guides_color)      

def draw_rectangle_filled(shape, guides):
    global worldOrigin
    if (len(shape.points) == 2):
        length = abs(shape.points[1].x - shape.points[0].x)*scale
        height = abs(shape.points[1].y - shape.points[0].y)*scale
        #calc new points in screen space
        drawPoint1 = pygame.Vector2()
        drawPoint1.xy = float((shape.points[0].x*scale)+worldOrigin[0] + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - (shape.points[0].y+worldOrigin[1])*scale)
          
        drawPoint2 = pygame.Vector2()
        drawPoint2.xy = float((shape.points[0].x*scale)+worldOrigin[0] + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - (shape.points[0].y+worldOrigin[1])*scale)
          
    
        point(drawPoint1.x, drawPoint1.y, length, height, shape.color)
    
    #draw guide points
    drawPoint = pygame.Vector2()
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])          
        #draw previous points
        for i in range(len(shape.points)):
            drawPoint.xy = float(shape.points[i].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[i].y*scale)
            point(drawPoint.x-2,drawPoint.y-2,3,3,guides_color)   
        ##draw active move point     
        if(len(shape.points) > activeP):
            drawPoint.xy = float(shape.points[activeP].x*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - shape.points[activeP].y*scale)
            point(drawPoint.x-3,drawPoint.y-3,5,5,guides_color)    

def draw_rectangle(shape, guides):
    global worldOrigin
    if (len(shape.points) == 2):
        length = (shape.points[1].x - shape.points[0].x)*scale
        height = (shape.points[0].y - shape.points[1].y)*scale
        #calc new points in screen space
        drawPoint1 = pygame.Vector2()
        drawPoint1.xy = float(shape.points[0].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[0].y*scale)
          
        drawPoint2 = pygame.Vector2()
        drawPoint2.xy = float(shape.points[1].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[1].y*scale)
          
        offset = shape.size/2
        point(drawPoint1.x-offset, drawPoint1.y-offset, shape.size, height, shape.color)
        point(drawPoint1.x-offset, drawPoint1.y-offset, length, shape.size, shape.color)
        point(drawPoint2.x-offset, drawPoint1.y-offset, shape.size, height, shape.color)
        point(drawPoint1.x-offset, drawPoint2.y-offset, length, shape.size, shape.color)        
        point(drawPoint2.x-offset, drawPoint2.y-offset, shape.size, shape.size, shape.color)
    
    #draw guide points
    drawPoint = pygame.Vector2()
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])          
        #draw previous points
        for i in range(len(shape.points)):
            drawPoint.xy = float(shape.points[i].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[i].y*scale)
            point(drawPoint.x-2,drawPoint.y-2,3,3,guides_color)   
        ##draw active move point     
        if(len(shape.points) > activeP):
            drawPoint.xy = float(shape.points[activeP].x*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - shape.points[activeP].y*scale)
            point(drawPoint.x-3,drawPoint.y-3,5,5,guides_color)    

def draw_ellipse(shape, guides = False):
    global scale
    global activeP
    global activeWidth
    global worldOrigin
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(shape.points)):
        pointMatX.append(shape.points[i].x + worldOrigin[0] )
        pointMatY.append(shape.points[i].y - worldOrigin[1] )
       
    
    
    ##define Range
    tB = 0*scale             # begin of range
    tE = 2 * math.pi * scale # end of range
    sT = tB                  # set range traversal  
    
    #draw ellipse
    drawPoint = pygame.Vector2()
    if(len(shape.points) == 3):
        r1 = shape.points[0].distance_to(shape.points[1])
        r2 = shape.points[0].distance_to(shape.points[2])
        while sT <= tE:
            t= sT/scale
            drawPoint.x = (((r1*math.cos(t)))*scale) + ((screenRes[0]/2)-1)
            drawPoint.y = (screenRes[1]/2)-1 + r2 * math.sin(t)*scale
            drawPoint.x = drawPoint.x + (pointMatX[0]*scale)
            drawPoint.y = drawPoint.y - (pointMatY[0]*scale)
            point(drawPoint.x-((shape.size/scale/10)/2),drawPoint.y-((shape.size/scale/10)/2), shape.size, shape.size, shape.color,"ell")
            sT+= 0.01
            
    
    #draw guidelines
    drawPoint = pygame.Vector2()
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])   
        
        if(len(shape.points) == 3):
            pygame.gfxdraw.circle(gameDisplay, int(pointMatX[0]*scale+((screenRes[0]/2)-1)), int((screenRes[1]/2)-1-pointMatY[0]*scale), int(r1*scale), guides_color) 
            pygame.gfxdraw.circle(gameDisplay, int(pointMatX[0]*scale+((screenRes[0]/2)-1)), int((screenRes[1]/2)-1-pointMatY[0]*scale), int(r2*scale), guides_color)
        #draw guide lines
        for i in range(len(pointMatX)):  
            guideLines = [shape.points[0],shape.points[i]]
            draw_line_from_points(guideLines, guides_color, 3, guides = False)    
    
def check_overlap(bounds):
    if(pygame.mouse.get_pos()[0] > bounds[0] and pygame.mouse.get_pos()[0] < bounds[1]):
        if(pygame.mouse.get_pos()[1] > bounds[2] and pygame.mouse.get_pos()[1] < bounds[3]):
            return True
        return False
    return False

def update(screenRes):    
    global scale
    global worldOrigin
    global activeP 
    global tDown
    global drawline
    global activeColor
    global activeWidth
    global is_drawing
    global new_shape
    global prevMouse
    global previous_keys
    global shapes
    global layers
    global current_layer
    global redoCache
    
    pressed_keys = pygame.key.get_pressed()
    
    #list of drawing tools
    draw_tools = ("Line","Bez Line","Pixel Draw","Triangle","Rectangle","Fill Rect.","Ellipse")
    ##Quit game on escape
    if (pressed_keys[K_ESCAPE]):   
        pygame.quit()
        
    ## Mouse on menu
    if(pygame.mouse.get_pos()[0] < 150 or pygame.mouse.get_pos()[0] > 1280):
        onMenu = True
    else:
        onMenu = False
        
    #check menu presses
    if (onMenu == True):
        if pygame.mouse.get_pressed()[0]:
            if prevMouse == 0:
                #check left buttons
                if(is_drawing and main_fr.actTool != "Pixel Draw"):
                    for i in range(len(main_fr.all_buttons)):
                        bounds =[main_fr.all_buttons[i].origin.x-14,
                                 main_fr.all_buttons[i].origin.x+14,
                                 main_fr.all_buttons[i].origin.y-14,
                                 main_fr.all_buttons[i].origin.y+14]
                
                        if(check_overlap(bounds)):
                            main_fr.actTool = main_fr.all_buttons[i].name
                            is_drawing = False                
                else:
                    for i in range(len(main_fr.all_buttons)-2):
                        bounds =[main_fr.all_buttons[i].origin.x-14,
                                 main_fr.all_buttons[i].origin.x+14,
                                 main_fr.all_buttons[i].origin.y-14,
                                 main_fr.all_buttons[i].origin.y+14]
                
                        if(check_overlap(bounds)):
                            main_fr.actTool = main_fr.all_buttons[i].name
                            is_drawing = False
            #layer buttons
                for i in range(len(layers)):
                    bounds =[layers[i].position[0]-74,
                         layers[i].position[0]+74,
                         layers[i].position[1]-15,
                         layers[i].position[1]+15]
                
                    if(check_overlap(bounds)):
                        current_layer=i
            #layer visibility buttons
                for i in range(len(layers)):
                    bounds =[layers[i].all_buttons[0].origin.x-14,
                         layers[i].all_buttons[0].origin.x+14,
                         layers[i].all_buttons[0].origin.y-14,
                         layers[i].all_buttons[0].origin.y+14]
                    if(check_overlap(bounds) and (prevMouse == False)):
                        layers[i].visible = not layers[i].visible
                        drawCache()
            
            #check Vert sliders
            for i in range(4):
                bounds =[main_fr.sliders[i].center.x-5,
                         main_fr.sliders[i].center.x+5,
                         main_fr.sliders[i].top.y-1,
                         main_fr.sliders[i].top.y+main_fr.sliders[i].height+1,]
                if(check_overlap(bounds)):
                    main_fr.sliders[i].value = main_fr.sliders[i].top.y+main_fr.sliders[i].height - pygame.mouse.get_pos()[1]
                    main_fr.sliders[i].value /= main_fr.sliders[i].height
                    main_fr.sliders[i].value = round(main_fr.sliders[i].value,3)
           
            #check Horizontal sliders
            #size slider
            bounds =[main_fr.sizeSlid.left.x-1 ,
                     main_fr.sizeSlid.left.x+5+main_fr.sizeSlid.width,
                     main_fr.sizeSlid.left.y-4,
                     main_fr.sizeSlid.left.y+4]
            if(check_overlap(bounds)):
                main_fr.sizeSlid.value = main_fr.sizeSlid.left.x+main_fr.sizeSlid.width - pygame.mouse.get_pos()[0]
                main_fr.sizeSlid.value /= main_fr.sizeSlid.width
                main_fr.sizeSlid.value = 1-main_fr.sizeSlid.value
                activeWidth = round(main_fr.sizeSlid.value*50)
                
            activeColor = (main_fr.sliders[0].color, main_fr.sliders[1].color, main_fr.sliders[2].color)
            if((main_fr.sliders[3].value*100)+10  != scale):
                scale = (main_fr.sliders[3].value*10)+10   
                drawCache()  
                
            prevMouse = pygame.mouse.get_pressed()[0]       
            return
      
    #set background based on fill tool
    if(main_fr.actTool == "Fill Back"):
        if (pygame.mouse.get_pressed()[0]):
            global backgroundColor
            backgroundColor = activeColor
            drawCache()
    if (main_fr.actTool == "Saving"):
        global saving 
        global gameDisplay
        saving = True        
    
    if (main_fr.actTool == "Exporting"):
        export_file()
        main_fr.actTool = "None"

    if (main_fr.actTool == "Load"):
        load_chd()
        main_fr.actTool = "None"
        drawCache()
    
    if (main_fr.actTool == "Importing"):
        if(len(layers) < 16):
            import_chd()
            main_fr.actTool = "None"
            drawCache()
        
    if (main_fr.actTool == "Add Layer"):        
        name = "Layer_0"
        nameID = 0
        cont = True
        while(cont):
            name = "Layer_"+str(nameID)
            for lay in layers:
                if name == lay.name:
                    nameID += 1                    
                    break
            else:
                cont = False       
        
        if(len(layers) < 16):
            layers.insert(0,content_layer(name))
        main_fr.actTool = "None"
    
    if (main_fr.actTool == "Rem Layer" and len(layers) > 0):
        del layers[current_layer]
        if(current_layer > len(layers)-1):
            current_layer -= 1
        main_fr.actTool = "None"
        drawCache()
    
    if (main_fr.actTool == "Layer Up" and len(layers) > 1):
        if(current_layer != 0):            
            tLayer = layers[current_layer]
            layers[current_layer] = layers[current_layer-1]
            layers[current_layer-1] = tLayer
            current_layer -=1
        main_fr.actTool = "None"
        drawCache()
    
    if (main_fr.actTool == "Layer Down" and len(layers) > 1):
        if(current_layer != len(layers)-1):            
            tLayer = layers[current_layer]
            layers[current_layer] = layers[current_layer+1]
            layers[current_layer+1] = tLayer
            current_layer +=1
        main_fr.actTool = "None"
        drawCache()
    
    #Don't draw if no layers
    if(len(layers) <= 0):
        prevMouse = pygame.mouse.get_pressed()[0]
        previous_keys = pressed_keys
        return
        
    ##undo
    if ((pressed_keys[K_LCTRL] and pressed_keys[K_z] and (not previous_keys[K_LCTRL] or not previous_keys[K_z])) or main_fr.actTool == "Undo"): 
        if(is_drawing and main_fr.actTool != "Pixel Draw"):
            if(len(new_shape.points) > 1):
               del new_shape.points[-1]
               activeP -= 1
        else:
            if(len(layers[current_layer].shape_list) > 0):
                redoCache.append(layers[current_layer].shape_list[len(layers[current_layer].shape_list)-1])
                del layers[current_layer].shape_list[len(layers[current_layer].shape_list)-1]
                drawCache()
                if(main_fr.actTool != "Pixel Draw"):
                    main_fr.actTool = "None"
    if ((pressed_keys[K_LCTRL] and pressed_keys[K_y] and (not previous_keys[K_LCTRL] or not previous_keys[K_y])) or main_fr.actTool == "Redo"):
        if(len(redoCache)>0):
            layers[current_layer].shape_list.append(redoCache[len(redoCache)-1])
            drawCache()
            del redoCache[len(redoCache)-1]
        main_fr.actTool = "None"
    #confirm new shape
    if(main_fr.actTool == "Added!"):
        redoCache = []
        layers[current_layer].shape_list.append(new_shape)
        drawCache()
        main_fr.actTool = "None"
        
    #check if using drawing tool
    if(main_fr.actTool in draw_tools):
        if(main_fr.actTool == "Pixel Draw"):
            if (prevMouse == True and pygame.mouse.get_pressed()[0] == False):
                new_shape = (shape(main_fr.actTool, activeWidth, activeColor))
                layers[current_layer].shape_list.append(new_shape)
                drawCache()
                activeP = 0     
        elif (is_drawing == False):
            new_shape = (shape(main_fr.actTool, activeWidth, activeColor))
            activeP = 0
        is_drawing = True            
    else:
        is_drawing = False
    
    if(is_drawing):
        ## set Active edit point\
        if (pressed_keys[K_TAB]):
            if (tDown == False):
                activeP +=1
                tDown = True
                if (activeP >= new_shape.pointLim):
                    activeP = 0
        else:
            tDown = False     
        if(onMenu == False):
            if pygame.mouse.get_pressed()[0]:
                new_point = pygame.Vector2()
                
                new_point[0]=(pygame.mouse.get_pos()[0]-(worldOrigin[0]*scale)-(screenRes[0]/2))/scale
                new_point[1]=((screenRes[1]/2)+(worldOrigin[1]*scale)-pygame.mouse.get_pos()[1])/scale
                
                if(len(new_shape.points) > 1):
                    if(new_point != new_shape.points[activeP-1]):
                        new_shape.addPoint(new_point,activeP)
                        if (activeP < new_shape.pointLim-1 and prevMouse == 0 and new_shape.pointLim != len(new_shape.points)):
                            activeP +=1                            
                        elif activeP < new_shape.pointLim-1 and (main_fr.actTool=="Pixel Draw"):
                            activeP +=1
                else:
                    new_shape.addPoint(new_point,activeP)
                    activeP +=1
                
                    
                    
        else:
            if pressed_keys[K_RIGHT]:
                drawline.points[activeP-1].x +=0.1
            if pressed_keys[K_LEFT]:
                drawline.points[activeP-1].x -=0.1        
            if pressed_keys[K_UP]:
                drawline.points[activeP-1].y +=0.1       
            if pressed_keys[K_DOWN]:
                drawline.points[activeP].y -=0.1   
        
            if(onMenu == False):
                if pygame.mouse.get_pressed()[0]:
                    drawline.points[activeP-1].y=((screenRes[1]/2)+(worldOrigin[1]*scale)-pygame.mouse.get_pos()[1])/scale
                    drawline.points[activeP-1].x=(pygame.mouse.get_pos()[0]-(worldOrigin[0]*scale)-(screenRes[0]/2))/scale
        
            
        
    #change scale
    if pressed_keys[K_KP_PLUS]:
        scale +=1      
    if pressed_keys[K_KP_MINUS]:    ##clamp lower end scaling
        scale -=1
    if (scale <= 0):
        scale+=1
    #cache previous user input
    prevMouse = pygame.mouse.get_pressed()[0]
    previous_keys = pressed_keys
       
def build_chd(name):
    global layers
    global current_layer
    global backgroundColor
    
    outtext = ["/* CHD */"]
    outtext.append("/* filename :" + name + " */")
    outtext.append("bg :" +str(backgroundColor[0])+","+str(backgroundColor[1])+","+str(backgroundColor[2]))
    
    for layer in layers:
        outtext.append("l :"+ layer.name)
        outtext.append("v :"+ str(layer.visible))
        if(len(layer.shape_list)<0):
           continue
        for j, shape in enumerate(layer.shape_list):
            outtext.append("s :"+str(j))
            outtext.append("shape :"+str(shape.shape))
            outtext.append("size :"+str(shape.size))
            outtext.append("col :"+str(shape.color[0])+","+str(shape.color[1])+","+str(shape.color[2]))
            for point in shape.points:
                outtext.append("p :"+str(point.x)+","+str(point.y))
    outtext.append("|")
    return outtext
                                
def load_chd():
    global layers
    global backgroundColor
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        filepath = filedialog.askopenfile(title="Load CHD",filetypes=(("CHD", "*.chd"), ("JPEG", "*.jpeg"))).name  
        file = open(filepath)
    except:
        print("Failed to Load")
        return
    
    
    pygame.display.set_caption("Simple Drawing ["+filepath.rsplit('/', 1)[1].rsplit('.', 1)[0]+".chd]")
    layers = [] #reset layers
    current_l = -1
    layer_name = ""
    visibility = ""
    shape_n = ""
    shape_s = 0
    shape_col = (0,0,0)
    points = []
    for line in file:
        if line[0] == "//":
            #header of file
            continue
        if(line.split(" ")[0] == "bg"):
            color = line.split(":")[1].split(",")
            backgroundColor = (int(color[0]),int(color[1]),int(color[2]))
            continue
        if(line[0] == "l"):
            layer_name = line.split(":")[1]
            layer_name = layer_name.rstrip(layer_name[-1])
            layers.append(content_layer(layer_name))
            current_l +=1
            continue
        if(line[0] == "v"):
            visibility = line.split(":")[1]
            visibility = visibility.rstrip(visibility[-1])
            if(visibility=="True"):
                layers[current_l].visible = True
            else:
                layers[current_l].visible = False                
            continue
        if(line.split(" ")[0] == "s"):
            #build shape and add to content layer if a shape has been made
            if(shape_n!=""):
                new_shape = (shape(shape_n,shape_s,shape_col))
                for point in points:
                    new_shape.addPoint(point)
                points = [] #clear local points
                layers[current_l].shape_list.append(new_shape)
            continue
        if(line.split(" ")[0] == "shape"):
            shape_n = line.split(":")[1]
            shape_n = shape_n.rstrip(shape_n[-1])
            continue
        if(line.split(" ")[0] == "size"):
            shape_s = int(line.split(":")[1])
            continue
        if(line.split(" ")[0] == "col"):
            color = line.split(":")[1].split(",")
            shape_col = (int(color[0]),int(color[1]),int(color[2]))
            continue
        if(line.split(" ")[0] == "p"):
            point = line.split(":")[1].split(",")
            points.append((float(point[0]),float(point[1])))
            continue
        if(line[0] == "|"):
            #build shape and add to content layer if a shape has been made
            if(shape_n!=""):
                new_shape = shape(shape_n,shape_s,shape_col)
                for point in points:
                    new_shape.addPoint(point)
                points = [] #clear local points
                layers[current_l].shape_list.append(new_shape)
            continue
                    
def import_chd():
    global layers
    global current_layer
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        filepath = filedialog.askopenfile(title="Import CHD",filetypes=(("CHD", "*.chd"), ("JPEG", "*.jpeg"))).name  
        file = open(filepath)
    except:
        print("Failed to Import")
        return
    layer_name = ""
    visibility = ""
    addShape = True
    shape_n = ""
    shape_s = 0
    shape_col = (0,0,0)
    points = []
    layers.insert(current_layer,content_layer(filepath.rsplit('/', 1)[1].rsplit('.', 1)[0]))
    for line in file:
        if line[0] == "//":
            #header of file
            continue
        if(line[0] == "l"):
            layer_name = line.split(":")[1]
            layer_name = layer_name.rstrip(layer_name[-1])
            continue
        if(line[0] == "v"):
            visibility = line.split(":")[1]
            visibility = visibility.rstrip(visibility[-1])
            if(visibility=="True"):
                addShape = True
            else:
                addShape = False                
            continue
        if(not addShape):
            continue
        if(line.split(" ")[0] == "s"):
            #build shape and add to content layer if a shape has been made
            if(shape_n!=""):
                new_shape = (shape(shape_n,shape_s,shape_col))
                for point in points:
                    new_shape.addPoint(point)
                points = [] #clear local points
                layers[current_layer].shape_list.append(new_shape)
            continue
        if(line.split(" ")[0] == "shape"):
            shape_n = line.split(":")[1]
            shape_n = shape_n.rstrip(shape_n[-1])
            continue
        if(line.split(" ")[0] == "size"):
            shape_s = int(line.split(":")[1])
            continue
        if(line.split(" ")[0] == "col"):
            color = line.split(":")[1].split(",")
            shape_col = (int(color[0]),int(color[1]),int(color[2]))
            continue
        if(line.split(" ")[0] == "p"):
            point = line.split(":")[1].split(",")
            points.append((float(point[0]),float(point[1])))
            continue
        if(line[0] == "|"):
            #build shape and add to content layer if a shape has been made
            if(shape_n!=""):
                new_shape = shape(shape_n,shape_s,shape_col)
                for point in points:
                    new_shape.addPoint(point)
                points = [] #clear local points
                layers[current_layer].shape_list.append(new_shape)
            continue
            
def export_file():    
    root = tk.Tk()
    root.withdraw()
    try:
        filepath = filedialog.asksaveasfile(title="Export CHD",defaultextension = "*.chd",filetypes=(("CHD", "*.chd"), ("", "*"))).name         
        filename = filepath.rsplit('/', 1)[1]
        file_out = build_chd(filename)          
        pygame.display.set_caption("Simple Drawing ["+filepath.rsplit('/', 1)[1].rsplit('.', 1)[0]+".chd]")
        f = open (filepath,"a")
        for line in file_out:
            f.write(line+"\n")
        f.close()
    except:  
        print("error")
        pass
    
def save_file():
    root = tk.Tk()
    root.withdraw()
    try:
        filepath = filedialog.asksaveasfile(title="Save Image",filetypes=(("PNG", "*.png"), ("JPEG", "*.jpeg"))).name   
        pygame.image.save(gameDisplay, filepath)
    except:  
        pass

def drawCache():
    global backgroundImage
    global layers
    global current_layer
    global backgroundColor

    #draw bacdrop
    gameDisplay.fill(backgroundColor)
    
    for i in range (len(layers)):
        layer = layers[len(layers)-i-1]
        if(not layer.visible):
            continue
        for i in range (len(layer.shape_list)):      
            if (layer.shape_list[i].shape =="Line"):
                draw_line(layer.shape_list[i], False)
            if (layer.shape_list[i].shape  =="Pixel Draw"):
                draw_pixel_array(layer.shape_list[i])
            if (layer.shape_list[i].shape  =="Ellipse"):
                draw_ellipse(layer.shape_list[i], False)
            if (layer.shape_list[i].shape  =="Triangle"):
                draw_triangle(layer.shape_list[i], False)
            if (layer.shape_list[i].shape  == "Rectangle"):
                draw_rectangle(layer.shape_list[i], False)
            if (layer.shape_list[i].shape  =="Fill Rect."):
                draw_rectangle_filled(layer.shape_list[i], False)
            if (layer.shape_list[i].shape  =="Bez Line"):
                draw_bez_line(layer.shape_list[i], False)
            
    #cache image
    pygame.image.save(gameDisplay, "CacheImage.png")     

    #load cached shapes        
    backgroundImage = pygame.image.load('CacheImage.png')
    backgroundImage = pygame.transform.scale(backgroundImage,(screenRes[0],screenRes[1]))                       
    
##game loop to play
def gameLoop():
    global newShape
    global is_drawing
    global gameDisplay
    global saving
    global worldOrigin
    global backgroundImage
    global screenRes
    global activeColor
    global scale
    
    gameExit = False
    
    drawCache()
    
    while not gameExit:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 os.remove("CacheImage.png")
                 gameExit = True
        ##get user input
        update(screenRes)
        
        
        gameDisplay.blit(backgroundImage, (0, 0))
        
        if (is_drawing):    
            new_shape.color = activeColor
            new_shape.size = activeWidth
            if (new_shape.shape =="Line"):
                draw_line(new_shape, True)            
            if (new_shape.shape  =="Pixel Draw"):
                draw_pixel_array(new_shape)
            if (new_shape.shape =="Ellipse"):
                draw_ellipse(new_shape, True)
            if (new_shape.shape =="Triangle"):
                draw_triangle(new_shape, True)
            if (new_shape.shape =="Rectangle"):
                draw_rectangle(new_shape, True)
            if (new_shape.shape =="Fill Rect."):
                draw_rectangle_filled(new_shape, True)
            if (new_shape.shape =="Bez Line"):
                draw_bez_line(new_shape, True)
        
        
        if (saving == True):                       
            screenRes = [1130,720]
            gameDisplay = pygame.display.set_mode((screenRes[0],screenRes[1]))
            ts = scale
            scale = 10
            worldOrigin = [2,0]
            drawCache()
            save_file()
            screenRes = [1480,720]
            worldOrigin = [0,0]
            scale = ts
            gameDisplay = pygame.display.set_mode((screenRes[0],screenRes[1]))
            drawCache()
            main_fr.actTool = "None"  
            saving = False
            
        main_fr.draw_frame()
        
        pygame.display.update() 
        
def main():
    ##run game loop
    gameLoop()
    print("Program closed")
    pygame.quit()

if __name__=="__main__":
    main()