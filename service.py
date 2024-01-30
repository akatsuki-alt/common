import threading
class Service:
    
    def __init__(self, service_name, daemonize=False) -> None:
        self.service_name = service_name
        self.daemonize = daemonize
        self.thread = threading.Thread(target=self.run, name=service_name, daemon=self.daemonize)
    
    def run(self):
        pass
