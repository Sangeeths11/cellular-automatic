
class SimulationException(Exception):
    def __init__(self, message) -> None:
        self.message = message
    
    def getMessage(self) -> str:
        return self.message