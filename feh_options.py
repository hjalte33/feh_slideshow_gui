#This class holds options for the slideshow 
from tkinter import BooleanVar


class FehOptions(object):
    def __init__(self):
        self.options = {}
        self._delay = 7
        # Automatically rotate images based on EXIF data. Does not alter the image files.
        self.options['auto rotate'] = {'lang_name':'auto rotering', 'activated':BooleanVar(value=True),'btn_selectable':True,'feh_arg':'--auto-rotate'}
        # Zoom pictures to screen size in fullscreen / fixed geometry mode.      
        self.options['zoom'] = {'lang_name':'fyld skærm','activated':BooleanVar(value=True),'btn_selectable':True,'feh_arg':'--zoom fill'}
        self.options['auto_zoom'] = {'lang_name':'auto zoom','activated':BooleanVar(value=False),'btn_selectable':True,'feh_arg':'--auto-zoom'}
        # Create borderless windows.         
        self.options['borderless'] = {'lang_name':'uden kant','activated':BooleanVar(value=True),'btn_selectable':False,'feh_arg':'--borderless'}
        # Make the window fullscreen. Note that in this mode, large images will always be scaled down to fit the screen, --zoom zoom only affects smaller images and never scales larger than necessary to fit the screen size. The only exception is a zoom of 100, in which case images will always be shown at 100% zoom, no matter their dimensions.
        self.options['full_screen'] = {'lang_name':'fuld skærm','activated':BooleanVar(value=True),'btn_selectable':False,'feh_arg':'--fullscreen'}
        # Hide the pointer (useful for slideshows).
        self.options['hide_pointer'] = {'lang_name':'skjul mus','activated':BooleanVar(value=True),'btn_selectable':True,'feh_arg':'--hide-pointer'}     
        # When viewing multiple files in a slideshow, randomize the file list before displaying. The list is re-randomized whenever the slideshow cycles (that is, transitions from last to first image).
        self.options['randomise'] = {'lang_name':'tilfældig','activated':BooleanVar(value=False),'btn_selectable':True,'feh_arg':'--randomize'}                
        # Recursively expand any directories in the commandline arguments to the content of those directories, all the way down to the bottom level.
        self.options['recursive'] = {'lang_name':'rekursive','activated':BooleanVar(value=True),'btn_selectable':True,'feh_arg':'--recursive'}               
        # Reload filelist and current image after int seconds. Useful for viewing HTTP webcams or frequently changing directories. (Note that the filelist reloading is still experimental.)
        self.options['reload_folder'] = {'lang_name':'auto genindlæs','activated':BooleanVar(value=False),'btn_selectable':False,'feh_arg':'--reload'}                 
        # Reverse the sort order. Use this to invert the order of the filelist. E.g. to sort in reverse width order, use -nSwidth.
        self.options['reverse'] = {'lang_name':'baglæns','activated':BooleanVar(value=False),'btn_selectable':True,'feh_arg':'--reverse'}                 
        # float For slideshow mode, wait float seconds between automatically changing slides. Useful for presentations. Specify a negative number to set the delay (which will then be float * (-1)), but start feh in paused mode.
        # feh_arg as a comma because options are split at commas.
        self.options['delay'] = {'lang_name':'forsinkelse', 'feh_arg':lambda:'--slideshow-delay,'+ str(self._delay)}
        
    def get_feh_args (self):
        output = ''
        flag = False
        for val in self.options.values():
            if 'activated' in val and val['activated'].get() == True:  # using short circuit evaluation to first check if activated is even in the list. 
                output += (val['feh_arg'])
                output += ','
        output += self.options['delay']['feh_arg']()      
        return(output)

    def set_option (self,name,data):
        if name == 'delay': 
            try:
                self._delay = float(data)
                print(self._delay)
            except ValueError:
                print('set option delay went wrong')
                return
        elif isinstance(data,bool):
            try:
                self.options[name]['activated'].set(str(data))
            except KeyError:
                return
