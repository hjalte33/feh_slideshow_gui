import yaml 
import warnings

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return '%s:%s: %s:%s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warning_on_one_line

class FehConfiguration():
    def __init__(self,path ="./defaults.yaml",verbose = True):
         # Small verbose printer funciton
        self.verboseprint = print if verbose else lambda *a, **k: None
        
        # Variable for holding the options.
        self.configuration = None
        self.load_configuration(path)   

    def set_option(self,name,activated,value=None):
        """Set an option to a specific value
        
        Arguments:
            name {str} -- Name must be in the set of options name 
                          given by the yaml configuration fil
            *arg {*arg} -- A list of options that shall be set.
        """
        try:
            option = self.configuration['options'][name]
            self.verboseprint('Setting option %s' % name)

            # Activated is a bool 
            option['activated'] = activated
            self.verboseprint('\tActivation: %s' % activated)

            # Value is none just pass
            if not value:
                pass
            # If value is string and if it's in list of legal values.   
            elif isinstance(value,str) and value in option['values']:
                # Set the feh sublementary argument to value
                option['feh_arg'][1] = value
                self.verboseprint("Sublementary argument: %s" % value)

            # If value is number and if list of leagal values contains number    
            elif isinstance(value,(float,int)):
                if any(isinstance(value,(float,int)) for item in option['values']):
                    
                    # Set the feh sublementary argument to value
                    option['feh_arg'][1] = value
                    self.verboseprint('Sublementary argument: %s' % value)
            else:
                # Warn the user that the value is not legal
                warnings.warn('The value %s does not seem to be a legal value. The legal values are %s' % (value,option['values']))
        
        except KeyError:
            warnings.warn("Option %s does not exit in the configuration or the option does not have a sublementary argument." %name)
            return


    def load_configuration(self,path):
        """Function to load a yaml file containing configuration for feh_slideshow.
        The function does not check for content, only syntax
        
        Arguments:
            path {str} -- Path to the yaml file
        """

        with open(path, 'r', encoding='utf8') as stream:
            try:
                #load the yaml configuration file
                self.configuration = yaml.load(stream)
                self.verboseprint("Successfully loaded configuration from %s " % path)
            
            except yaml.YAMLError as exc:
                # Warn the user if yaml failed to load
                warnings.warn("Faild to load configuration file from %s " % path)
                print(exc)
                
    def save_configuration(self,path):
        with open(path, 'w', encoding='utf8') as stream:
            try:
                # Write YAML file
                yaml.dump(self.configuration, stream, default_flow_style=False, allow_unicode=True)
            except yaml.YAMLError as exc:
                print(exc)
    
    def print_configuration(self):
        print ("The current configuration is:\n")
        print(self.configuration)

    def get_btn_key_names(self):
        """Get a list of all the keys to the options
        that can be changed with a button
        
        Returns:
            list -- list of keys
        """

        # Initialise empty key list
        key_names = []
        try:
            # Try to get the list from the settings file
            key_names = self.configuration['btn_selectables']
        
        # If no list is found, warn the user and return an emty list.
        except KeyError:
            warnings.warn("There is no list of button selectable in the configuration. Returning empty list.")
        
        return key_names

    def get_feh_command(self):
        """Collect all the active options and create a command
        that is ready to pass to a call command. 
        
        Returns:
            list -- Command list for a call function.
        """
        self.verboseprint('\n\nCreating command for feh\n')
        command = ['feh']

        # loop through all the options to find the ones with feh arguments
        for key, option in self.configuration['options'].items():        
            try:
                # Is the option active then add it to the command list
                # Print verbose messages if verbose is active
                if option['activated'] == True:
                    command.extend(option['feh_arg'])        
                    self.verboseprint('Activate:   %s with the argument %s' % (key,option['feh_arg']))
                else:
                    self.verboseprint('Deactivate: %s with the argument %s' % (key,option['feh_arg']))
            # If theres a key error inform the user that the acivated tag is missing
            except KeyError:
                warnings.warn("Error trying to set option %s. The option did'n seam to have an ativated tag in the yaml file" % key)
    
        try:
            # Retreave the path from the configuration
            path = self.configuration['path']['path']

            # Add the path the command list and print verbose messages if verbose is active.
            command.extend(path)
            self.verboseprint('Using path %s\n' % path)
        
        # If theres no path in the configuration
        except KeyError:
            # Insert a default path to the pictures folder and warn the user.
            command.extend(['~/Pictures'])
            warnings.warn("No path found in the configuration. Make sure that a path exists. I inserted the folder ~/Pictures as a temporary path for you")
    
        # Return the full feh command list readdy to pass to a call function.
        return command    
        

        

if __name__ == "__main__":
    obj = FehConfiguration()
    obj.set_option('zoom',True,'max')
    print(obj.get_feh_command())
    #obj.save_options('./test.yaml')