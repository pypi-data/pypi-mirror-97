import numpy as np

from scipy import optimize

from simses.commons.log import Logger
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class SungrowAcDcConverter(AcDcConverter):
    """  Fitted Efficiency Curve using field data: Master Thesis by Felix Müller"""

    """ Source:
        Field data from fcr storage system. Datasheet of converter can be found here:
        ...\simses\simulation\storage_system\power_electronics\acdc_converter\data\datasungrow_SC1000TL_spec.pdf
    """


    __fit_dch = 1 # 1: Notton, 2: Rampinelli, 3: Rational12
    __fit_ch = 1 # 1: Notton, 2: Rampinelli, 3: Rational12
    __min_eff = 0.2092 # Minimum for efficiency (in case of Discharge and Notton or Rampinelli is used)

    # Notton
    # Fit for Discharging
    __P0_to_ac_Notton = 0.005511580
    __K_to_ac_Notton = 0.018772838
    # Fit for Charging
    __P0_to_dc_Notton = 0.007701864
    __K_to_dc_Notton = 0.017290859

    # Rampinelli
    # Fit for Discharging
    __K0_to_ac_Rampinelli = 0.003407887
    __K1_to_ac_Rampinelli = 0.013809826
    __K2_to_ac_Rampinelli = 0.003155305
    # Fit for Charging
    __K0_to_dc_Rampinelli = 0.007421847
    __K1_to_dc_Rampinelli = 0.003452202
    __K2_to_dc_Rampinelli = 0.011994448

    # Rational12
    # Fit for Discharging
    __a1_to_ac_Rat = 57.341420538
    __a0_to_ac_Rat = 0.092381040
    __b1_to_ac_Rat = 57.318868901
    __b0_to_ac_Rat = 0.441493908
    # Fit for Charging
    __a1_to_dc_Rat = 47.773200770
    __a0_to_dc_Rat = 0.210333852
    __b1_to_dc_Rat = 47.572383928
    __b0_to_dc_Rat = 0.630988885

    __VOLUMETRIC_POWER_DENSITY = 3.227 * 1e5  # W / m3
    # Calculated Value: Nominal Power / (W * H * D)
    __GRAVIMETRIC_POWER_DENSITY = 909  # W/kg
    # Calculated Value: Nominal Power / Weight
    __SPECIFIC_SURFACE_AREA = 1.349 * 1e-5  # in m2 / W
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

    def __get_efficiency_to_ac(self, power: float) -> float:
        power_factor = abs(power) / self._MAX_POWER
        if power_factor < 0.0 or power_factor > 1.0:
            raise Exception('Power factor is not possible: ' + str(power_factor))
        if self.__fit_dch == 1:
            return max(self.__min_eff, power_factor /
                       (power_factor + self.__P0_to_ac_Notton + self.__K_to_ac_Notton * power_factor ** 2))
        elif self.__fit_dch == 2:
            return max(self.__min_eff, power_factor / (power_factor + (self.__K0_to_ac_Rampinelli +
                       self.__K1_to_ac_Rampinelli * power_factor + self.__K2_to_ac_Rampinelli * power_factor ** 2)))
        elif self.__fit_dch == 3:
            return (self.__a1_to_ac_Rat * power_factor + self.__a0_to_ac_Rat) / \
                   (power_factor ** 2 + self.__b1_to_ac_Rat * power_factor + self.__b0_to_ac_Rat)
        else:
            raise Exception('Fit for Discharge is not possible: __fit_dch=' + str(self.__fit_dch))

    def __get_efficiency_to_dc(self, power: float) -> float:
        power_factor = abs(power) / self._MAX_POWER
        if power_factor < 0.0 or power_factor > 1.0:
            raise Exception('Power factor is not possible: ' + str(power_factor))
        if self.__fit_ch == 1:
            return power_factor / (power_factor + self.__P0_to_dc_Notton + self.__K_to_dc_Notton * power_factor ** 2)
        elif self.__fit_ch == 2:
            return power_factor / (power_factor + (self.__K0_to_dc_Rampinelli +
                       self.__K1_to_dc_Rampinelli * power_factor + self.__K2_to_dc_Rampinelli * power_factor ** 2))
        elif self.__fit_ch == 3:
            return (self.__a1_to_dc_Rat * power_factor + self.__a0_to_dc_Rat) / \
                   (power_factor ** 2 + self.__b1_to_dc_Rat * power_factor + self.__b0_to_dc_Rat)
        else:
            raise Exception('Fit for Charge is not possible: __fit_ch=' + str(self.__fit_ch))

    def to_dc_reverse(self, power_dc: float) -> float:
        if power_dc == 0:
            return 0.0
        elif power_dc < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(power_dc) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            if self.__fit_ch == 1:
                p = - power_dc / (1 - power_dc * self.__K_to_dc_Notton / self._MAX_POWER)
                q = - self.__P0_to_dc_Notton * power_dc / \
                    (1 / self._MAX_POWER - abs(power_dc) * self.__K_to_dc_Notton / self._MAX_POWER ** 2)
            elif self.__fit_ch == 2:
                p = - power_dc * (self.__K1_to_dc_Rampinelli + 1) / (
                        1 - power_dc * self.__K2_to_dc_Rampinelli / self._MAX_POWER)
                q = - self.__K0_to_dc_Rampinelli * power_dc / (
                            1 / self._MAX_POWER - abs(power_dc) * self.__K_to_dc_Notton / self._MAX_POWER ** 2)
            elif self.__fit_ch == 3:
                p = (self.__a0_to_dc_Rat * self._MAX_POWER - self.__b1_to_dc_Rat * power_dc) / (
                            self.__a1_to_dc_Rat - (power_dc / self._MAX_POWER))
                q = -(power_dc * self.__b0_to_dc_Rat * self._MAX_POWER) / (self.__a1_to_dc_Rat - (power_dc / self._MAX_POWER))
            else:
                raise Exception('Fit for Charge is not possible: __fit_ch=' + str(self.__fit_ch))
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
            if self.__fit_dch == 3:
                def fun(x):
                    return x ** 3 + self._MAX_POWER * self.__b1_to_ac_Rat * x ** 2 + \
                           (self.__b0_to_ac_Rat * self._MAX_POWER ** 2 - self._MAX_POWER * self.__a1_to_ac_Rat * abs(
                               power_dc)) * x - \
                           self._MAX_POWER ** 2 * self.__a0_to_ac_Rat * abs(power_dc)
                self.__log.debug('P_DC: ' + str(power_dc))
                opt_result = optimize.root(fun, abs(power_dc))
                power_ac = opt_result.x[0] * (-1)
                self.__log.debug('P_AC: ' + str(power_ac))
                return power_ac
            else:
                if self.__fit_dch == 1:
                    p = self._MAX_POWER / self.__K_to_ac_Notton
                    q = (self.__P0_to_ac_Notton * self._MAX_POWER ** 2 -
                        abs(power_dc) * self._MAX_POWER) / self.__K_to_ac_Notton
                elif self.__fit_dch == 2:
                    p = (1 + self.__K1_to_ac_Rampinelli) * self._MAX_POWER / self.__K0_to_ac_Rampinelli
                    q = (self.__K0_to_ac_Rampinelli * self._MAX_POWER ** 2 - abs(power_dc) * self._MAX_POWER) / \
                        self.__K2_to_ac_Rampinelli
                else:
                    raise Exception('Fit for Discharge is not possible: __fit_dch=' + str(self.__fit_dch))
                self.__log.debug('P_DC: ' + str(power_dc))
                power_ac = min(0.0, -(-p / 2 + np.sqrt((p / 2) ** 2 - q)))
                self.__log.debug('P_AC: ' + str(power_ac))
                return min(power_ac, self.__min_eff * power_dc)

    @property
    def volume(self) -> float:
        return self.max_power / self.__VOLUMETRIC_POWER_DENSITY\

    @property
    def mass(self):
        return self.max_power / self.__GRAVIMETRIC_POWER_DENSITY

    @property
    def surface_area(self) -> float:
        return self.max_power * self.__SPECIFIC_SURFACE_AREA

    @classmethod
    def create_instance(cls, max_power: float, power_electronics_config=None):
        return SungrowAcDcConverter(max_power)

    def close(self) -> None:
        self.__log.close()
