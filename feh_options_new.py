import yaml 

class FehOptions():
    def __init__(self,path ="./defaults.yaml",verbose = True):
        # Variable for holding the options.
        self.the_options = None
        self.load_options(path)
        
        # Small verbose printer funciton
        self.verboseprint = print if verbose else lambda *a, **k: None

    def get_feh_command(self):

        command_list = []

        for key, option in self.the_options.items():
            # Check if the option has an argument that can be passed to feh
            if 'feh_arg' in option:               
                # Is the option active then add it to the command list
                if option['activated'] == True:
                    command_list.append(option['feh_arg'])        
                    self.verboseprint('Activate:   %s with the argument %s' % (key,option['feh_arg']))
                else:
                    self.verboseprint('Deactivate: %s with the argument %s' % (key,option['feh_arg']))

        return command_list
   

    def set_option(self,name,*arg):
        """Set an option to a specific value
        
        Arguments:
            name {str} -- Name must be in the set of options name given by the yaml options fil
            *arg {*arg} -- A key value list of options that shall be set.
        """

        if name in self.the_options:
            pass


    def load_options(self,path):
        with open(path, 'r', encoding='utf8') as stream:
            try:
                #load the yaml options file
                self.the_options = yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    
    def save_options(self,path):
        with open(path, 'w', encoding='utf8') as stream:
            try:
                # Write YAML file
                yaml.dump(self.the_options, stream, default_flow_style=False, allow_unicode=True)
            except yaml.YAMLError as exc:
                print(exc)
    
    def print_options(self):
        print ("The current options are:\n")
        print(self.the_options)

    def get_names(self):
        pass

if __name__ == "__main__":
    obj = FehOptions()
    print(obj.get_feh_command())
    obj.save_options('./test.yaml')