from configparser import ConfigParser

from simses.commons.config.simulation.simulation_config import SimulationConfig


class BatteryConfig(SimulationConfig):
    """
    Battery specific configs
    """

    def __init__(self, config: ConfigParser, path: str = None):
        super().__init__(path, config)
        self.__section: str = 'BATTERY'

    @property
    def soc(self) -> float:
        """
        Minimum SOC (0-1)

        Returns
        -------
        float:
            Returns the start soc from data_config file

        """
        return float(self.get_property(self.__section, 'START_SOC'))

    @property
    def min_soc(self) -> float:
        """
        Minimum SOC (0-1)

        Returns
        -------
        float:
            Returns the minimum soc from data_config file

        """
        return float(self.get_property(self.__section, 'MIN_SOC'))

    @property
    def max_soc(self) -> float:
        """
        Maximum SOC (0-1)

        Returns
        -------
        float:
            Returns the maximum soc from data_config file

        """
        return float(self.get_property(self.__section, 'MAX_SOC'))

    @property
    def eol(self) -> float:
        """
        End of Life criteria (0-1)

        Returns
        -------
        float:
            Returns EOL criteria in % from data_config file

        """
        return float(self.get_property(self.__section, 'EOL'))

    @property
    def start_soh(self) -> float:
        """
        End of Life criteria (0-1)

        Returns
        -------
        float:
            Returns start SOH from data_config file

        """
        return float(self.get_property(self.__section, 'START_SOH'))

    @property
    def exact_size(self) -> bool:
        """Returns selection for exact sizing True/False"""
        return self.get_property(self.__section, 'EXACT_SIZE') in ['True']

    @property
    def start_soh_share(self) -> float:
        """
        Share of start SOH between calendar and cyclic capacity degradation

        Returns
        -------
        float:
            Returns start SOH share in p.u.

        """
        return 0.5

    @property
    def serial_scale(self) -> float:
        """Returns a linear scaling factor of cell in order to simulate a serial lithium_ion connection"""
        return float(self.get_property(self.__section, 'CELL_SERIAL_SCALE'))

    @property
    def parallel_scale(self) -> float:
        """Returns a linear scaling factor of cell in order to simulate a parallel lithium_ion connection"""
        return float(self.get_property(self.__section, 'CELL_PARALLEL_SCALE'))
