from .data_config import DataConfig


class TemperatureDataConfig(DataConfig):

    SECTION: str = 'TEMPERATURE_DATA'
    LOCATION_DIR: str = 'LOCATION_DIR'
    LOCATION_TEMPERATURE_FILE: str = 'LOCATION_TEMPERATURE_FILE'
    LOCATION_GLOBAL_HORIZONTAL_IRRADIANCE_FILE: str = 'LOCATION_GLOBAL_HORIZONTAL_IRRADIANCE_FILE'

    def __init__(self, path: str = None):
        super().__init__(path)
        self.__section: str = 'TEMPERATURE_DATA'

    @property
    def location_data_dir(self) -> str:
        """Returns directory of location data directory"""
        return self.get_data_path(self.get_property(self.SECTION, self.LOCATION_DIR))

    @property
    def location_temperature_file(self) -> str:
        """Returns directory of location temperature data file"""
        return self.location_data_dir + self.get_property(self.SECTION, self.LOCATION_TEMPERATURE_FILE)

    @property
    def location_global_horizontal_irradiance_file(self) -> str:
        """Returns directory of location global horizontal irradiance data file"""
        return self.location_data_dir + self.get_property(self.SECTION, self.LOCATION_GLOBAL_HORIZONTAL_IRRADIANCE_FILE)

