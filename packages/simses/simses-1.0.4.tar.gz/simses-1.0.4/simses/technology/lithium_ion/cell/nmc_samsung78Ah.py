from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType


class Samsung78AhNMC(CellType):
    """Characterisation using field data: Master Thesis by Felix Müller"""

    r""" Source:
        Field data from fcr storage system. Datasheet can be found here:
        ...\simses\simulation\storage_system\technology\lithium_ion\cell_type\data\nmc_samsung78Ah_datasheet.pdf
    """

    __CELL_VOLTAGE = 3.7  # V
    __CELL_CAPACITY = 73.95  # Ah
    __CELL_RESISTANCE = 0.636847061 * 10 ** (-3)  # Ohm

    # Parameters for Curve Fitting: Discharge
    __p1_dch = 20.290042045
    __p2_dch = -60.088705239
    __p3_dch = 65.004615460
    __p4_dch = -30.204504426
    __p5_dch = 5.208737944
    __p6_dch = 0.473682851
    __p7_dch = 3.394776910

    # Parameters for Curve Fitting: Charge
    __p1_ch = 20.717822026
    __p2_ch = -60.174639133
    __p3_ch = 62.332299803
    __p4_ch = -25.900465062
    __p5_ch = 2.767903886
    __p6_ch = 0.931931308
    __p7_ch = 3.408247703

    # Parameters for Curve Fitting: Rest
    __p1_rest = 5.255925680
    __p2_rest = -14.288201873
    __p3_rest = 11.785819139
    __p4_rest = -0.932995895
    __p5_rest = -2.416565204
    __p6_rest = 1.282337714
    __p7_rest = 3.375062956

    def __init__(self, voltage: float, capacity: float, soh: float, battery_config: BatteryConfig,
                 battery_data_config: BatteryDataConfig):
        super().__init__(voltage, capacity, soh, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__nom_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = 4.1 * self._SERIAL_SCALE  # V
        self.__min_voltage = 2.7 * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah
        self.__max_c_rate_charge = 2  # 1/h
        self.__max_c_rate_discharge = 4  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A
        self.__min_temperature = 248.15  # K
        self.__max_temperature = 323.15  # K

        self.__coulomb_efficiency_charge = 0.9843  # -
        self.__coulomb_efficiency_discharge = 0.9843  # -

        self.__self_discharge_rate = 0  # Self discharge is neglectged in our simulations;

        # Physical parameters for lithium_ion thermal model
        self.__mass = 2  # kg
        self.__height = 125.7  # mm
        self.__wide = 45.6  # mm
        self.__length = 173.9  # mm

        self.__volume = self.__height * self.__wide * self.__length * 10 ** (-9)  # m3
        self.__surface_area = 2 * (self.__length * self.__height + self.__length * self.__wide +
                                   self.__wide * self.__height) * 10 ** (-6)  # m2

        # Values from nmc_sanyo_ur18650e (source: https://akkuplus.de/Panasonic-UR18650E-37-Volt-2150mAh-Li-Ion-EOL)
        self.__specific_heat = 823  # J/kgK
        self.__convection_coefficient = 15  # W/m2K, parameter for natural convection

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        soc = battery_state.soc
        if battery_state.is_charge:
            open_circuit_voltage_cell = self.__p1_ch * soc ** 6 + self.__p2_ch * soc ** 5 + self.__p3_ch * soc ** 4 + \
                                        self.__p4_ch * soc ** 3 + self.__p5_ch * soc ** 2 + self.__p6_ch * soc + self.__p7_ch
        else:
            if battery_state.current == 0:
                open_circuit_voltage_cell = self.__p1_rest * soc ** 6 + self.__p2_rest * soc ** 5 + self.__p3_rest * soc ** 4 + \
                                            self.__p4_rest * soc ** 3 + self.__p5_rest * soc ** 2 + self.__p6_rest * soc + self.__p7_rest
            else:
                open_circuit_voltage_cell = self.__p1_dch * soc ** 6 + self.__p2_dch * soc ** 5 + self.__p3_dch * soc ** 4 + \
                                            self.__p4_dch * soc ** 3 + self.__p5_dch * soc ** 2 + self.__p6_dch * soc + self.__p7_dch
        return open_circuit_voltage_cell * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        return float(self.__CELL_RESISTANCE / self._PARALLEL_SCALE * self._SERIAL_SCALE)

    def get_self_discharge_rate(self) -> float:
        return self.__self_discharge_rate

    def get_coulomb_efficiency(self, battery_state: LithiumIonState) -> float:
        return self.__coulomb_efficiency_charge if battery_state.is_charge else 1 / self.__coulomb_efficiency_discharge

    def get_nominal_voltage(self) -> float:
        return self.__nom_voltage

    def get_min_current(self, battery_state: LithiumIonState) -> float:
        return self.__min_current

    def get_nominal_capacity(self) -> float:
        return self.__capacity

    def get_capacity(self, battery_state: LithiumIonState) -> float:
        return self.__capacity

    def get_max_current(self, battery_state: LithiumIonState) -> float:
        return self.__max_current

    def get_min_temp(self) -> float:
        return self.__min_temperature

    def get_max_temp(self) -> float:
        return self.__max_temperature

    def get_min_voltage(self) -> float:
        return self.__min_voltage

    def get_max_voltage(self) -> float:
        return self.__max_voltage

    def get_serial_scale(self) -> float:
        return self._SERIAL_SCALE

    def get_parallel_scale(self) -> float:
        return self._PARALLEL_SCALE

# Physical parameters for lithium_ion thermal model

    def get_mass(self) -> float:
        return self.__mass * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_volume(self):
        return self.__volume * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_surface_area(self):
        return self.__surface_area * self._SERIAL_SCALE * self._PARALLEL_SCALE

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def close(self):
        self.__log.close()
