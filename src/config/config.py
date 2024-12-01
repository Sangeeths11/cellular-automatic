import os

class _Config():

    _DEFAULT_MAX_NUMBER_OF_ITTERATIONS: int = 200

    def __init__(self):
        self.savePath = self._getStandartPath()
        self.maxItterations = self._DEFAULT_MAX_NUMBER_OF_ITTERATIONS
        pass

    def getSavePath(self) -> str:
        return self.savePath

    def setSavePath(self, path: str) -> None:
        self.savePath = path

    def getMaxItterations(self) -> int:
        return self.maxItterations

    def setMaxNumberOfItterations(self, maxItterations) -> None:
        self.maxItterations = maxItterations

    def _getStandartPath(self) -> str:
        pwd = os.getcwd()
        return os.path.join(pwd, "data")
    
    def __repr__(self) -> str:
        return f"---Config---\nsavePath: <{self.savePath}>\nMaxItterations: <{self.maxItterations}>"


class ConfigBuilder():

    def __init__(self):
        self.config = _Config()
    
    def setSavePath(self, path: str):
        self.config.setSavePath(path)
        return self
    
    def setNumberOfMaxItterations(self, maxItterations):
        self.config.setMaxNumberOfItterations(maxItterations)
        return self
    
    def build(self) -> _Config:
        return self.config