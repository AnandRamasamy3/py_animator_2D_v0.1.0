import pygame,sys,math,random,os,threading,socket,json,time
from pygame.locals import *


class tools_box:
    def __init__(self,main,surface,database):
        self.main=main
        self.surface=surface
    def select_button(self):
        print ("got select button")
    def pen_button(self):
        # print ("got pen button")
        self.main.current_tool="pen_button"
    def eraser_button(self):
        # print ("got eraser button")
        self.main.current_tool="eraser_button"
        # pygame.draw.rect(self.main.surface,self.main.colors["black"],(self.main.mouse[0],self.main.mouse[0],10,10),1)
    def paint_bucket_button(self):
        print ("got paint bucket button")
    def clear_button(self):
        self.main.total_time_strip[self.main.layers][self.main.current_layer][self.main.current_object]["points"]=[]
    def clear_layer_button(self):
        self.main.total_time_strip[self.main.layers][self.main.current_layer]=[
            {"name":self.main.generate_new_object_name(),"points":[],"properties":{"color":(self.main.color[0],self.main.color[1],self.main.color[2]),"thickness":self.main.thickness,"fill":False}}
        ]
        self.main.current_layer=0
        self.main.current_object=0
        self.main.cursor_for_list_of_objects=0
    def navigate_button(self,button_name):
        if button_name=="select_button":
            self.select_button()
        elif button_name=="pen_button":
            self.pen_button()
        elif button_name=="eraser_button":
            self.eraser_button()
        elif button_name=="clear_layer_button":
            self.clear_layer_button()
        elif button_name=="clear_button":
            self.clear_button()
