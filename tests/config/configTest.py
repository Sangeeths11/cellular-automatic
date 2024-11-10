import unittest
from src.config.config import ConfigBuilder
from src.config.config import _Config

class ConfigBuilderTest(unittest.TestCase):

    def test_build_returnsDefaultConfig(self):
        # ARRANGE
        configBuilder: ConfigBuilder = ConfigBuilder()
        expectedMaxItterations: int = _Config._DEFAULT_MAX_NUMBER_OF_ITTERATIONS
        expectedPath: str =_Config()._getStandartPath()

        # ACT
        config: _Config = configBuilder.build()

        # ASSERT
        self.assertEqual(expectedMaxItterations, config.getMaxItterations())
        self.assertEqual(expectedPath, config.getSavePath())

    def test_setSavePath_hasNewPath(self):
        # ARRANGE
        configBuilder: ConfigBuilder = ConfigBuilder()
        expectedMaxItterations: int = _Config._DEFAULT_MAX_NUMBER_OF_ITTERATIONS
        expectedPath: str = "AnOtherPath"

        # ACT
        config: _Config = configBuilder.setSavePath(expectedPath).build()

        # ASSERT
        self.assertEqual(expectedMaxItterations, config.getMaxItterations())
        self.assertEqual(expectedPath, config.getSavePath())

    def test_setMaxItterations_hasNewMaxItterations(self):
        # ARRANGE
        configBuilder: ConfigBuilder = ConfigBuilder()
        expectedMaxItterations: int = 20
        expectedPath: str =_Config()._getStandartPath()

        # ACT
        config: _Config = configBuilder.setNumberOfMaxItterations(expectedMaxItterations).build()

        # ASSERT
        self.assertEqual(expectedMaxItterations, config.getMaxItterations())
        self.assertEqual(expectedPath, config.getSavePath())


if __name__ == "__main__":
    unittest.main()