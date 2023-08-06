import math

import pandas as pd
import scipy.interpolate

from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType


class MolicelNMC(CellType):
    """An NMC (NMC_Molicel) is a special cell type and inherited by CellType"""
    """Source: 
    Schuster, S. F., Bach, T., Fleder, E., Müller, J., Brand, M., Sextl, G., & Jossen, A. (2015). 
    Nonlinear aging characteristics of lithium-ion cells under different operational conditions. 
    Journal of Energy Storage, 1, 44–53. doi:10.1016/j.est.2015.05.003 """

    __SOC_IDX = 0

    __CELL_VOLTAGE = 3.7  # V
    __CELL_CAPACITY = 1.9  # Ah

    pd.set_option('precision', 9)

    def __init__(self, voltage: float, capacity: float, soh: float, battery_config: BatteryConfig,
                 battery_data_config: BatteryDataConfig):
        super().__init__(voltage, capacity, soh, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)

        self.__battery_data_config = battery_data_config
        self.__log: Logger = Logger(type(self).__name__)
        self.__RINT_FILE = self.__battery_data_config.nmc_molicel_rint_file
        self.__nom_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = 4.25 * self._SERIAL_SCALE  # V
        self.__min_voltage = 3 * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah

        self.__max_c_rate_charge = 1.05  # 1/h
        self.__max_c_rate_discharge = 2.1  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A

        self.__min_temperature = 273.15  # K
        self.__max_temperature = 318.15  # K

        self.__coulomb_efficiency_charge = 1  # -
        self.__coulomb_efficiency_discharge = 1  # -
        self.__self_discharge_rate = 0 # Self discharge is neglectged in our simulations;
        # self.__self_discharge_rate = 0.015 / (30.5 * 24 * 3600)  # 1.5%-soc per month in second step

        # Physical parameters for lithium_ion thermal model
        # See SimSES Paper for Sources
        self.__mass = 0.045 * self._SERIAL_SCALE * self._PARALLEL_SCALE  # in kg for 1 cell
        self.__diameter = 18  # mm
        self.__length = 65  # mm
        self.__volume = math.pi * self.__diameter ** 2 * self.__length / 4 * 10 ** (-9) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m3
        self.__surface_area = (2 * math.pi * self.__diameter / 2 * self.__length + 2 * math.pi * (
                    self.__diameter / 2) ** 2) * 10 ** (-6) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m2
        self.__specific_heat = 965  # J/kgK
        self.__convection_coefficient = 15  # W/m2K, parameter for natural convection

        internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm
        soc_arr = internal_resistance.iloc[:, self.__SOC_IDX]
        rint_mat_ch = internal_resistance.iloc[:, 2]
        rint_mat_dch = internal_resistance.iloc[:, 5]
        self.__rint_ch_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_ch, kind='linear')
        self.__rint_dch_interp1d = scipy.interpolate.interp1d(soc_arr, rint_mat_dch, kind='linear')

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        '''Parameters build with ocv fitting'''
        a1 = -1.6206
        a2 = -6.9895
        a3 = 1.4458
        a4 = 1.9530
        b1 = 3.4206
        b2 = 0.8759
        k0 = 2.0127
        k1 = 2.7684
        k2 = 1.0698
        k3 = 4.1431
        k4 = -3.8417
        k5 = -0.1856
        soc = battery_state.soc

        ocv = k0 + \
              k1 / (1 + math.exp(a1 * (soc - b1))) + \
              k2 / (1 + math.exp(a2 * (soc - b2))) + \
              k3 / (1 + math.exp(a3 * (soc - 1))) +\
              k4 / (1 + math.exp(a4 * soc)) +\
              k5 * soc

        return ocv * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        soc = self.check_soc_range(battery_state.soc)
        if battery_state.is_charge:
            rint = self.__rint_ch_interp1d(soc)
        else:
            rint = self.__rint_dch_interp1d(soc)
        return float(rint) / self._PARALLEL_SCALE * self._SERIAL_SCALE

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

    def get_capacity_cal_file_name(self) -> str:
        return self.__battery_data_config.nmc_molicel_capacity_cal_file

    def get_resistance_cal_file_name(self) -> str:
        return self.__battery_data_config.nmc_molicel_ri_cal_file

    def get_capacity_cyc_file_name(self) -> str:
        return self.__battery_data_config.nmc_molicel_capacity_cyc_file

    def get_resistance_cyc_file_name(self) -> str:
        return self.__battery_data_config.nmc_molicel_ri_cyc_file

    def get_mass(self) -> float:
        return self.__mass

    def get_volume(self):
        return self.__volume

    def get_surface_area(self):
        return self.__surface_area

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def close(self):
        self.__log.close()
