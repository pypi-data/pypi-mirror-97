from simses.commons.profile.file import FileProfile
from simses.commons.config.data.temperature import TemperatureDataConfig
from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.system.thermal.ambient.ambient_thermal_model import AmbientThermalModel


class LocationAmbientTemperature(AmbientThermalModel):

    """
    LocationAmbientTemperature provides a ambient temperature profile for a specified location.
    Ambient temperature time series data for Berlin, Germany and Jodhpur, India from DLR Greenius Tool:
    https://www.dlr.de/sf/en/desktopdefault.aspx/tabid-11688/20442_read-44865/
    """

    def __init__(self, data_config: TemperatureDataConfig, general_config: GeneralSimulationConfig):
        super().__init__()
        self.__start_time = general_config.start
        self.__file = FileProfile(general_config, data_config.location_temperature_file)

    def get_temperature(self, time) -> float:
        temp_c = self.__file.next(time)  # in °C
        temp_k = temp_c + 273.15  # in K
        return temp_k

    def get_initial_temperature(self) -> float:
        return self.get_temperature(self.__start_time)  # in K

    def close(self):
        self.__file.close()


