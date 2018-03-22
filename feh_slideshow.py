from collections import namedtuple
import tkinter as tk
import tkinter.filedialog
from subprocess import call
from feh_options import *

class App(tk.Frame):
    def __init__(self, master=None):
        self.options = FehOptions()
        self.path_name = ''
        super().__init__(master)
        self.pack()
        self.configure(padx = 5,pady = 5)
        self.check_btns = [] # a list that can hold a list of buttons for options.
        self.create_widgets()

    
    def create_widgets(self):
        #make the area where you select the path
        self.path_field = tk.Label(self, justify = "center", pady = 2, padx = 2)
        self.path_field.bind("<Button-1>", self.browse_func)
        self.path_field.pack(side="top")

        self.path_text = tk.Label(master = self.path_field, width = 30, bg = "white",relief = "sunken")
        self.path_text.configure(text = "Vælg en mappe", font = ["Helvetica",20], anchor="w", padx = 5 )
        self.path_text.bind("<Button-1>", self.browse_func)
        self.path_text.pack(side = "left")
        
        folder_icon = tk.PhotoImage(file = "./folderX45.gif")
        self.browse_icon = tk.Label(master = self.path_field, image = folder_icon)
        self.browse_icon.configure(width = 45, height = 45, anchor = "center")
        self.browse_icon.image = folder_icon  
        self.browse_icon.bind("<Button-1>", self.browse_func)
        self.browse_icon.pack(side="right")
        
        #make a field for the options buttons
        self.options_field = tk.Label(self, width = 40,bd = 2,relief='solid')
        self.options_field.pack(side="left")
        n = list(self.options.options.keys())
        n.sort()
        for key in n:
            if 'btn_selectable' in self.options.options[key].keys(): #if the item has the option to be selectable
                if self.options.options[key]['btn_selectable'] == True: #is selectable enabled?
                    self.check_btns.append(tk.Checkbutton(self.options_field, 
                                                        variable = self.options.options[key]['activated'], 
                                                        onvalue = True,
                                                        offvalue = False,
                                                        text = self.options.options[key]['lang_name'],
                                                        font = ["Helvetica",20]))
        for btn in self.check_btns:
            btn.pack(side = 'top', anchor = 'w')
        
        self.quit = tk.Button(self)
        self.quit["text"] = "Luk"
        self.quit["fg"] = "red"
        self.quit["font"] = ["Helvetica",20]
        self.quit["command"] = root.destroy
        self.quit.pack(side="bottom")
        
        self.start_btn = tk.Button(self)
        self.start_btn["text"] = "Start slideshow"
        self.start_btn["font"] = ["Helvetica",20]
        self.start_btn["command"] = self.start_slide
        self.start_btn.pack(side="bottom")

        self.delay_field = tk.Label(self,width = 40)
        self.delay_field.pack(side = 'bottom')

        self.delay_text = tk.Label(master = self.delay_field, text = "delay in sec.")
        self.delay_text.configure(font = ["Helvetica",20], padx = 5 )
        self.delay_text.pack(side = "left")

        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        vcmd = (self.register(self.validate_delay),'%d', '%s','%S','%V')
        self.delay_entry = tk.Entry(master = self.delay_field, width = 3,)
        self.delay_entry.configure(font = ["Helvetica",20])
        self.delay_entry.insert(0,'7')
        self.delay_entry.configure(validate = 'all',vcmd = vcmd)
        self.delay_entry.pack(side = 'right')
    
    def validate_delay(self,d,s,S,V):
        try:
            var = float(s+S)
            if V == 'focusout' and var < 3:  #if too small delay
                self.delay_entry.delete(0,'end') #delete the entry 
                self.delay_entry.insert(0,'3') #write 3 
                self.options.set_option(name = 'delay', data = 3) 
            if len(s) < 3 or d == '0': #if entry is short enough or a delete 
                if d == '0':
                    self.options.set_option(name = 'delay', data = s[:-1]) # return all but the last char
                else:
                    self.options.set_option(name = 'delay', data = var)       
                return True 
            
        except ValueError:
            return False
        return False


    def browse_func(self,*arg):
        self.path_field.focus_set()
        self.path_name = tk.filedialog.askdirectory(title='vælg en billedmappe',initialdir = '/home/pi/Pictures')
        self.path_name.rfind("/")
        
        self.path_text["text"] = self.path_name
        #self.pathlabel.config(text=filename)
    
    def start_slide(self):
        command = 'feh '+ self.options.get_feh_args()+' '+self.path_name
        command = command.split(' ')
        print(command)    
        call(command)

        
root = tk.Tk()
app = App(master=root)
app.mainloop()



