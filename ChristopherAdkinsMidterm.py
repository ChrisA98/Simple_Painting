# -*- coding: utf-8 -*-
"""
Christopher Adkins
CSC 550
Midterm exam - draw images with primitive shapes.
"""
import pygame, sys
from pygame.locals import *
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
        if (self.shape =="Line"):
            self.pointLim = 2
        if (self.shape =="Bez Line"):
            self.pointLim = 5
        if (self.shape =="Triangle"):
            self.pointLim = 3
        if (self.shape =="Rectangle"):
            self.pointLim = 2
        if (self.shape =="Fill Rect."):
            self.pointLim = 2
        if (self.shape =="Ellipse"):
            self.pointLim = 3
        
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
            

class button():
    def __init__(self, origin_, name_):
        self.name = name_
        self.scaleX = 25
        self.scaleY = 25
        self.origin = pygame.Vector2()
        self.origin.xy = origin_[0],origin_[1]
        self.color = black
        self.active = False
        self.off_color = dark_grey
        self.on_color = off_black
        self.off_l_color = off_black
        self.on_l_color = white
        
    def design_button(self, pixels):
        #define button design
        self.pixels = pixels
        
    def draw_button(self, act_tool):
        #draw backing of button
        point(self.origin.x-13, self.origin.y-13, 27, 27, grey)
        if(act_tool == self.name):     
            point(self.origin.x-13, self.origin.y-13, 27, 27, self.on_l_color)       
            point(self.origin.x-12, self.origin.y-12, 25, 25, self.on_color)
        else:
            point(self.origin.x-13, self.origin.y-13, 27, 27, self.off_l_color )
            point(self.origin.x-12, self.origin.y-12, 25, 25, self.off_color)
        #draw button icon
        for i in range(25):
            for j in range(25):
                if (self.pixels[i][j] == 1):
                    point(self.origin.x-12+j, self.origin.y-12+i, 1, 1, grey)
                    
    def set_colors(self, off_color, on_color, on_l_color, off_l_color=(20,20,20)):
        self.off_color = off_color
        self.on_color = on_color
        self.off_l_color = off_l_color
        self.on_l_color = on_l_color
        
