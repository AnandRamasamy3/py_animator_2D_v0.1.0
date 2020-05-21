import os,json,time
# import

class main_bar:
    def __init__(self,main,surface,database):
        self.main=main
        self.surface=surface
        self.undo_effectiveness=10
    def new_button(self):
        print ("got new button")
        self.main.total_time_strip=[]
        for ___ in range(100):
            self.main.total_time_strip.append([
                [
                    {"name":self.main.generate_new_object_name(),"points":[],"properties":{"color":(self.main.color[0],self.main.color[1],self.main.color[2]),"thickness":self.main.thickness,"fill":False}}
                ]
            ])
    def save_button(self):
        # print ("got save button")
        # print (os.getcwd())
        try:
            fobj=open("saved_items/main.json","w")#
            json.dump(self.main.total_time_strip,fobj)
            fobj.close()
            self.main.dialog_message=["successfully saved.          in the file named main.json into saved_items irectory",time.time()+3]
        except:
            self.main.dialog_message=["error on saving",time.time()+3]
    def open_button(self):
        # print ("got open button")
        try:
            f_obj=open("saved_items/main.json",)
            self.main.total_time_strip=json.load(f_obj)
            f_obj.close()
            self.main.dialog_message=["opened successfully",time.time()+3]
        except:
            self.main.dialog_message=["error on opening",time.time()+3]
            # print ("no files found.            ToTo avoid this error move your existing file to saved_items/ directory")
    def undo_button(self):
        # print ("got undo button")
        for ___ in range(10):
            try:
                self.main.undo.append(self.main.current_object["points"][-1])
                self.main.current_object["points"]=self.main.current_object["points"][:-1]
            except:
                pass
    def redo_button(self):
        # print ("got redo button")
        for ___ in range(self.undo_effectiveness):
            if self.main.undo!=[]:
                if self.main.undo[-1]!=None:
                    self.main.current_object["points"].append(self.main.undo[-1])
                    if len(self.main.undo)==1:
                        self.main.undo=[]
                    else:
                        self.main.undo=self.main.undo[:-1]
    def play_button(self):
        self.main.enable_play=True
        self.main.flag=self.main.layers
    def stop_button(self):
        self.main.enable_play=False
        self.main.layers=self.main.flag
    def navigate_button(self,button_name):
        if button_name=="new_button":
            self.new_button()
        elif button_name=="open_button":
            self.open_button()
        elif button_name=="save_button":
            self.save_button()
        elif button_name=="undo_button":
            self.undo_button()
        elif button_name=="redo_button":
            self.redo_button()
        elif button_name=="play_button":
            self.play_button()
        elif button_name=="stop_button":
            self.stop_button()
