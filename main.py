import pygame,sys,math,random,os,threading,socket,json,time
from pygame.locals import *
from src.buttons.main_bar import *
from src.buttons.tools_box import *
import numpy as np

pygame.init()
WIDTH,HEIGHT=1100,600
surface=pygame.display.set_mode((WIDTH,HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption("animator v0.1.0")

font=pygame.font.SysFont('Calibri',17,bold=True,italic=False)
sub_font=pygame.font.SysFont('Arial',12,bold=True,italic=False)

# -------------- colors
f_obj=open("src/config/colors.json",)
colors=json.load(f_obj)
f_obj.close()
# -------------- layout
f_obj=open("src/config/layout.json",)
layout=json.load(f_obj)
f_obj.close()
# -------------- layout
f_obj=open("src/config/buttons.json",)
buttons=json.load(f_obj)
# print (buttons)
f_obj.close()

database={"colors":colors,"layout":layout,"buttons":buttons}

# print (database)

# temp_font=pygame.font.SysFont('Calibri',31,bold=True,italic=False)
# object_name_text_bottom=temp_font.render("_",False,self.colors["black"])
# surface.blit(object_name_text_bottom,(x+width-25+5,y-3))

class main:
    def __init__(self,surface,database):
        self.surface=surface
        self.database=database
        self.colors=database["colors"]
        self.layout=database["layout"]
        self.buttons=database["buttons"]
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.time_strip_unit=0.1
        self.last_clicked=time.time()
        self.color=[0,0,0]
        self.thickness=3
        self.shape_fill_x=30
        self.shape_fill_y=120
        self.shape_fill_radius=10
        self.undo=[]
        self.time_strip_duration=100
        self.total_time_strip=[]
        for ___ in range(100):
            self.total_time_strip.append([
                [
                    {"name":self.generate_new_object_name(),"points":[],"properties":{"color":(self.color[0],self.color[1],self.color[2]),"thickness":self.thickness,"fill":False}}
                ]
            ])
        # print (self.current_object["properties"]["color"])
        self.layers=0
        self.current_layer=0
        self.current_object=0
        self.cursor_for_list_of_objects=0
        self.cursor_for_list_of_layers=0
        self.add_layer_button_x=[0,0,0,0]
        self.current_tool="pen_button"
        self.eraser_radius=10
        self.enable_play=False
        self.flag=0
        self.dialog_message=["",time.time()+0]
    def generate_new_object_name(self):
        return "o_"+str(int(time.time()))
    def generate_new_layer_name(self):
        return "l_"+str(int(time.time()))
    def manage_clicks(self,frame,button_name):
        if frame=="main_bar":
            bar=main_bar(self,self.surface,self.database)
            bar.navigate_button(button_name)
        elif frame=="tools_box":
            bar=tools_box(self,self.surface,self.database)
            bar.navigate_button(button_name)
    def onclick_button(self):
        if self.click[0]==1 and time.time()>=self.last_clicked+0.5:
            self.last_clicked=time.time()
            for frame in self.buttons:
                for button_name in self.buttons[frame]:
                    if self.buttons[frame][button_name]["x"]<=self.mouse[0]<=self.buttons[frame][button_name]["x"]+self.buttons[frame][button_name]["width"] and self.buttons[frame][button_name]["y"]<=self.mouse[1]<=self.buttons[frame][button_name]["y"]+self.buttons[frame][button_name]["height"]:
                        self.manage_clicks(frame,button_name)
            # check list of objects
            x,y,width,height=self.layout["objects"]["x"],self.layout["objects"]["y"],self.layout["objects"]["width"],self.layout["objects"]["height"]
            if x+25<=self.mouse[0]<=x+25+width-50 and y+9<=self.mouse[1]<=y+9+49:
                pass
                # print ("up click")
                # print (self.cursor_for_list_of_objects)
                if len(self.total_time_strip[self.layers][self.current_layer])>0:
                    self.current_object=self.cursor_for_list_of_objects
                    self.color=[self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][0],self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][1],self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][2]]
                    self.thickness=self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["thickness"]
                else:
                    self.total_time_strip[self.layers][self.current_layer].append({"name":self.generate_new_object_name(),"points":[],"properties":{"color":(self.color[0],self.color[1],self.color[2]),"thickness":self.thickness}})
            elif x+25<=self.mouse[0]<=x+25+width-50 and y+67<=self.mouse[1]<=y+67+49:
                pass
                # print ("down click")
                # print (self.cursor_for_list_of_objects)
                if len(self.total_time_strip[self.layers][self.current_layer])>0:
                    self.current_object=self.cursor_for_list_of_objects+1
                    if self.current_object>len(self.total_time_strip[self.layers][self.current_layer])-1:
                        self.total_time_strip[self.layers][self.current_layer].append({"name":self.generate_new_object_name(),"points":[],"properties":{"color":(self.color[0],self.color[1],self.color[2]),"thickness":self.thickness,"fill":False}})
                    self.color=[self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][0],self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][1],self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"][2]]
                    self.thickness=self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["thickness"]
            elif x+25+width-50<=self.mouse[0]<=x+25+width and y<=self.mouse[1]<=y+(height//2):
                self.cursor_for_list_of_objects-=1
                if self.cursor_for_list_of_objects<0:
                    self.cursor_for_list_of_objects=0
                # print ("ups",self.cursor_for_list_of_objects)
            elif x+25+width-50<=self.mouse[0]<=x+25+width and y+(height//2)+1<=self.mouse[1]<=y+height:
                self.cursor_for_list_of_objects+=1
                if self.cursor_for_list_of_objects>len(self.total_time_strip[self.layers][self.current_layer])-1:
                    self.cursor_for_list_of_objects=len(self.total_time_strip[self.layers][self.current_layer])-1
                # print ("downs",self.cursor_for_list_of_objects)
            if self.add_layer_button_x[0]<=self.mouse[0]<=self.add_layer_button_x[1] and self.add_layer_button_x[2]<=self.mouse[1]<=self.add_layer_button_x[3]:
                # print ("ooops")
                self.total_time_strip[self.layers].append([
                    {"name":self.generate_new_object_name(),"points":[],"properties":{"color":(self.color[0],self.color[1],self.color[2]),"thickness":self.thickness,"fill":True}}
                ])
                self.current_layer=len(self.total_time_strip[self.layers])-1
                self.current_object=0
                self.cursor_for_list_of_objects=0
            # print ("got here")
            x,y,width,height=self.layout["properties_box"]["x"],self.layout["properties_box"]["y"],self.layout["properties_box"]["width"],self.layout["properties_box"]["height"]
            # print (x,self.mouse[0],x+width,y,self.mouse[1],y+height)
            # print (x+self.shape_fill_x<=self.mouse[0]<=x+self.shape_fill_x+self.shape_fill_radius*2,y+self.shape_fill_y<=self.mouse[1]<=y+self.shape_fill_y+self.shape_fill_radius*2)
            if x+self.shape_fill_x<=self.mouse[0]<=x+self.shape_fill_x+self.shape_fill_radius*2 and y+self.shape_fill_y<=self.mouse[1]<=y+self.shape_fill_y+self.shape_fill_radius*2:
                # print ("ooops")
                try:
                    if self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["fill"]:
                        self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["fill"]=False
                    else:
                        self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["fill"]=True
                except:
                    pass
    def draw_gradient(self,X,Y,width,height,color_1,color_2):
        self.unit=[]
        for index in range(3):
            self.unit.append((color_2[index]-color_1[index])/width)
        for x in range(width):
            for y in range(height):
                color=[]
                for index in range(3):
                    color.append(int((color_1[index]+x*self.unit[index])))
                self.surface.set_at((X+x,Y+y),color)
    def draw_on_canvas(self):
        if self.layers>=1:
            # print (self.layers-1)
            for layer in self.total_time_strip[self.layers-1]:
                for object in layer:
                    if len(object["points"])>0:
                        color=[object["properties"]["color"][0],object["properties"]["color"][1],object["properties"]["color"][2],100]
                        if object["properties"]["fill"] and len(object["points"])>2:
                            pygame.draw.polygon(self.surface,color,object["points"])
                        else:
                            for point in range(0,len(object["points"])-1):
                                # print (color)
                                pygame.draw.line(self.surface,color,(object["points"][point][0],object["points"][point][1]),(object["points"][point+1][0],object["points"][point+1][1]),object["properties"]["thickness"])
                            # print ("hahahahaha")
        for layer in self.total_time_strip[self.layers]:
            for object in layer:
                if len(object["points"])>0:
                    if object["properties"]["fill"] and len(object["points"])>2:
                        pygame.draw.polygon(self.surface,object["properties"]["color"],object["points"])
                    else:
                        for point in range(0,len(object["points"])-1):
                            pygame.draw.line(self.surface,object["properties"]["color"],(object["points"][point][0],object["points"][point][1]),(object["points"][point+1][0],object["points"][point+1][1]),object["properties"]["thickness"])
                        # print ("hahahahaha")
    def get_points_from_mouse_for_canvas(self):
        if self.click[0]==1 and self.current_tool=="pen_button":
            if self.layout["canvas"]["x"]<=self.mouse[0]<=self.layout["canvas"]["x"]+self.layout["canvas"]["width"] and self.layout["canvas"]["y"]<=self.mouse[1]<=self.layout["canvas"]["y"]+self.layout["canvas"]["height"]:
                try:
                    # print (self.total_time_strip[self.layers],self.current_layer,self.current_object)
                    self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"].append(self.mouse)
                except:
                    pass
    def draw_properties_box(self):
        if self.current_tool=="pen_button":
            x,y,width,height=self.layout["properties_box"]["x"],self.layout["properties_box"]["y"],self.layout["properties_box"]["width"],self.layout["properties_box"]["height"]
            # shape fill
            temp_font=pygame.font.SysFont('Calibri',19,bold=False,italic=False)
            object_name_text_bottom=temp_font.render("Shape Fill",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+self.shape_fill_x-10,y+self.shape_fill_y-20))
            pygame.draw.rect(self.surface,self.colors["black"],(x+self.shape_fill_x,y+self.shape_fill_y,self.shape_fill_radius*2,self.shape_fill_radius*2),2)
            try:
                if self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["fill"]:
                    pygame.draw.circle(self.surface,self.colors["black"],(x+self.shape_fill_x+self.shape_fill_radius,y+self.shape_fill_y+self.shape_fill_radius),self.shape_fill_radius)
            except:
                pass
            # thickness bar
            thickness_bar_x,thickness_bar_y=30,180
            distance=100
            temp_font=pygame.font.SysFont('Calibri',19,bold=False,italic=False)
            object_name_text_bottom=temp_font.render("Thickness",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+thickness_bar_x-10,y+thickness_bar_y-20))
            pygame.draw.line(self.surface,self.colors["black"],(x+thickness_bar_x,y+thickness_bar_y),(x+thickness_bar_x+distance,y+thickness_bar_y),2)
            if self.click[0]==1:
                if x+thickness_bar_x<=self.mouse[0]<=self.layout["properties_box"]["x"]+thickness_bar_x+distance and self.layout["properties_box"]["y"]+thickness_bar_y-1<=self.mouse[1]<=self.layout["properties_box"]["y"]+thickness_bar_y+1:
                    self.thickness=self.mouse[0]-(x+thickness_bar_x)
            pygame.draw.circle(self.surface,self.colors["black"],(x+thickness_bar_x+self.thickness,y+thickness_bar_y),5)
            try:
                self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["thickness"]=self.thickness
            except:
                pass
        elif self.current_tool=="eraser_button":
            pass
            # print ("hahahahaha")
            x1,y1,x2,y2=self.mouse[0]-self.eraser_radius//2,self.mouse[1]-self.eraser_radius//2,self.mouse[0]+self.eraser_radius//2,self.mouse[1]+self.eraser_radius//2
            if self.click[0]==1:
                for x in range(x1,x2):
                    for y in range(y1,y2):
                        point=(x,y)
                        # print (point,self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"])
                        # print (self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"])
                        if point in self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"]:
                            # print ("hahahahaha",time.time())
                            self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"].remove(point)
    def draw_color_palette(self):
        thick=10
        distance=110
        unit=distance/255
        self.draw_gradient(self.layout["color_palette"]["x"]+20,self.layout["color_palette"]["y"]+20,distance,thick,(0,0,0),(255,0,0))
        self.draw_gradient(self.layout["color_palette"]["x"]+20,self.layout["color_palette"]["y"]+40,distance,thick,(0,0,0),(0,255,0))
        self.draw_gradient(self.layout["color_palette"]["x"]+20,self.layout["color_palette"]["y"]+60,distance,thick,(0,0,0),(0,0,255))
        height_of_pointer=6
        red_X=self.layout["color_palette"]["x"]+20+(self.color[0]/255)*distance
        pygame.draw.rect(self.surface,self.colors["black"],(red_X,self.layout["color_palette"]["y"]+20-height_of_pointer,1,height_of_pointer))
        green_X=self.layout["color_palette"]["x"]+20+(self.color[1]/255)*distance
        pygame.draw.rect(self.surface,self.colors["black"],(green_X,self.layout["color_palette"]["y"]+40-height_of_pointer,1,height_of_pointer))
        blue_X=self.layout["color_palette"]["x"]+20+(self.color[2]/255)*distance
        pygame.draw.rect(self.surface,self.colors["black"],(blue_X,self.layout["color_palette"]["y"]+60-height_of_pointer,1,height_of_pointer))
        if self.click[0]==1:
            if self.layout["color_palette"]["x"]+20<=self.mouse[0]<=self.layout["color_palette"]["x"]+self.layout["color_palette"]["width"]-20:
                if self.layout["color_palette"]["y"]+20-thick/2<=self.mouse[1]<=self.layout["color_palette"]["y"]+20+thick/2:
                    self.color[0]=int(((self.mouse[0]-self.layout["color_palette"]["x"]-20)/distance)*255)
                elif self.layout["color_palette"]["y"]+40-thick/2<=self.mouse[1]<=self.layout["color_palette"]["y"]+40+thick/2:
                    self.color[1]=int(((self.mouse[0]-self.layout["color_palette"]["x"]-20)/distance)*255)
                elif self.layout["color_palette"]["y"]+60-thick/2<=self.mouse[1]<=self.layout["color_palette"]["y"]+60+thick/2:
                    self.color[2]=int(((self.mouse[0]-self.layout["color_palette"]["x"]-20)/distance)*255)
        pygame.draw.rect(self.surface,self.color,(self.layout["color_palette"]["x"]+30,self.layout["color_palette"]["y"]+100,60,20))
        pygame.draw.rect(self.surface,self.colors["black"],(self.layout["color_palette"]["x"]+30,self.layout["color_palette"]["y"]+100,60,20),1)
        try:
            self.total_time_strip[self.layers][self.current_layer][self.current_object]["properties"]["color"]=(self.color[0],self.color[1],self.color[2])
        except:
            pass
    def draw_objects_list_menu(self):
        x_adjust,y_adjust=50,20
        x,y,width,height=self.layout["objects"]["x"],self.layout["objects"]["y"],self.layout["objects"]["width"],self.layout["objects"]["height"]
        try:
            if len(self.total_time_strip[self.layers][self.current_layer])>0:
                # print (x,y,width,height)
                # first text
                temp_font=pygame.font.SysFont('Calibri',21,bold=False,italic=False)
                # print (self.cursor_for_list_of_objects)
                # if self.cursor_for_list_of_objects<len(self.total_time_strip[self.layers][self.current_layer]):
                object_name_text_bottom=temp_font.render(self.total_time_strip[self.layers][self.current_layer][self.cursor_for_list_of_objects]["name"],False,self.colors["black"])
                surface.blit(object_name_text_bottom,(x+25+x_adjust,y+y_adjust))
                # second text
                # print ("hahahahaha")
                try:
                    temp_font=pygame.font.SysFont('Calibri',21,bold=False,italic=False)
                    object_name_text_bottom=temp_font.render(self.total_time_strip[self.layers][self.current_layer][self.cursor_for_list_of_objects+1]["name"],False,self.colors["black"])
                except:
                    temp_font=pygame.font.SysFont('Calibri',31,bold=True,italic=False)
                    object_name_text_bottom=temp_font.render("+",False,self.colors["black"])
                surface.blit(object_name_text_bottom,(x+25+x_adjust,y+y_adjust+58))
                # print (x+width-25+5,y-3)
                # right plain white box
                pygame.draw.rect(self.surface,self.colors["white"],(x+width-25,y+1,25-1,height-2))
                # first box check current
                if self.current_object==self.cursor_for_list_of_objects:
                    pygame.draw.rect(self.surface,self.colors["black"],(x+25+49,y+9,width-50-49,49))
                    temp_font=pygame.font.SysFont('Calibri',20,bold=True,italic=False)
                    object_name_text_bottom=temp_font.render(self.total_time_strip[self.layers][self.current_layer][self.cursor_for_list_of_objects]["name"],False,self.colors["white"])
                    surface.blit(object_name_text_bottom,(x+25+x_adjust,y+y_adjust))
                # first box draw full outline box
                pygame.draw.rect(self.surface,self.colors["black"],(x+25,y+9,width-50,49),1)
                # second box check current
                if self.current_object==self.cursor_for_list_of_objects+1:
                    pygame.draw.rect(self.surface,self.colors["black"],(x+25+49,y+67,width-50-49,49))
                    temp_font=pygame.font.SysFont('Calibri',20,bold=True,italic=False)
                    object_name_text_bottom=temp_font.render(self.total_time_strip[self.layers][self.current_layer][self.cursor_for_list_of_objects+1]["name"],False,self.colors["white"])
                    surface.blit(object_name_text_bottom,(x+25+x_adjust,y+y_adjust+58))
                # second box draw full outline box
                pygame.draw.rect(self.surface,self.colors["black"],(x+25,y+67,width-50,49),1)
                # up text _
                # if #
                # print (round(time.time(),2),round(self.last_clicked+0.5,2),self.click[0]==1,time.time()>=self.last_clicked+0.5)
                # print (self.click[0]==1,time.time()>=self.last_clicked+0.5)
                # for object in self.current_layer:
                #     # print (object["name"])
                #     print (self.current_object["name"],object["name"],len(object["points"]))
            else:
                pygame.draw.rect(self.surface,self.colors["black"],(x+25,y+9,width-50,49),1)
                temp_font=pygame.font.SysFont('Calibri',31,bold=True,italic=False)
                object_name_text_bottom=temp_font.render("+",False,self.colors["black"])
                surface.blit(object_name_text_bottom,(x+25+x_adjust,y+y_adjust))
            temp_font=pygame.font.SysFont('Calibri',31,bold=True,italic=False)
            object_name_text_bottom=temp_font.render("_",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+width-25+5,y-3))
            # up text |
            object_name_text_bottom=temp_font.render("|",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+width-25+8,y+15))
            # down text _
            object_name_text_bottom=temp_font.render("_",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+width-25+5,y+9+71))
            # down text |
            object_name_text_bottom=temp_font.render("|",False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+width-25+8,y+9+70))
        except:
            pass
    def draw_layers_control_box(self):
        pass
        x,y,width,height=self.layout["layers"]["x"],self.layout["layers"]["y"],self.layout["layers"]["width"],self.layout["layers"]["height"]
        unit_width=width//(len(self.total_time_strip[self.layers])+1)
        self.add_layer_button_x=[x+width-unit_width,x+width,y+height-20,y+height]
        # print (unit_width)
        for x_ in range(len(self.total_time_strip[self.layers])):
            temp_font=pygame.font.SysFont('Calibri',20,bold=True,italic=False)
            object_name_text_bottom=temp_font.render(chr(x_+97),False,self.colors["black"])
            surface.blit(object_name_text_bottom,(x+x_*unit_width+3,y+height-20+2))
            # check current
            # print (self.layers,x_)
            if self.current_layer==x_:
                pygame.draw.rect(self.surface,self.colors["black"],(x+x_*unit_width,y+height-20,unit_width,20))
                temp_font=pygame.font.SysFont('Calibri',20,bold=True,italic=False)
                object_name_text_bottom=temp_font.render(chr(x_+97),False,self.colors["white"])
                surface.blit(object_name_text_bottom,(x+x_*unit_width+3,y+height-20+2))
            # draw full outline box
            pygame.draw.rect(self.surface,self.colors["black"],(x+x_*unit_width,y+height-20,unit_width,20),1)
        pygame.draw.rect(self.surface,self.colors["black"],(x+x_*unit_width,y+height-20,(x+width)-(x+x_*unit_width),20),1)
        temp_font=pygame.font.SysFont('Calibri',38,bold=True,italic=False)
        object_name_text_bottom=temp_font.render("+",False,self.colors["black"])
        # print (unit_width)
        surface.blit(object_name_text_bottom,(x+width-unit_width-3,y+height-26))
        if self.click[0]==1:
            if x<=self.mouse[0]<=x+width and y+height-20<=self.mouse[1]<=y+height:
                length=(self.mouse[0]-x)//unit_width
                # print (length)
                if length<=len(self.total_time_strip[self.layers])-1:
                    self.current_layer=length
                    self.current_object=0
                    # print (self.total_time_strip[self.layers][self.current_layer][-1]["properties"]["color"])
                    self.color[0],self.color[1],self.color[2]=self.total_time_strip[self.layers][self.current_layer][-1]["properties"]["color"][0],self.total_time_strip[self.layers][self.current_layer][-1]["properties"]["color"][1],self.total_time_strip[self.layers][self.current_layer][-1]["properties"]["color"][2]
    def draw_layout(self):
        # drawing boxes
        for box in self.layout:
            if box!="canvas":
                pygame.draw.rect(self.surface,self.colors["white"],(self.layout[box]["x"],self.layout[box]["y"],self.layout[box]["width"],self.layout[box]["height"]))
            pygame.draw.rect(self.surface,self.colors["black"],(self.layout[box]["x"],self.layout[box]["y"],self.layout[box]["width"],self.layout[box]["height"]),1)
        # drawing buttons
        for box in self.buttons:
            for button in self.buttons[box]:
                pygame.draw.rect(self.surface,self.colors["black"],(self.buttons[box][button]["x"],self.buttons[box][button]["y"],self.buttons[box][button]["width"],self.buttons[box][button]["height"]),1)
                button_text=font.render(self.buttons[box][button]["text"],False,self.colors["black"])
                surface.blit(button_text,(self.buttons[box][button]["x"]+2,self.buttons[box][button]["y"]+2))
    def draw_eraser_cursor(self):
        # print ("ooops",self.current_tool,self.current_tool=="eraser_button")
        if self.current_tool=="eraser_button":
            # self.mouse=pygame.mouse.get_pos()
            if self.layout["canvas"]["x"]<=self.mouse[0]<=self.layout["canvas"]["x"]+self.layout["canvas"]["width"] and self.layout["canvas"]["y"]<=self.mouse[1]<=self.layout["canvas"]["y"]+self.layout["canvas"]["height"]:
                pygame.draw.rect(self.surface,self.colors["black"],(self.mouse[0]-self.eraser_radius//2,self.mouse[1]-self.eraser_radius//2,self.eraser_radius,self.eraser_radius),1)
        #
    def set_buttons_for_time_strip(self):
        # print (self.layout)
        # print (self.buttons)
        x,y,width,height=self.layout["time_strip"]["x"],self.layout["time_strip"]["y"],self.layout["time_strip"]["width"],self.layout["time_strip"]["height"]
        x+=20
        unit_width=(width-20-20)/self.time_strip_duration
        # print (unit_width)
        for index_time in range(self.time_strip_duration):
            # pass
            # print (index_time*unit_width)
            # print (x+index_time*unit_width,y+10,self.mouse)
            # pygame.draw.rect(self.surface,self.colors["black"],(x+index_time*unit_width,y+10,unit_width,20),1)
            self.buttons["time_strip"].update({
                index_time:{
                    "text":"",
                    "x":x+index_time*unit_width,
                    "y":y+10,
                    "width":unit_width,
                    "height":20
                }
            })
    def time_strip_bar(self):
        pass
        # print (self.buttons["time_strip"])
        for button in self.buttons["time_strip"]:
            # print (self.buttons["time_strip"][button])
            if button==self.layers:
                # current time strip
                pygame.draw.rect(self.surface,self.colors["black"],(self.buttons["time_strip"][button]["x"],self.buttons["time_strip"][button]["y"],self.buttons["time_strip"][button]["width"],self.buttons["time_strip"][button]["height"]))
                # print (button)
            pygame.draw.rect(self.surface,self.colors["black"],(self.buttons["time_strip"][button]["x"],self.buttons["time_strip"][button]["y"],self.buttons["time_strip"][button]["width"],self.buttons["time_strip"][button]["height"]),1)
            if self.click[0]==1:
                if self.buttons["time_strip"][button]["x"]<=self.mouse[0]<=self.buttons["time_strip"][button]["x"]+self.buttons["time_strip"][button]["width"] and self.buttons["time_strip"][button]["y"]<=self.mouse[1]<=self.buttons["time_strip"][button]["y"]+self.buttons["time_strip"][button]["height"]:
                    # print (button)
                    self.layers=button
                    self.current_layer=0
                    self.current_object=0
                    self.cursor_for_list_of_objects=0
                    self.cursor_for_list_of_layers=0
                    self.current_tool="pen_button"
    def play_animation(self):
        if self.enable_play:
            self.layers+=1
            if self.layers>=len(self.total_time_strip)-1:
                self.layers=0
    def get_apt_message(self,message):
    	result=[""]
    	length=40
    	message=message.split(" ",)
    	while len(message)>0:
    		if len(result[-1])<length:
    			if (len(result[-1])+len(message[0]))<length:
    				result[-1]+=" "+message[0]
    				message.remove(message[0])
    			elif len(result[-1])<(length/2):
    				rem_length=length-len(result[-1])-1
    				result[-1]+=" "+message[0][0:rem_length]
    				message[0]=message[0].replace(message[0][0:rem_length],"")
    			else:
    				result.append("")
    		else:
    			result.append("")
    	return result
    def draw_dialog_box(self):
        if self.dialog_message[1]>=time.time():
            message=self.get_apt_message(self.dialog_message[0])
            # print (message)
            height=10
            for ___ in range(len(message)):
                height+=15
            height+=10
            x=(WIDTH//2)-(300//2)
            y=(HEIGHT//2)-(height//2)
            pygame.draw.rect(self.surface,self.colors["white"],(x,y,300,height))
            pygame.draw.rect(self.surface,self.colors["black"],(x,y,300,height),1)
            y_for_line=y+10
            for line in message:
                temp_font=pygame.font.SysFont('Calibri',20,bold=False,italic=False)
                object_name_text_bottom=temp_font.render(line,False,self.colors["black"])
                surface.blit(object_name_text_bottom,(x+10,y_for_line))
                y_for_line+=17
            # self.dialog_message[1]+=1
            pass
        else:
            self.dialog_message[0]=""
    def run(self):
        app_runnable=True
        self.set_buttons_for_time_strip()
        # temp=self.
        play_index=0
        while app_runnable:
            self.surface.fill(self.colors["white"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            # print (self.mouse)
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_SPACE:
                        pass
                        app_runnable=False
                    if event.key==K_F10:
                        app_runnable=False
                    if event.key==K_LEFT:
                        pass
                    if event.key==K_RIGHT:
                        pass
            self.draw_on_canvas()
            self.draw_layout()
            self.draw_color_palette()
            self.draw_objects_list_menu()
            self.draw_layers_control_box()
            self.draw_properties_box()
            self.draw_eraser_cursor()
            # print (self.total_time_strip[self.layers][self.current_layer],self.layers,self.current_layer,self.current_object)
            self.time_strip_bar()
            if len(self.dialog_message[0])>0:
                self.draw_dialog_box()
                # print ("hahahahaha",self.dialog_message)
            else:
                self.get_points_from_mouse_for_canvas()
                self.onclick_button()
                self.play_animation()
            # print (self.dialog_message)
            pygame.display.update()
            ft.tick(fps)
            # print (self.layers)
            # print (self.total_time_strip[self.layers][self.current_layer][self.current_object])
            # print (len(self.total_time_strip[self.layers][self.current_layer][self.current_object]["points"]))
            # break




if __name__=="__main__":
    app=main(surface,database)
    app.run()

# print (len(str(int(time.time()))))

#
