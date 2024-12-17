from src.exceptions.simulationErrorCodes import SimulationErrorCodes

class SimulationException(Exception):
    def __init__(self, errorCode: SimulationErrorCodes) -> None:
        self.errorCode = errorCode
    
    def getMessage(self) -> str:
        return self.errorCode.value[1]
    
    def getCode(self) -> str:
        return self.errorCode.value[0]