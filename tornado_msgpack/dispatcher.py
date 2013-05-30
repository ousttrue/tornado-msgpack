class Dispatcher(object):

    def __init__(self):
        self.method_map={}

    def add_handler(self, name, method):
        self.method_map[name]=method

