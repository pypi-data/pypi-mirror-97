import math

from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.calendar.calendar_degradation import \
    CalendarDegradationModel


class SanyoNMCCalendarDegradationModel(CalendarDegradationModel):
    """Source: Schmalstieg, J., Käbitz, S., Ecker, M., & Sauer, D. U. (2014).
    A holistic aging model for Li (NiMnCo) O2 based 18650 lithium-ion batteries.
    Journal of Power Sources, 257, 325-334."""
    __capacity_loss = 0
    __resistance_increase = 0

    def __init__(self, cell_type: CellType):
        super().__init__(cell_type)
        self.__capacity_loss_cal = cell_type.get_calendar_capacity_loss_start()
        self.__rinc_cal = 0

    def calculate_degradation(self, time: float, battery_state: LithiumIonState) -> None:
        time_passed = time - battery_state.time
        # Calendar degradation in dummy cell is a function of sqrt(t)
        temp = battery_state.temperature # cell temperature in K
        voltage = self._cell.get_open_circuit_voltage(battery_state) / self._cell.get_serial_scale() # single cell voltage
        qloss: float = self.__capacity_loss_cal
        # TODO Workaround for preventing complex numbers
        voltage = max(voltage, 3.15)
        alpha_cap = (7.543*voltage - 23.75)*10**6*math.exp(-6976/temp)
        virtual_time = (qloss/alpha_cap)**(4/3) # virtual aging time in days
        capacity_loss = alpha_cap*(virtual_time + time_passed / 86400)**(0.75) - qloss

        self.__capacity_loss = capacity_loss * self._cell.get_nominal_capacity()  # Ah
        self.__capacity_loss_cal += capacity_loss

    def calculate_resistance_increase(self, time: float, battery_state: LithiumIonState) -> None:
        time_passed = time - battery_state.time
        temp = battery_state.temperature # cell temperature in K
        voltage = self._cell.get_open_circuit_voltage(battery_state) / self._cell.get_serial_scale() # single cell voltage
        rinc_cal = self.__rinc_cal
        # TODO Workaround for preventing complex numbers
        voltage = max(voltage, 3.15)
        alpha_res = (5.27*voltage - 16.32)*10**5*math.exp(-5986/temp)
        virtual_time = (rinc_cal/alpha_res)**(4/3) # virtual time in days
        resistance_increase = alpha_res*(virtual_time + time_passed / 86400)**(0.75) - rinc_cal

        self.__rinc_cal += resistance_increase
        self.__resistance_increase = resistance_increase  # pu

    def get_degradation(self) -> float:
        return self.__capacity_loss

    def get_resistance_increase(self) -> float:
        return self.__resistance_increase

    def reset(self, battery_state: LithiumIonState) -> None:
        self.__capacity_loss_cal = 0
        self.__rinc_cal = 0

    def close(self) -> None:
        pass
