import threading

class ClassBetweenhreads:
    def __init__(self):
        self.users = ''
        self.received = []
        self.lock = threading.RLock()