class slider():
    
    def __init__(self, top_, height_, val):
        self.top = pygame.Vector2()
        self.top.xy = top_[0], top_[1]
        self.height = height_
        self.value = val
    
    def draw_slider(self):
        point(self.top.x-1,self.top.y,6,self.height,grey)
        point(self.top.x,self.top.y,4,self.height,off_black)
        sliderSpot = pygame.Vector2()
        sliderSpot.y = self.top.y+self.height-(self.height*self.value)-5
        sliderSpot.x = self.top.x-3
        point(sliderSpot.x,sliderSpot.y,11,11,grey)
        point(sliderSpot.x+2,sliderSpot.y+2,7,7,white)
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
        point(self.left.x, self.left.y-1,self.width,5,grey)
        point(self.left.x, self.left.y, self.width,3,off_black)
        sliderSpot = pygame.Vector2()
        sliderSpot.y = self.left.y-4
        sliderSpot.x = self.left.x+(self.width*self.value)-4
        point(sliderSpot.x,sliderSpot.y,11,11,grey)
        point(sliderSpot.x+2,sliderSpot.y+2,7,7,white)
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
        self.clean_array()        
        frame.draw_button_points(self.points, 20, 24, 1, 5)
        for i in range(3, 21):
            frame.draw_button_points(self.points, i, i+2, 25-i-2, 25-i)
        frame.draw_button_points(self.points, 1, 5, 20, 24)
        self.points[1][22] = 1        
        
        self.line_button = button((30,40),"Line")
        self.line_button.design_button(self.points)
        self.all_buttons.append(self.line_button)
        
        #bezier  tool        
        self.clean_array()        
        frame.draw_button_points(self.points, 20, 24, 1, 5)
        for i in range(3, 21):
            frame.draw_button_points(self.points, i, i+2, 25-i-2, 25-i)
        for i in range(6, 18):
            self.points[i][i] = 1 
        for i in range(6, 18):
            self.points[i][i-1] = 1         
        for i in range(6, 18):
            self.points[i][i+1] = 1 
        frame.draw_button_points(self.points, 1, 5, 20, 24)        
        self.points[1][22] = 1        
        
        self.bez_button = button((60,40),"Bez Line")
        self.bez_button.design_button(self.points)
        self.all_buttons.append(self.bez_button)               
        
        #Pixel tool
        self.clean_array()       
        frame.draw_button_points(self.points, 10, 16, 10, 16)
        
        self.pix_button = button((90,40),"Pixel Draw")
        self.pix_button.design_button(self.points)
        self.all_buttons.append(self.pix_button)   
        
        #triangle tool
        self.clean_array()       
        frame.draw_button_points(self.points, 4, 22, 18, 20)
        self.points[17][4] = 1
        frame.draw_button_points(self.points, 5, 6, 15, 18)
        for i in range (8):
            frame.draw_button_points(self.points, i+5, i+8, 15-i, 17-i)        
        for i in range (10):
            frame.draw_button_points(self.points, i+11, i+14, 8+i, 10+i)
        self.tri_button = button((120,40),"Triangle")
        self.tri_button.design_button(self.points)
        self.all_buttons.append(self.tri_button)     
        
        #rect tool
        self.clean_array()       
        frame.draw_button_points(self.points, 5, 21, 5, 21)
        frame.erase_button_points(self.points, 8, 18, 8, 18)
        
        self.pix_button = button((30,70),"Rectangle")
        self.pix_button.design_button(self.points)
        self.all_buttons.append(self.pix_button)
        
        #filled rect tool
        self.clean_array()       
        frame.draw_button_points(self.points, 5, 21, 5, 21)
        
        self.pix_button = button((60,70),"Fill Rect.")
        self.pix_button.design_button(self.points)
        self.all_buttons.append(self.pix_button)
        
        #Ellipse tool
        self.clean_array()       
        frame.draw_button_points(self.points, 10, 17, 1,3)
        frame.draw_button_points(self.points, 8, 12, 2,4)
        frame.draw_button_points(self.points, 15, 19, 2,4)
        frame.draw_button_points(self.points, 6, 10, 4,6)
        frame.draw_button_points(self.points, 17, 21, 4,6)
        frame.draw_button_points(self.points, 4, 8, 6, 8)
        frame.draw_button_points(self.points, 19, 23, 6, 8)
        frame.draw_button_points(self.points, 2, 5, 8, 15)
        frame.draw_button_points(self.points, 21, 24, 8, 15)
        frame.draw_button_points(self.points, 19, 23, 15, 17)
        frame.draw_button_points(self.points, 4, 8, 15, 17)
        frame.draw_button_points(self.points, 6, 10, 17,19)
        frame.draw_button_points(self.points, 17, 21, 17,19)
        frame.draw_button_points(self.points, 8, 12, 19,21)
        frame.draw_button_points(self.points, 15, 19, 19,21)
        frame.draw_button_points(self.points, 10, 17, 21,22)
        
        self.cir_button = button((90,70),"Ellipse")
        self.cir_button.design_button(self.points)
        self.all_buttons.append(self.cir_button)
        
        #fill tool
        self.clean_array()       
        frame.draw_button_points(self.points, 7, 9, 2, 14) 
        for i in range (8):
            frame.draw_button_points(self.points, i+5, i+8, 15-i, 17-i)        
        for i in range (7):
            frame.draw_button_points(self.points, i+11, i+14, 8+i, 10+i)        
        for i in range (7):
            frame.draw_button_points(self.points, i+9, i+12, 21-i, 23-i)         
        for i in range (6):
            frame.draw_button_points(self.points, i+5, i+7, 16+i, 18+i)    
        frame.draw_button_points(self.points, 18, 22, 14, 24)         
        self.pix_button = button((120,70),"Fill Back")
        self.pix_button.design_button(self.points)
        self.all_buttons.append(self.pix_button) 
        
        #save button tool
        self.clean_array()       
        frame.draw_button_points(self.points, 2, 23, 2, 23) 
        frame.erase_button_points(self.points, 6, 8, 1, 10) 
        frame.erase_button_points(self.points, 7, 17, 10, 11) 
        frame.erase_button_points(self.points, 16, 18, 1, 10) 
        frame.erase_button_points(self.points, 12, 14, 1, 4) 
        frame.erase_button_points(self.points, 15, 17, 1, 4) 
        self.points[22][2] = 0
        self.points[22][21] = 0
        
        self.pix_button = button((30,100),"Saving")
        self.pix_button.design_button(self.points)
        self.all_buttons.append(self.pix_button) 
        
        #confirm button
        self.clean_array()       
        
        self.add_button = button((90,100),"Added!")
        self.add_button.set_colors(green, dark_green, white)
        self.add_button.design_button(self.points)
        self.all_buttons.append(self.add_button)
        
        #cancel button
        self.clean_array()       
        
        self.rem_button = button((120,100),"Canceled!")
        self.rem_button.set_colors(red, darkRed, white)
        self.rem_button.design_button(self.points)
        self.all_buttons.append(self.rem_button) 
        
        
        #build sliders        
        self.redSlid = slider((30,320),100,1)
        self.greenSlid = slider((70,320),100,1)
        self.blueSlid = slider((110,320),100,1)
        
        self.zoomSlid = slider((65,580),100,0)
        
        self.sizeSlid = sliderHorizontal((20,470), 100, 1)
        
        self.sliders =[self.redSlid, self.greenSlid, self.blueSlid, self.zoomSlid]
    
    def draw_frame(self):      
        global activeColor
        global is_drawing
        #frame Backdrop
        point(0,0,150,720,dark_grey)
        
        # draw buttons
        if (is_drawing):
            for i in range(len(self.all_buttons)):
                self.all_buttons[i].draw_button(self.actTool)
        else:
            for i in range(len(self.all_buttons)-2):
                self.all_buttons[i].draw_button(self.actTool)
            
        #divider 1
        self.divHeight = 120
        point(0,self.divHeight,150,1,grey)
        point(0,self.divHeight+1,150,1,dark_grey)
        point(0,self.divHeight+2,150,2,off_black)
        
        #divider 1
        self.divHeight = 160
        point(0,self.divHeight,150,1,grey)
        point(0,self.divHeight+1,150,1,dark_grey)
        point(0,self.divHeight+2,150,2,off_black)
        
        
        point(148,0,2,720,off_black)
        point(150,0,2,720,dark_grey)
        point(152,0,2,720,grey)
        
        # draw tool title
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("Tools", True, black)      
        textRect = text.get_rect()
        textRect.center = (77,17)
        gameDisplay.blit(text, textRect)
        text = font.render("Tools", True, grey)    
        textRect.center = (75,15)
        gameDisplay.blit(text, textRect)
        
        
        # draw actvive tool text
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Using: "+self.actTool, True, black) 
        textRect.center = (44,146)
        gameDisplay.blit(text, textRect)
        text = font.render("Using: "+self.actTool, True, grey) 
        textRect.center = (42,144)
        gameDisplay.blit(text, textRect)
        
        
        #draw color sample
        point(15,170,120,120,activeColor)
        point(15,285,120,5,white)
        point(132,170,5,120,off_black)
        point(132,285,5,5,grey)
        
        # write actvive color value text
        font = pygame.font.Font('freesansbold.ttf', 14)
        text = font.render("R: "+(str)(activeColor[0])+ "  G: "+(str)(activeColor[1])+" B: "+(str)(activeColor[2]), True, black) 
        textRect.center = (27,310)
        gameDisplay.blit(text, textRect)
        text = font.render("R: "+(str)(activeColor[0])+ "  G: "+(str)(activeColor[1])+" B: "+(str)(activeColor[2]), True, grey) 
        textRect.center = (29,310)
        gameDisplay.blit(text, textRect)
        
        #draw sliders
        self.redSlid.draw_slider()
        self.greenSlid.draw_slider()
        self.blueSlid.draw_slider()  
        
        #divider 2
        self.divHeight = 430
        point(0,self.divHeight,150,1,grey)
        point(0,self.divHeight+1,150,1,dark_grey)
        point(0,self.divHeight+2,150,2,off_black)
        
        # draw actvive line width text
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Line Size: "+(str)(activeWidth), True, black) 
        textRect.center = (44,452)
        gameDisplay.blit(text, textRect)
        text = font.render("Line Size: "+(str)(activeWidth), True, grey) 
        textRect.center = (42,450)
        gameDisplay.blit(text, textRect)
        self.sizeSlid.draw_slider()
        
        #divider 3
        self.divHeight = 500
        point(0,self.divHeight,150,1,grey)
        point(0,self.divHeight+1,150,1,dark_grey)
        point(0,self.divHeight+2,150,2,off_black)
        
        
        self.zoomSlid.draw_slider()
        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render("+", True, black) 
        textRect.center = (87,566)
        gameDisplay.blit(text, textRect)
        text = font.render("-", True, black) 
        textRect.center = (90,690)
        gameDisplay.blit(text, textRect)
        
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("Zoom: "+(str)(round(scale)), True, black) 
        textRect.center = (62,552)
        gameDisplay.blit(text, textRect)
        text = font.render("Zoom: "+(str)(round(scale)), True, grey) 
        textRect.center = (60,550)
        gameDisplay.blit(text, textRect)
        
        #draw mouse point        
        activeX = pygame.mouse.get_pos()[0]-150
        if(activeX < 0):
            activeX=0
        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render("X: "+(str)(activeX)+", Y: "+(str)(pygame.mouse.get_pos()[1]), True, grey) 
        textRect.center = (200,30)
        gameDisplay.blit(text, textRect)   
        
        
        
        
