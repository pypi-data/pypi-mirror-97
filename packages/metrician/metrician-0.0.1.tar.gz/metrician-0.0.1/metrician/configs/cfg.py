

class AutoDict(dict):
    """
        Allows for JS Object type interaction
        Recusrively sets attributes as a dictionary
    """
    def __init__(self,**kwargs):
        for k,v in kwargs.items():setattr(self,k,v if not isinstance(v, (dict) ) else AutoDict(**v) )
    

def DefaultCFG(AutoDict) -> AutoDict:

    def __init__(self,cfg : dict = {}) -> 'DefaultCFG':
        super(self,DefaultCFG).__init__( **cfg )
        self.validate_config(self)

    @staticmethod
    def validate_config(cls : DefaultCFG ) -> bool:
        """
            Iterate over config and validate data structure
        """
        pass
