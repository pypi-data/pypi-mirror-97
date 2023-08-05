import os 
class Decorator(object):
    def __init__(self):
        self.testing = os.environ.get("enableDailyTest", None) == str(True)
    def __call__(self, cls):
        class Wrapped(cls):
            testing = self.testing
        return Wrapped
