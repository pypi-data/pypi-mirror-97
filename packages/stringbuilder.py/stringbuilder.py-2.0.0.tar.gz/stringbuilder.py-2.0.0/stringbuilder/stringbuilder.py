import onetrick

def build(delim:str="") -> str:
    return lambda function: str.join(delim, map(str, function()))

@onetrick
class stringbuilder:
    def __init__(self, builder):
        self.builder = builder
    
    def __call__(self, delim:str=""):
        return build(delim=delim)(self.builder)