import math

from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.calendar.calendar_degradation import \
    CalendarDegradationModel


class SonyLFPCalendarDegradationModel(CalendarDegradationModel):

    def __init__(self, cell_type: CellType):
        super().__init__(cell_type)
        self.__initial_capacity = self._cell.get_nominal_capacity()

        # Source SONY_US26650FTC1_Product Specification and Naumann, Maik, et al.
        # "Analysis and modeling of calendar aging of a commercial LiFePO4/graphite cell."
        # Journal of Energy Storage 17 (2018): 153-169.
        # DOI: https://doi.org/10.1016/j.est.2018.01.019

        self.__capacity_loss = 0
        self.__resistance_increase = 0

        self.__TEMP_REF = 298.15  # K
        self.__SOC_REF = 1  # pu
        self.__R = 8.3144598  # J/(K*mol)

        self.__K_REF_QLOSS = 1.2571 * 10 ** (-5)  # pu*s^(-0.5)
        self.__A_QLOSS = -2059.8  # K
        self.__B_QLOSS = 9.2644  # constant
        self.__C_QLOSS = 2.8575  # constant
        self.__D_QLOSS = 0.60225  # constant
        self.__EA_QLOSS = 17126  # J/mol

        self.__K_REF_RINC = 3.4194 * 10 ** (-10)  # pu*s^(-0.5)
        self.__A_RINC = -8638.8  # K
        self.__B_RINC = 29.992  # constant
        self.__C_RINC = -3.3903  # constant
        self.__D_RINC = 1.5604  # constant
        self.__EA_RINC = 71827  # J/mol

    def calculate_degradation(self, time: float, battery_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        time_passed = time - battery_state.time
        soc = battery_state.soc
        temp = battery_state.temperature
        qloss = (self.__initial_capacity - battery_state.capacity / battery_state.nominal_voltage) / self.__initial_capacity  # pu

        virtual_time = (qloss / (
                self.__K_REF_QLOSS * math.exp(-self.__EA_QLOSS / self.__R * (1 / temp - 1 / self.__TEMP_REF)) * (
                self.__C_QLOSS * (soc - 0.5) ** 3 + self.__D_QLOSS))) ** 2 # seconds

        capacity_loss = (virtual_time + time_passed) ** 0.5 * self.__K_REF_QLOSS * math.exp(
            -self.__EA_QLOSS / self.__R * (1 / temp - 1 / self.__TEMP_REF)) * (
                                                 self.__C_QLOSS * (soc - 0.5) ** 3 + self.__D_QLOSS)  # total qloss p.u.

        capacity_loss -= qloss  # relative qloss in pu

        self.__capacity_loss = capacity_loss * self.__initial_capacity  # relative qloss in Ah

    def calculate_resistance_increase(self, time: float, battery_state: LithiumIonState) -> None:
        soc = battery_state.soc
        temp = battery_state.temperature
        time_passed = time - battery_state.time

        resistance_increase = time_passed * (self.__K_REF_RINC * math.exp(
            -self.__EA_RINC / self.__R * (1 / temp - 1 / self.__TEMP_REF)) * (
                                                       self.__C_RINC * (soc - 0.5) ** 2 + self.__D_RINC))

        self.__resistance_increase = resistance_increase # pu

    def get_degradation(self) -> float:
        return self.__capacity_loss

    def get_resistance_increase(self) -> float:
        return self.__resistance_increase

    def reset(self, battery_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        pass
