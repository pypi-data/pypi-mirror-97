from simses.commons.cycle_detection.cycle_detector import CycleDetector
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType
from simses.technology.lithium_ion.degradation.cyclic.cyclic_degradation import \
    CyclicDegradationModel


class SanyoNMCCyclicDegradationModel(CyclicDegradationModel):
    """Source: Schmalstieg, J., Käbitz, S., Ecker, M., & Sauer, D. U. (2014).
    A holistic aging model for Li (NiMnCo) O2 based 18650 lithium-ion batteries.
    Journal of Power Sources, 257, 325-334."""

    def __init__(self, cell_type: CellType, cycle_detector: CycleDetector):
        super().__init__(cell_type, cycle_detector)
        self.__log: Logger = Logger(type(self).__name__)
        self.__capacity_loss = 0
        self.__capacity_loss_cyclic = cell_type.get_cyclic_capacity_loss_start()
        self.__fec = 0
        self.__rinc_cyclic = 0
        self.__resistance_increase = 0
        self.__voltage_last_step = 3.6
        self.__cycle_detector: CycleDetector = cycle_detector

    def calculate_degradation(self, battery_state: LithiumIonState) -> None:
        doc: float = self._cycle_detector.get_depth_of_cycle()
        self.__fec = self._cycle_detector.get_full_equivalent_cycle() # Updating FEC

        qloss: float = self.__capacity_loss_cyclic # in p.u.
        qcell: float = battery_state.capacity / battery_state.nominal_voltage / self._cell.get_parallel_scale()

        # Open circuit voltage is used for cyclic degradation model
        voltage: float = self._cell.get_open_circuit_voltage(battery_state) / self._cell.get_serial_scale()
        v_ch = max(self.__voltage_last_step, voltage)  # charge voltage -> defined as higher one of both
        v_disch = min(self.__voltage_last_step, voltage)  # charge voltage -> defined as lower one of both
        v_average = (v_ch + v_disch)/2

        beta_cap = 7.348*10**(-3)*(v_average - 3.667)**2 + 7.6*10**(-4) + 4.081*10**(-3)*doc
        virtual_q = (qloss/beta_cap)**2 # virtual charge throughput in Ah
        capacity_loss = beta_cap*(virtual_q + qcell*doc)**0.5 - qloss

        self.__capacity_loss_cyclic += capacity_loss  # pu
        self.__capacity_loss = capacity_loss * self._cell.get_nominal_capacity()  # Ah

    def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
        doc: float = self.__cycle_detector.get_depth_of_cycle() # DOC
        rinc_cyclic: float = self.__rinc_cyclic
        qcell: float = battery_state.capacity / battery_state.nominal_voltage / self._cell.get_parallel_scale()

        voltage: float = self._cell.get_open_circuit_voltage(battery_state) / self._cell.get_serial_scale()
        v_ch = max(self.__voltage_last_step, voltage)  # charge voltage -> defined as higher one of both
        v_disch = min(self.__voltage_last_step, voltage)  # charge voltage -> defined as lower one of both
        v_average = (v_ch + v_disch) / 2

        beta_res = 2.153*10**(-4)*(v_average - 3.725)**2 - 1.521*10**(-5) + 2.798*10**(-4)*doc
        virtual_q = (rinc_cyclic/beta_res)**2 # virtual charge throughput in Ah
        resistance_increase = beta_res*(virtual_q + doc*qcell)**0.5 - rinc_cyclic

        self.__rinc_cyclic += resistance_increase
        self.__resistance_increase = resistance_increase  # pu

    def get_degradation(self) -> float:
        capacity_loss = self.__capacity_loss
        self.__capacity_loss = 0    # Set value to 0, because cyclic losses are not calculated in each step
        return capacity_loss

    def get_resistance_increase(self) -> float:
        resistance_increase = self.__resistance_increase
        self.__resistance_increase = 0 # Set value to 0, because cyclic losses are not calculated in each step
        return resistance_increase

    def reset(self, lithium_ion_state: LithiumIonState) -> None:
        self.__capacity_loss = 0
        self.__capacity_loss_cyclic = 0
        self.__rinc_cyclic = 0
        self.__resistance_increase = 0

    def close(self) -> None:
        self.__log.close()