FPS = 60
FramePerSec = pygame.time.Clock()

#basic colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (190, 190, 190)
dark_grey = (75, 75, 75)
dark_green = (0, 150, 0)
off_black = (20, 20, 20)
red = (255, 0, 0)
darkRed = (155, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#info about current drawing
activeColor = white
activeWidth = 50
is_drawing = False

#things to save
backgroundColor = white
shapes = []
saving = False

scale = 10 #screen scale

#center of screen for moving graphs (currently deprecated, but may readd moving items, so left implementation)
origin = [0,0]
activeP = 0    #active point being edited
tDown = False  #keep track of previous tab input
prevMouse = False  #keep trakc of previous mouse inputs
previous_keys = pygame.key.get_pressed()   #keep trakc of previous key inputs
new_shape = (shape("Line", 0, white))

screenRes = [1280,720]
gameDisplay = pygame.display.set_mode((screenRes[0],screenRes[1]))
pygame.display.set_caption("Simple Shapes Drawing")

def point (pX,pY,width,height,color):
    pygame.draw.rect(gameDisplay,color,[pX,pY,width,height])

#simple call for main draw function
def draw_line(origin, line, guides = False):
    draw_line_from_points(origin,line.points,line.color,line.size,guides)
    
#complex method for drawing within other shapes
def draw_line_from_points(origin, points, color, size, guides = False):
    global scale
    global activeP
    global activeWidth
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(points)):
        pointMatX.append(points[i].x + origin[0])
        pointMatY.append(points[i].y - origin[1])
    
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
            point(drawPoint.x-(size/2),drawPoint.y-(size/2), size, size, color)
            sT += 0.01
            #stop drawing outside of screen
            if(drawPoint.y > 0 or drawPoint.x < 0):
                continue        
            if(drawPoint.y > screenRes[1] or drawPoint.x < screenRes[0]):
                break
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
    
