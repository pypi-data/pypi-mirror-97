from configparser import ConfigParser

from simses.commons.config.simulation.simulation_config import SimulationConfig


class EnergyManagementConfig(SimulationConfig):
    """
    Energy management specific configs
    """

    SECTION: str = 'ENERGY_MANAGEMENT'

    STRATEGY: str = 'STRATEGY'
    POWER_FCR: str = 'POWER_FCR'
    POWER_IDM: str = 'POWER_IDM'
    SOC_SET: str = 'SOC_SET'
    MAX_POWER: str = 'MAX_POWER'
    MIN_SOC: str = 'MIN_SOC'
    MAX_SOC: str = 'MAX_SOC'
    FCR_RESERVE: str = 'FCR_RESERVE'

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)

    @property
    def operation_strategy(self) -> str:
        """Returns operation strategy from __analysis_config file_name"""
        return self.get_property(self.SECTION, self.STRATEGY)

    @property
    def max_fcr_power(self) -> float:
        """Returns max power for providing frequency containment reserve from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.POWER_FCR))

    @property
    def max_idm_power(self) -> float:
        """Returns max power for intra day market transactions from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.POWER_IDM))

    @property
    def soc_set(self) -> float:
        """Returns the optimal soc for a FCR storage from __analysis_config file_name.
        In case of an overall efficiency below 1, the optimal soc should be higher than 0.5"""
        return float(self.get_property(self.SECTION, self.SOC_SET))

    @property
    def max_power(self) -> float:
        """Returns max power for peak shaving from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.MAX_POWER))

    @property
    def min_soc(self) -> float:
        """Returns min soc from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.MIN_SOC))

    @property
    def max_soc(self) -> float:
        """Returns max soc from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.MAX_SOC))

    @property
    def fcr_reserve(self) -> float:
        """Returns max soc from __analysis_config file_name"""
        return float(self.get_property(self.SECTION, self.FCR_RESERVE))
