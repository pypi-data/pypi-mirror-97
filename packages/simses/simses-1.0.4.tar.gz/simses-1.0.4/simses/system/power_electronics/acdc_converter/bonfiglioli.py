import numpy as np

from simses.commons.log import Logger
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class BonfiglioliAcDcConverter(AcDcConverter):
    """
    Efficiency fit for converter RPS TL-4Q by Bonfiglioli
        (http://www.docsbonfiglioli.com/pdf_documents/catalogue/VE_CAT_RTL-4Q_STD_ENG-ITA_R00_5_WEB.pdf)
    using field data and Notton-Fit as described in master's thesis by Felix Müller.
    """

    __USE_FIELD_DATA = False
    # Notton-Fit parameter
    if __USE_FIELD_DATA:
        # measured data from battery systems providing fcr
        # Charge
        __P0_to_dc = 0.00195
        __K_to_dc = 0.01349
        __min_eff_cha = 0.3441
        # Discharge
        __P0_to_ac = 0.00292
        __K_to_ac = 0.03609
        __min_eff_dis = 0.2742
    else:
        # measured data under testing condition
        # Charge
        __P0_to_dc = 0.0072
        __K_to_dc = 0.034
        __min_eff_cha = 0.5813
        # Discharge
        __P0_to_ac = 0.0072
        __K_to_ac = 0.034
        __min_eff_dis = 0.5813

    __VOLUMETRIC_POWER_DENSITY = 1.667 * 1e5  # W / m3
    # Calculated Value: Nominal Power / (W * H * D)
    __GRAVIMETRIC_POWER_DENSITY = 342  # W/kg
    # Calculated Value: Nominal Power / Weight
    __SPECIFIC_SURFACE_AREA = 2.311 * 1e-5  # in m2 / W
    # Calculated Value: (W*H + W*D + H*D)*2 / Nominal Power

    def __init__(self, max_power: float):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        if power >= 0:
            return 0
        else:
            return power / self.__get_efficiency_to_ac(power)

    def to_dc(self, power: float, voltage: float) -> float:
        if power <= 0:
            return 0
        else:
            return power * self.__get_efficiency_to_dc(power)

    def to_dc_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = - dc_power / (1 - dc_power * self.__K_to_dc / self._MAX_POWER)
            q = - self.__P0_to_dc * dc_power / (1 / self._MAX_POWER - abs(dc_power) * self.__K_to_dc / self._MAX_POWER ** 2)
            self.__log.debug('P_DC: ' + str(dc_power))
            ac_power = max(0.0, -p / 2 + np.sqrt((p / 2) ** 2 - q))
            self.__log.debug('P_AC: ' + str(ac_power))
            return ac_power

    def to_ac_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            p = self._MAX_POWER / self.__K_to_ac
            q = (self.__P0_to_ac * self._MAX_POWER ** 2 - abs(dc_power) * self._MAX_POWER) / self.__K_to_ac
            self.__log.debug('P_DC: ' + str(dc_power))
            ac_power = min(0.0, -(-p / 2 + np.sqrt((p / 2) ** 2 - q)))
            self.__log.debug('P_AC: ' + str(ac_power))
            return min(ac_power, self.__min_eff_dis * dc_power)

    def __get_efficiency_to_ac(self, power) -> float:
        pf = abs(power) / self._MAX_POWER
        if 0.0 < pf > 1.0:
            raise Exception('Power factor is not possible: ' + str(pf))
        return max(self.__min_eff_dis, pf / (pf + self.__P0_to_ac + self.__K_to_ac * pf ** 2))

    def __get_efficiency_to_dc(self, power) -> float:
        pf = abs(power) / self._MAX_POWER
        if 0.0 < pf > 1.0:
            raise Exception('Power factor is not possible: ' + str(pf))
        return max(self.__min_eff_cha, pf / (pf + self.__P0_to_dc + self.__K_to_dc * pf ** 2))

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY

    @property
    def mass(self) -> float:
        return self.max_power / self.__GRAVIMETRIC_POWER_DENSITY

    @property
    def surface_area(self) -> float:
        return self.max_power * self.__SPECIFIC_SURFACE_AREA

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return BonfiglioliAcDcConverter(max_power)

    def close(self) -> None:
        self.__log.close()
