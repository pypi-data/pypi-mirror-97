import numpy as np

from simses.commons.log import Logger
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class NottonLossAcDcConverter(AcDcConverter):

    # Notton Type 2 inverter
    __P0 = 0.0072
    __K = 0.0345

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    __GRAVIMETRIC_POWER_DENSITY = 17000  # W/kg
    __SPECIFIC_SURFACE_AREA = 0.0001  # in m2 / W  # TODO add exact values
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)
    # ( https://www.apcuk.co.uk/app/uploads/2018/02/PE_Full_Pack.pdf )

    def __init__(self, max_power):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, ac_power: float, voltage: float) -> float:
        if ac_power >= 0:
            return 0
        return min(ac_power - self.__get_loss(ac_power), 0)

    def to_dc(self, ac_power: float, voltage: float) -> float:
        if ac_power <= 0:
            return 0
        else:
            return max(ac_power - self.__get_loss(ac_power), 0)

    def to_dc_reverse(self, power_dc: float) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = - power_dc / (1 - power_dc * self.__K / self._MAX_POWER)
            q = - self.__P0 * power_dc / (1 / self._MAX_POWER - abs(power_dc) * self.__K / self._MAX_POWER ** 2)
            self.__log.debug('P_DC: ' + str(power_dc))
            power_ac = max(0.0, -p / 2 + np.sqrt((p / 2) ** 2 - q))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    def to_ac_reverse(self, power_dc) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = self._MAX_POWER / self.__K
            q = (self.__P0 * self._MAX_POWER ** 2 - abs(power_dc) * self._MAX_POWER) / self.__K
            self.__log.debug('P_DC: ' + str(power_dc))
            power_ac = min(0.0, -(-p / 2 + np.sqrt((p / 2) ** 2 - q)))
            self.__log.debug('P_AC: ' + str(power_ac))
            return power_ac

    def __get_loss(self, power: float) -> float:
        return abs(self.__P0 * self._MAX_POWER + (self.__K / self._MAX_POWER) * power ** 2)

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @property
    def mass(self):
        return self.max_power / self.__GRAVIMETRIC_POWER_DENSITY

    @property
    def surface_area(self) -> float:
        return self.max_power * self.__SPECIFIC_SURFACE_AREA

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return NottonLossAcDcConverter(max_power)

    def close(self) -> None:
        pass
