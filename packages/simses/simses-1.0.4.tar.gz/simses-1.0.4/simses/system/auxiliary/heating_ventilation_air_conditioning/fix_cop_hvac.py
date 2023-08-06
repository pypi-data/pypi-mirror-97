from numpy import sign
from simses.commons.config.simulation.system import StorageSystemConfig
from simses.system.auxiliary.heating_ventilation_air_conditioning.hvac import HeatingVentilationAirConditioning


class FixCOPHeatingVentilationAirConditioning(HeatingVentilationAirConditioning):

    def __init__(self, hvac_configuration: list):
        super().__init__()

        # Get optional user-defined values required for this class
        try:
            self.__max_thermal_power: float = float(hvac_configuration[StorageSystemConfig.HVAC_POWER])
        except IndexError:
            raise Exception('Please specify thermal power for HVAC class' + self.__name__)
        self.__min_thermal_power: float = self.__max_thermal_power * 0.0
        try:
            self.__set_point_temperature = float(hvac_configuration[StorageSystemConfig.HVAC_TEMPERATURE_SETPOINT]) + 273.15
        except IndexError:
            self.__set_point_temperature = 298.15
        # source for scop and seer :
        # https://data.toshiba-klima.at/de/Multisplit%20R32%20-%2010,00%20kW%20-%20R32%20-%20Home%20RAS-5M34U2AVG-E%20de.pdf
        # seasonal coefficient of performance (for cooling)
        self.__scop: float = 4.08
        # seasonal energy efficiency ratio (for heating)
        self.__seer: float = 6.31

        # Initialize variables
        self.__electric_power: float = 0
        self.__thermal_power: float = 0
        self.__air_mass: float = 0
        self.__air_specific_heat: float = 0

    def run_air_conditioning(self, temperature_time_series: [float], temperature_timestep: float) -> None:
        # This HVAC model monitors the air temperature (with respect to the provided set-point)
        # This logic reduces chatter and rapid switching between heating and cooling to some extent
        temperature_time_series = temperature_time_series[0]  # To control the air temperature: 0
        if abs(self.__set_point_temperature - temperature_time_series[-1]) > 1:
            cooling_power = -self.__air_mass * self.__air_specific_heat * \
                            (self.__set_point_temperature - temperature_time_series[-1])  # in W, rough cooling power estimate
            if abs(cooling_power) < self.__min_thermal_power:
                self.__thermal_power = 0.0
            elif abs(cooling_power) > self.__max_thermal_power:
                self.__thermal_power = self.__max_thermal_power * sign(cooling_power)
            else:
                self.__thermal_power = cooling_power

            # thermal_power is +ve when cooling and -ve when heating
            if cooling_power > 0:
                self.__electric_power = abs(self.__thermal_power / self.__seer)
            else:
                self.__electric_power = abs(self.__thermal_power / self.__scop)
        else:
            self.__thermal_power = 0
            self.__electric_power = 0
        # # idea to set basic power consumption if the hvac is active
        # if self.__thermal_power != 0:
        #     self.__electric_power = 1000+abs(self.__thermal_power / self.__scop)

    def get_max_thermal_power(self) -> float:
        return self.__max_thermal_power

    def get_thermal_power(self) -> float:
        return self.__thermal_power

    def get_electric_power(self) -> float:
        return self.__electric_power

    def get_set_point_temperature(self) -> float:
        return self.__set_point_temperature

    def get_scop(self) -> float:
        return self.__scop

    def get_seer(self) -> float:
        return self.__seer

    def update_air_parameters(self, air_mass: float = None, air_specific_heat: float = None) -> None:
        self.__air_mass = air_mass
        self.__air_specific_heat = air_specific_heat

    def set_electric_power(self, electric_power: float) -> None:
        """Used in cases where multiple runs of the HVAC take place within a SimSES timestep"""
        self.__electric_power = electric_power