def draw_bez_line(origin, line, guides):
    global scale
    global activeP
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(line.points)):
        pointMatX.append(line.points[i].x + origin[0])
        pointMatY.append(line.points[i].y - origin[1])
    
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
            point(drawPoint.x-(line.size/2),drawPoint.y-(line.size/2), line.size, line.size, line.color)
            
            sT += 0.01
            #stop drawing outside of screen
            if(drawPoint.y > 0 or drawPoint.x < 0):
                continue        
            if(drawPoint.y > screenRes[1] or drawPoint.x < screenRes[0]):
                break
    
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])     
        #draw guide lines
        for i in range(len(pointMatX)-1):  
            guideLines = [line.points[i],line.points[i+1]]
            draw_line_from_points(origin, guideLines, guides_color, 3, guides = False)                
        #draw previous points
        for i in range(len(pointMatX)):
            drawPoint.xy = float(pointMatX[i]*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - pointMatY[i]*scale)
            point(drawPoint.x,drawPoint.y,3,3,guides_color)   
        ##draw active move point     
        if(len(pointMatX) > activeP):
            drawPoint.xy = float(pointMatX[activeP]*scale + (screenRes[0]/2)-2), float((screenRes[1]/2)-2 - pointMatY[activeP]*scale)
            point(drawPoint.x,drawPoint.y,5,5,guides_color)       

def draw_pixel_array(origin, pixels):    
    global scale
    global activeP
    
    pointMatX = []
    pointMatY = []
    
    #enter points to be drawn and adjusted
    for i in range (len(pixels.points)):
        pointMatX.append(pixels.points[i].x + origin[0])
        pointMatY.append(pixels.points[i].y - origin[1])
        
    #define draw points
    drawPoint = pygame.Vector2()    
    
    #draw previous points
    for i in range(len(pointMatX)):
        drawPoint.xy = float(pointMatX[i]*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - pointMatY[i]*scale)
        point(drawPoint.x-(pixels.size/2),drawPoint.y-(pixels.size/2), pixels.size, pixels.size, pixels.color)
        
