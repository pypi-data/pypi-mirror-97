import math

import pandas as pd
import scipy.interpolate

from simses.commons.config.data.battery import BatteryDataConfig
from simses.commons.config.simulation.battery import BatteryConfig
from simses.commons.log import Logger
from simses.commons.state.technology.lithium_ion import LithiumIonState
from simses.technology.lithium_ion.cell.type import CellType


class SonyLFP(CellType):
    """An LFP is a special cell type and inherited by CellType"""

    __SOC_HEADER = 'SOC'
    __SOC_IDX = 0
    __TEMP_IDX = 1
    __C_RATE_IDX = 0
    __ETA_IDX = 1

    __CELL_VOLTAGE = 3.2  # V
    __CELL_CAPACITY = 3.0  # Ah

    pd.set_option('precision', 9)

    def __init__(self, voltage: float, capacity: float, soh: float, battery_config: BatteryConfig,
                 battery_data_config: BatteryDataConfig):
        super().__init__(voltage, capacity, soh, self.__CELL_VOLTAGE, self.__CELL_CAPACITY, battery_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__RINT_FILE = battery_data_config.lfp_sony_rint_file

        # Source SONY_US26650FTC1_Product Specification and Naumann, Maik. Techno-economic evaluation of stationary
        # lithium_ion energy storage systems with special consideration of aging.
        # PhD Thesis. Technical University Munich, 2018.

        self.__nominal_voltage = self.__CELL_VOLTAGE * self._SERIAL_SCALE  # V
        self.__max_voltage = 3.6 * self._SERIAL_SCALE  # V
        self.__min_voltage = 2.0 * self._SERIAL_SCALE  # V
        self.__capacity = self.__CELL_CAPACITY * self._PARALLEL_SCALE  # Ah
        self.__max_c_rate_charge = 1  # 1/h
        self.__max_c_rate_discharge = 6.6  # 1/h
        self.__max_current = self.__capacity * self.__max_c_rate_charge  # A
        self.__min_current = -self.__capacity * self.__max_c_rate_discharge  # A
        self.__coulomb_efficiency = 1 # Coulomb Efficiency is set to 1. Losses are calculated via internal resistance

        # Physical parameters for lithium_ion thermal model
        # See SimSES Paper for Sources
        self.__mass = 0.07 * self._SERIAL_SCALE * self._PARALLEL_SCALE  # kg
        self.__diameter = 26  # mm
        self.__length = 65  # mm
        self.__volume = math.pi * self.__diameter ** 2 * self.__length / 4 * 10 ** (-9) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m3
        self.__surface_area = (2 * math.pi * self.__diameter/2 * self.__length + 2 * math.pi * (self.__diameter/2)**2) * 10**(-6) * self._SERIAL_SCALE * self._PARALLEL_SCALE  # m2
        self.__specific_heat = 1001  # J/kgK
        self.__convection_coefficient = 15  # W/m2K

        self.__min_temperature = 273.15  # K
        self.__max_temperature = 333.15  # K

        # Self discharge is neglected in our simulations 0.015 / (30.5 * 24 * 3600) #1.5%-soc per month in second step
        self.__self_discharge_rate = 0
        self.__internal_resistance = pd.read_csv(self.__RINT_FILE, delimiter=';', decimal=",")  # Ohm
        # SOC array has only 11 entries 0:0.1:1
        soc_arr = self.__internal_resistance.iloc[:, self.__SOC_IDX]
        # Temperature array has only 4 values (283.15 K, 298.15 K, 313.15 K, 333.15 K)
        temp_arr = self.__internal_resistance.iloc[:4, self.__TEMP_IDX]
        # internal resistance for charge, Column 2:5 for charging
        rint_mat_ch = self.__internal_resistance.iloc[:, 2:6]
        # internal resistance for discharge, Column 6:9 for charging
        rint_mat_dch = self.__internal_resistance.iloc[:, 6:]
        self.__rint_ch_interp2d = scipy.interpolate.interp2d(temp_arr.T, soc_arr, rint_mat_ch, kind='linear')
        self.__rint_dch_interp2d = scipy.interpolate.interp2d(temp_arr.T, soc_arr, rint_mat_dch, kind='linear')

    def get_open_circuit_voltage(self, battery_state: LithiumIonState) -> float:
        '''Parameters build with ocv fitting'''
        a1 = -116.2064
        a2 = -22.4512
        a3 = 358.9072
        a4 = 499.9994
        b1 = -0.1572
        b2 = -0.0944
        k0 = 2.0020
        k1 = -3.3160
        k2 = 4.9996
        k3 = -0.4574
        k4 = -1.3646
        k5 = 0.1251

        soc = battery_state.soc

        ocv = k0 + \
              k1 / (1 + math.exp(a1 * (soc - b1))) + \
              k2 / (1 + math.exp(a2 * (soc - b2))) + \
              k3 / (1 + math.exp(a3 * (soc - 1))) +\
              k4 / (1 + math.exp(a4 * soc)) +\
              k5 * soc

        return ocv * self._SERIAL_SCALE

    def get_internal_resistance(self, battery_state: LithiumIonState) -> float:
        if battery_state.is_charge:
            rint = self.__rint_ch_interp2d(battery_state.temperature, battery_state.soc)
        else:
            rint = self.__rint_dch_interp2d(battery_state.temperature, battery_state.soc)
        return float(rint) / self._PARALLEL_SCALE * self._SERIAL_SCALE

    def get_self_discharge_rate(self) -> float:
        return self.__self_discharge_rate

    def get_coulomb_efficiency(self, battery_state: LithiumIonState) -> float:
        return self.__coulomb_efficiency if battery_state.is_charge else 1 / self.__coulomb_efficiency

    def get_nominal_voltage(self) -> float:
        return self.__nominal_voltage

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

    def get_mass(self) -> float:
        return self.__mass

    def get_surface_area(self):
        return self.__surface_area

    def get_volume(self):
        return self.__volume

    def get_specific_heat(self):
        return self.__specific_heat

    def get_convection_coefficient(self):
        return self.__convection_coefficient

    def close(self):
        self.__log.close()