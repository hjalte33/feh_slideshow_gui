from collections import namedtuple
import tkinter as tk
import tkinter.filedialog
from subprocess import call
from feh_options import FehOptions

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
        
        #put the options field on the left 
        self.options_field.pack(side="left")

        # options are dicts so the need to be sorted
        n = list(self.options.options.keys())
        n.sort()

        # go through the options and create the check box
        for key in n:
            
            #If the option is something that can on/off selectable 
            if 'btn_selectable' in self.options.options[key].keys(): 

                # the the selectability enabled
                if self.options.options[key]['btn_selectable'] == True:
                    
                    #create the button 
                    self.check_btns.append(tk.Checkbutton(self.options_field, 
                                                        variable = self.options.options[key]['activated'], 
                                                        onvalue = True,
                                                        offvalue = False,
                                                        text = self.options.options[key]['lang_name'],
                                                        font = ["Helvetica",20]))
        
        # pack all the button elements on top of each other and push them to the left
        for btn in self.check_btns:
            btn.pack(side = 'top', anchor = 'w')
        
        # make the quit button
        self.quit = tk.Button(self)
        self.quit["text"] = "Luk"
        self.quit["fg"] = "red"
        self.quit["font"] = ["Helvetica",20]
        self.quit["command"] = root.destroy
        self.quit.pack(side="bottom")
        
        # make the start slideshow button
        self.start_btn = tk.Button(self)
        self.start_btn["text"] = "Start slideshow"
        self.start_btn["font"] = ["Helvetica",20]
        self.start_btn["command"] = self.start_slide
        self.start_btn.pack(side="bottom")

        # container for the delay input and some text
        self.delay_field = tk.Label(self,width = 40)
        self.delay_field.pack(side = 'bottom')

        # make the text that says this is the input field for the delay
        self.delay_text = tk.Label(master = self.delay_field, text = "skiftetid i sek.")
        self.delay_text.configure(font = ["Helvetica",20], padx = 5 )
        self.delay_text.pack(side = "left")

        # This is the entry field for the delay. It is badly documented how the text validation works,
        # but the vcmd is a function that can carry the following information to the validation function.
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        vcmd = (self.register(self.validate_delay),'%d', '%s','%S','%V')

        # create the text entry field for the slideshow delay
        self.delay_entry = tk.Entry(master = self.delay_field, width = 3,)
        self.delay_entry.configure(font = ["Helvetica",20])
        self.delay_entry.insert(0,'7')
        # try to validate the input on all possible inputs ie focus in/out, key typed/deleted
        self.delay_entry.configure(validate = 'all',vcmd = vcmd)
        self.delay_entry.pack(side = 'right')
    
    def validate_delay(self,d,s,S,V):
        """Text validation function for the slideshow delay entry field
            it makes sure that onyl numbers are typed and it does not go
            less then 3 sec and more than 999 sec.
        
        Arguments:
            d {str} -- %d = Type of action (1=insert, 0=delete, -1 for others)
            s {str} -- %s = value of entry prior to editing
            S {str} -- %S = the text string being inserted or deleted, if any
            V {str} -- %V = the type of validation that triggered the callback
                         (key, focusin, focusout, forced)

        
        Returns:
             bool -- is the input valid
        """

        try:
            # Value prior to editing + the inserted char.
            # Try to convert it to a float
            # if it cannot convert to float the input cannot be a number
            # if error the function returns false
            var = float(s+S)

            # If the user focus away from the textfield check that the value is smaller than 3
            if V == 'focusout' and var < 3:
                # If smaller delet the entry and write 3 for 3 sec
                self.delay_entry.delete(0,'end')    #delete the entry 
                self.delay_entry.insert(0,'3')      #write 3
                # Also update the option so it matches the input
                self.options.set_option(name = 'delay', data = 3) 

            # if the entry is less than 3 char or if user delets a char   
            if len(s) < 3 or d == '0': 
                
                # if deleting a char
                if d == '0':
                    # Update the option with the current typed in value minus the
                    # last char becaus it's gonna be deleted.
                    self.options.set_option(name = 'delay', data = s[:-1])
                
                # Else if the a char is inserted
                else:
                    # Update the option with the calculated float var
                    self.options.set_option(name = 'delay', data = var)  

                # Return true becaus it was a valid input because it could be 
                # converted to a char and it was less than 3 or a delet char
                return True 
            
        except ValueError:
            # Return false because the input could not be converted to a float
            return False

        # If the function didn't return true anywhere it must have been a false input.     
        return False


    def browse_func(self,*arg):
        """ Function that start the browsing of a folder
        """
        #set the path field as focus (may not be neccessary)
        self.path_field.focus_set()

        # set the pathname
        self.path_name = tk.filedialog.askdirectory(title='vælg en billedmappe',initialdir = '/home/pi/Pictures')
        
        # find the folder name and display it (not implemented yet)
        # self.path_name.rfind("/")
        
        # set the text of the path text box to the current path
        self.path_text["text"] = self.path_name

    
    def start_slide(self):
        """Function that starts feh with the commands contained in self
        """
        #put the command together 
        command = 'feh '+ self.options.get_feh_args()+','+self.path_name
        
        #split list at all the commas so it is a list of lists and call the command
        command = command.split(',')
        call(command)
        # print for debugging
        print(command)

# create a root element for tkinter        
root = tk.Tk()

# create an instance of App class
app = App(master=root)

# Start the application
app.mainloop()