def draw_triangle(origin, shape, guides):
    #draw line AB
    if(len(shape.points)>=2):
        points = [shape.points[0],shape.points[1]]
        draw_line_from_points(origin,points,shape.color,shape.size, False)
    #draw line BC
    
    if(len(shape.points)>=3):
        points = [shape.points[1],shape.points[2]]
        draw_line_from_points(origin,points,shape.color,shape.size, False)
        
        #draw line CA
        points = [shape.points[2],shape.points[0]]
        draw_line_from_points(origin,points,shape.color,shape.size, False)
        
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

def draw_rectangle_filled(origin, shape, guides):
    if (len(shape.points) == 2):
        length = abs(shape.points[0].x - shape.points[1].x)*scale
        height = abs(shape.points[0].y - shape.points[1].y)*scale
        #calc new points in screen space
        drawPoint1 = pygame.Vector2()
        drawPoint1.xy = float(shape.points[0].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[0].y*scale)
          
        drawPoint2 = pygame.Vector2()
        drawPoint2.xy = float(shape.points[0].x*scale + (screenRes[0]/2)-1), float((screenRes[1]/2)-1 - shape.points[0].y*scale)
          
    
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

def draw_rectangle(origin, shape, guides):
    if (len(shape.points) == 2):
        length = abs(shape.points[0].x - shape.points[1].x)*scale
        height = abs(shape.points[0].y - shape.points[1].y)*scale
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

def draw_ellipse(origin, shape, guides = False):
    global scale
    global activeP
    global activeWidth
    
    pointMatX = []
    pointMatY = []
    
        #enter points to be drawn and adjusted
    for i in range (len(shape.points)):
        pointMatX.append(shape.points[i].x + origin[0] )
        pointMatY.append(shape.points[i].y - origin[1] )
       
    
    ##define Range
    tB = 0*scale # begin of range
    tE = 2 * math.pi * scale # end of range
    sT = tB      # set range traversal  
    
    #draw ellipse
    drawPoint = pygame.Vector2()
    if(len(shape.points) == 3):
        while sT <= tE:
            t= sT/scale
            drawPoint.x = (((pointMatX[1]*math.cos(t)))*scale) + ((screenRes[0]/2)-1)
            drawPoint.y = (screenRes[1]/2)-1 + pointMatY[i] * math.sin(t)*scale
            drawPoint.x = drawPoint.x + (pointMatX[0]*scale)
            drawPoint.y = drawPoint.y - (pointMatY[0]*scale)
            point(drawPoint.x-(shape.size/2),drawPoint.y-(shape.size/2), shape.size, shape.size, shape.color)
            sT+= 0.01
            
    
    #draw guidelines
    drawPoint = pygame.Vector2()
    if (guides == True):
        #create guide color inverted from background color
        guides_color = (255-backgroundColor[0], 255-backgroundColor[1], 255-backgroundColor[2])     
        #draw guide lines
        for i in range(len(pointMatX)):  
            guideLines = [shape.points[0],shape.points[i]]
            draw_line_from_points(origin, guideLines, guides_color, 3, guides = False)    
    

def check_overlap(bounds):
    if(pygame.mouse.get_pos()[0] > bounds[0] and pygame.mouse.get_pos()[0] < bounds[1]):
        if(pygame.mouse.get_pos()[1] > bounds[2] and pygame.mouse.get_pos()[1] < bounds[3]):
            return True
        return False
    return False


