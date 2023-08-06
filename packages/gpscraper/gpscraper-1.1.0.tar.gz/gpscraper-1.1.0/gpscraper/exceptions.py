class InputTypeError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


class InputValueError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg