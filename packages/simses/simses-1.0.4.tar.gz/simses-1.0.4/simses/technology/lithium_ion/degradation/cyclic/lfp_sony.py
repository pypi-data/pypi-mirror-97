import scipy.integrate as integrate

from simses.commons.cycle_detection.cycle_detector import CycleDetector
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.cyclic.cyclic_degradation import \
    CyclicDegradationModel


class SonyLFPCyclicDegradationModel(CyclicDegradationModel):

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector):
        super().__init__(cell_type, cycle_detector)
        self.__log: Logger = Logger(type(self).__name__)
        self.__capacity_loss = 0
        self.__resistance_increase = 0
        self.__initial_capacity = self._cell.get_nominal_capacity()

        # Source SONY_US26650FTC1_Product Specification and Naumann, Maik, Franz Spingler, and Andreas Jossen.
        # "Analysis and modeling of cycle aging of a commercial LiFePO4/graphite cell."
        # Journal of Power Sources 451 (2020): 227666.
        # DOI: https://doi.org/10.1016/j.jpowsour.2019.227666

        self.__A_QLOSS = 0.0630  # constant
        self.__B_QLOSS = 0.0971  # constant
        self.__C_QLOSS = 4.0253  # constant
        self.__D_QLOSS = 1.0923  # constant

        self.__A_RINC = -0.0020  # constant
        self.__B_RINC = 0.0021  # constant
        self.__C_RINC = 6.8477  # constant
        self.__D_RINC = 0.91882  # constant

    def calculate_degradation(self, battery_state: LithiumIonState) -> None:
        try:
            crate: float = self._cycle_detector.get_crate() * 3600 # in 1 / s -> *3600 -> in 1/h
            doc: float = self._cycle_detector.get_depth_of_cycle() # in pu
            delta_fec: float = self._cycle_detector.get_delta_full_equivalent_cycle() # in pu
            qloss: float = (self.__initial_capacity - battery_state.capacity / battery_state.nominal_voltage) / self.__initial_capacity # pu
            virtual_fec: float = (qloss * 100 / ((self.__A_QLOSS * crate + self.__B_QLOSS) *
                                                (self.__C_QLOSS  * (doc - 0.6)**3 + self.__D_QLOSS )))**2

            rel_capacity_loss = lambda virtual_fec: (self.__A_QLOSS * crate + self.__B_QLOSS) *\
                                            (self.__C_QLOSS * (doc - 0.6)**3 + self.__D_QLOSS) / (2 * virtual_fec**0.5)

            capacity_loss, err = integrate.quad(rel_capacity_loss, virtual_fec, virtual_fec + delta_fec)
            capacity_loss = capacity_loss / 100 # pu

            self.__capacity_loss = capacity_loss * self.__initial_capacity  # Ah
        except ZeroDivisionError:
            self.__capacity_loss = 0
            self.__log.warn('Division by zero. Virtual FEC may be too small')
        except FloatingPointError:
            self.__capacity_loss = 0
            self.__log.warn('Division by zero. Virtual FEC may be too small')

    def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
        crate: float = self._cycle_detector.get_crate() * 3600 # in 1 / s -> *3600 -> in 1/h
        doc: float = self._cycle_detector.get_depth_of_cycle() # in pu
        delta_fec: float = self._cycle_detector.get_delta_full_equivalent_cycle()  # in pu
        rinc: float = battery_state.resistance_increase * 100 # in pu -> *100 -> in %

        virtual_fec: float = rinc / ((self.__A_RINC * crate + self.__B_RINC) *
                                            (self.__C_RINC * (doc - 0.5)**3 + self.__D_RINC))

        resistance_increase = (self.__A_RINC * crate + self.__B_RINC) * \
                                  (self.__C_RINC * (doc - 0.5)**3 + self.__D_RINC) * (virtual_fec + delta_fec) - rinc

        # Delta resistance increase
        self.__resistance_increase =  resistance_increase / 100 # in pu

    def get_degradation(self) -> float:
        capacity_loss = self.__capacity_loss
        self.__capacity_loss = 0    # Set value to 0, because cyclic losses are not calculated in each step
        return capacity_loss

    def get_resistance_increase(self) -> float:
        resistance_increase = self.__resistance_increase
        self.__resistance_increase = 0  # Set value to 0, because cyclic losses are not calculated in each step
        return resistance_increase

    def reset(self, lithium_ion_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        self.__log.close()