def update(screenRes):
    pressed_keys = pygame.key.get_pressed()
    
    global scale
    global origin
    global activeP 
    global tDown
    global drawline
    global activeColor
    global activeWidth
    global is_drawing
    global new_shape
    global prevMouse
    global previous_keys
    
    #list of drawing tools
    draw_tools = ("Line","Bez Line","Pixel Draw","Triangle","Rectangle","Fill Rect.","Ellipse")
    ##Quit game on escape
    if (pressed_keys[K_ESCAPE]):   
        pygame.quit()
        
    ## Mouse on menu
    if(pygame.mouse.get_pos()[0] < 150):
        onMenu = True
    else:
        onMenu = False
        
    #check menu presses
    if (onMenu == True):
        if pygame.mouse.get_pressed()[0]:
            #check buttons
            for i in range(len(main_fr.all_buttons)):
                bounds =[main_fr.all_buttons[i].origin.x-14,
                         main_fr.all_buttons[i].origin.x+14,
                         main_fr.all_buttons[i].origin.y-14,
                         main_fr.all_buttons[i].origin.y+14]
                
                if(check_overlap(bounds)):
                        main_fr.actTool = main_fr.all_buttons[i].name
                        is_drawing = False
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
            scale = (main_fr.sliders[3].value*100)+10
            return
      
    #set background based on fill tool
    if(main_fr.actTool == "Fill Back"):
        if (pygame.mouse.get_pressed()[0]):
            global backgroundColor
            backgroundColor = activeColor
    if (main_fr.actTool == "Saving"):
        global saving 
        global gameDisplay
        saving = True           
    
    
    ##undo
    if (pressed_keys[K_LCTRL] and pressed_keys[K_z] and (not previous_keys[K_LCTRL] or not previous_keys[K_z])): 
        if(is_drawing):
            if(len(new_shape.points) > 1):
               del new_shape.points[-1]
               activeP -= 1
        else:
            if(len(shapes) > 0):
                  del shapes[len(shapes)-1]
        
        
    #confirm new shape
    if(main_fr.actTool == "Added!"):
        shapes.append(new_shape)
        main_fr.actTool = "None"
        
    #check if using drawing tool
    if(main_fr.actTool in draw_tools):
        if (is_drawing == False):
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
                
                new_point[0]=(pygame.mouse.get_pos()[0]-(origin[0]*scale)-(screenRes[0]/2))/scale
                new_point[1]=((screenRes[1]/2)+(origin[1]*scale)-pygame.mouse.get_pos()[1])/scale
                
                if(len(new_shape.points) >= 1):
                    if(new_point != new_shape.points[activeP-1]):
                        new_shape.addPoint(new_point,activeP)
                        if (activeP < new_shape.pointLim-1 and prevMouse == False and new_shape.pointLim != len(new_shape.points)):
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
                    drawline.points[activeP-1].y=((screenRes[1]/2)+(origin[1]*scale)-pygame.mouse.get_pos()[1])/scale
                    drawline.points[activeP-1].x=(pygame.mouse.get_pos()[0]-(origin[0]*scale)-(screenRes[0]/2))/scale
        
            
        
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
           
##game loop to play
def gameLoop():
    global newShape
    global is_drawing
    global gameDisplay
    global saving
    gameExit = False
    print("Inside gameloop")
    while not gameExit:
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 gameExit = True
        ##get user input
        update(screenRes)
        
        #draw bacdrop
        gameDisplay.fill(backgroundColor)
                                
        #draw cached shapes
        for i in range (len(shapes)):      
            if (shapes[i].shape =="Line"):
                draw_line(origin, shapes[i], False)
            if (shapes[i].shape  =="Pixel Draw"):
                draw_pixel_array(origin, shapes[i])
            if (shapes[i].shape  =="Ellipse"):
                draw_ellipse(origin, shapes[i], False)
            if (shapes[i].shape  =="Triangle"):
                draw_triangle(origin, shapes[i], False)
            if (shapes[i].shape  == "Rectangle"):
                draw_rectangle(origin, shapes[i], False)
            if (shapes[i].shape  =="Fill Rect."):
                draw_rectangle_filled(origin, shapes[i], False)
            if (shapes[i].shape  =="Bez Line"):
                draw_bez_line(origin, shapes[i], False)
        
        if (is_drawing):    
            new_shape.color = activeColor
            new_shape.size = activeWidth
            if (new_shape.shape =="Line"):
                draw_line(origin, new_shape, True)            
            if (new_shape.shape  =="Pixel Draw"):
                draw_pixel_array(origin, new_shape)
            if (new_shape.shape =="Ellipse"):
                draw_ellipse(origin, new_shape, True)
            if (new_shape.shape =="Triangle"):
                draw_triangle(origin, new_shape, True)
            if (new_shape.shape =="Rectangle"):
                draw_rectangle(origin, new_shape, True)
            if (new_shape.shape =="Fill Rect."):
                draw_rectangle_filled(origin, new_shape, True)
            if (new_shape.shape =="Bez Line"):
                draw_bez_line(origin, new_shape, True)
        
        
        if (saving == True):           
            pygame.image.save(gameDisplay, "SavedImage.png")
            main_fr.actTool = "None"  
            saving = False
            
        main_fr.draw_frame()
        
        pygame.display.update() 
        
#create frame
main_fr = frame()
main_fr.construct_frame()

##run game loop
gameLoop()
print("Program closed")
pygame.quit()

