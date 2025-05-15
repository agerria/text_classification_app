
class BaseTraslator:
    def __init__(self, path, text_column, class_column=None):
        self.path = path
        self.text_column = text_column
        self.class_column = class_column
        
        self.texts = None
        self.classes = None
    
    
    def load_data(self):
        raise NotImplemented