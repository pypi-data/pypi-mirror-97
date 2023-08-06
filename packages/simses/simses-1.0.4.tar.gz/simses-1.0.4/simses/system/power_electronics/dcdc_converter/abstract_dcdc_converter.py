from abc import ABC, abstractmethod

from simses.system.auxiliary.auxiliary import Auxiliary


class DcDcConverter(ABC):

    def __init__(self, intermediate_circuit_voltage: float):
        self._intermediate_circuit_voltage: float = intermediate_circuit_voltage

    @abstractmethod
    def calculate_dc_current(self, dc_power: float, storage_voltage: float) -> None:
        """
        function to calculate the dc current

        Parameters
        ----------
        dc_power : dc input power in W
        storage_voltage : voltage of storage in V

        Returns
        -------
        dc current in A
        """
        pass

    @abstractmethod
    def reverse_calculate_dc_current(self, dc_power: float, storage_voltage: float) -> None:
        """
        function to calculate the dc current

        Parameters
        ----------
        dc_power : dc input power in W
        storage_voltage : voltage of storage in V

        Returns
        -------
        dc current in A
        """
        pass

    @property
    @abstractmethod
    def max_power(self) -> float:
        pass

    @property
    def intermediate_circuit_voltage(self):
        return self._intermediate_circuit_voltage

    @property
    @abstractmethod
    def dc_power_loss(self):
        pass

    @property
    @abstractmethod
    def dc_power(self):
        pass

    @property
    @abstractmethod
    def dc_current(self):
        pass

    @property
    @abstractmethod
    def volume(self):
        """
        Volume of dc dc converter in m3

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def mass(self):
        """
        Mass of dc dc converter in kg

        Returns
        -------

        """
        pass

    @property
    @abstractmethod
    def surface_area(self):
        """
        Surface area of dc dc converter in m2

        Returns
        -------

        """
        pass

    @abstractmethod
    def get_auxiliaries(self) -> [Auxiliary]:
        pass

    @staticmethod
    def _is_charge(power: float) -> bool:
        return power > 0.0

    @abstractmethod
    def close(self) -> None:
        """
        Closing all open resources in dcdc converter

        Parameters
        ----------

        Returns
        -------

        """

        pass
