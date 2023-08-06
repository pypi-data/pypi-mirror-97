from configparser import ConfigParser

from simses.commons.config.simulation.simulation_config import SimulationConfig, clean_split
from simses.commons.profile.file import FileProfile
from simses.commons.profile.power.file import FilePowerProfile


class ProfileConfig(SimulationConfig):
    """
    Profile specific configs
    """

    SECTION: str = 'PROFILE'

    POWER_PROFILE_DIR: str = 'POWER_PROFILE_DIR'
    TECHNICAL_PROFILE_DIR: str = 'TECHNICAL_PROFILE_DIR'
    LOAD_PROFILE: str = 'LOAD_PROFILE'
    FREQUENCY_PROFILE: str = 'FREQUENCY_PROFILE'
    LOAD_FORECAST_PROFILE: str = 'LOAD_FORECAST_PROFILE'
    SOC_PROFILE: str = 'SOC_PROFILE'
    GENERATION_PROFILE: str = 'GENERATION_PROFILE'
    LOAD_SCALING_FACTOR: str = 'LOAD_SCALING_FACTOR'
    GENERATION_SCALING_FACTOR: str = 'GENERATION_SCALING_FACTOR'


    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)

    @property
    def power_profile_dir(self) -> str:
        """Returns directory of power profiles from __analysis_config file_name"""
        return self.get_data_path(self.get_property(self.SECTION, self.POWER_PROFILE_DIR))

    @property
    def technical_profile_dir(self) -> str:
        """Returns directory of frequency profiles from __analysis_config file_name"""
        return self.get_data_path(self.get_property(self.SECTION, self.TECHNICAL_PROFILE_DIR))

    @property
    def load_profile(self) -> str:
        """ Return selected load profile"""
        return self.power_profile_dir + self.get_property(self.SECTION, self.LOAD_PROFILE)

    @property
    def frequency_file(self) -> str:
        """Returns frequency profile file_name name from __analysis_config file_name"""
        return self.technical_profile_dir + self.get_property(self.SECTION, self.FREQUENCY_PROFILE)

    @property
    def load_forecast_file(self) -> str:
        """Returns frequency profile file_name name from __analysis_config file_name"""
        return self.technical_profile_dir + self.get_property(self.SECTION, self.LOAD_FORECAST_PROFILE)

    @property
    def soc_file(self) -> str:
        """Returns soc profile file_name"""
        return self.technical_profile_dir + self.__get_soc_profile()[0]

    @property
    def soc_file_value(self) -> int:
        """Returns soc profile value index"""
        try:
            return int(self.__get_soc_profile()[1])
        except IndexError:
            return 1

    def __get_soc_profile(self) -> [str]:
        return clean_split(self.get_property(self.SECTION, self.SOC_PROFILE), ',')

    @property
    def generation_profile_file(self) -> str:
        """ Return PV generation profile file_name name from __analysis_config file_name"""
        return self.power_profile_dir + self.get_property(self.SECTION, self.GENERATION_PROFILE)

    @property
    def load_scaling_factor(self) -> float:
        """ Return scaling factor for the load from __analysis_config file_name"""
        load_scaling_factor: float = float(self.get_property(self.SECTION, self.LOAD_SCALING_FACTOR))
        if load_scaling_factor == 1.0:
            return load_scaling_factor  # default value 1: original values are taken
        else:
            return load_scaling_factor / 1000.0 / self.__get_annual_consumption()

    @property
    def generation_scaling_factor(self) -> float:
        """ Return scaling factor for pv from __analysis_config file_name"""
        scaling_factor: float = float(self.get_property(self.SECTION, self.GENERATION_SCALING_FACTOR))
        if scaling_factor == 1.0:
            return scaling_factor  # deafult value 1: original values are taken
        else:
            return scaling_factor / 1000.0 / self.__get_peak_power()

    def __get_annual_consumption(self) -> float:
        return self.__get_value_from_header(FilePowerProfile.Header.ANNUAL_CONSUMPTION, self.load_profile)

    def __get_peak_power(self) -> float:
        return self.__get_value_from_header(FilePowerProfile.Header.PEAK_POWER, self.generation_profile_file)

    @staticmethod
    def __get_value_from_header(name: str, file: str) -> float:
        try:
            header: dict = FileProfile.get_header_from(file)
            value = float(header[name])
            return value
        except IndexError:
            return 1.0
