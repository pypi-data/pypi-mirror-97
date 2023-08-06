from simses.commons.log import Logger
from simses.system.power_electronics.acdc_converter.abstract_acdc_converter import AcDcConverter


class NoLossAcDcConverter(AcDcConverter):

    __VOLUMETRIC_POWER_DENSITY = 143 * 1e6  # W / m3
    __GRAVIMETRIC_POWER_DENSITY = 17000  # W/kg
    __SPECIFIC_SURFACE_AREA = 0.0001  # in m2 / W  # TODO add exact values
    # Exemplary value from:
    # (https://www.iisb.fraunhofer.de/en/research_areas/vehicle_electronics/dcdc_converters/High_Power_Density.html)

    def __init__(self, max_power: float):
        super().__init__(max_power)
        self.__log: Logger = Logger(type(self).__name__)

    def to_ac(self, power: float, voltage: float) -> float:
        if power >= 0:
            return 0
        else:
            return power

    def to_dc(self, power: float, voltage: float) -> float:
        if power <= 0:
            return 0
        else:
            return power

    def to_dc_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power < 0:
            self.__log.error('Power DC should be positive in to DC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        else:
            return dc_power

    def to_ac_reverse(self, dc_power: float) -> float:
        if dc_power == 0:
            return 0.0
        elif dc_power > 0:
            self.__log.error('Power DC should be negative in to AC reverse function, but is '
                             + str(dc_power) + 'W. Check function update_ac_power_from.')
            return 0.0
        return dc_power

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
        return NoLossAcDcConverter(max_power)

    def close(self) -> None:
        pass
