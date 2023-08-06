# import math
#
# from simses.commons.cycle_detection.cycle_detector import CycleDetector
# from simses.commons.state.technology.lithium_ion import LithiumIonState
# from simses.technology.lithium_ion.cell.type import CellType
# from simses.technology.lithium_ion.degradation.cyclic.cyclic_degradation import \
#     CyclicDegradationModel
#
#
# class NRELCyclicDegradationModel(CyclicDegradationModel):
#
#     def __init__(self, cell_type: CellType, cycle_detector: CycleDetector):
#         super().__init__(cell_type, cycle_detector)
#         self.__c2_ref = 3.9193e-3
#         self.__c0_ref = 75.64  # Ah
#         self.__Ea_c_2 = -48260  # J/mol
#         self.__Ea_c_0 = 2224  # J/mol
#         self._beta_c_2 = 4.54
#         self.__initial_capacity = self._cell.get_nominal_capacity()
#         self.__TEMP_REF = 298.15  # K
#         self.__capacity_gain_pos = 0
#         self.__capacity_loss_li = 0
#         self.__capacity_neg = 0
#         self.__resistance_increase = 0
#         self.__R = 8.3144598
#         self.__a_2_ref = 46.05#Ah
#         self.__Ea_a2 =-29360 #J/mol
#         self.__Ea_b_2 = -42800
#         self.__b_2_ref = 1.541e-5
#         self.__c_0_ref = 75.64
#         self.__Ea_d01 = 34300  # J/mol
#         self.__Ea_d02 = 74860
#
#
#
#
#
#
#     def calculate_degradation(self, battery_state: LithiumIonState) -> None:
#         soc = battery_state.soc
#         self.__dod = 1-soc
#         self.__temp = battery_state.temperature
#         self.__fec = self._cycle_detector.get_full_equivalent_cycle() # Updating FEC
#         self.__c_2 = self.__c2_ref * math.exp((-self.__Ea_c_2 / self.__R) * (1 / self.__temp - 1 / self.__TEMP_REF))*(self.__dod)**self._beta_c_2
#
#         self.__d_0 = (self.__initial_capacity * math.exp(
#             (-self.__Ea_d01 / self.__R) * (1 / self.__temp - 1 / self.__TEMP_REF) - ((self.__Ea_d02 / self.__R) ** 2 * (
#                     1 / self.__temp - 1 / self.__TEMP_REF) ** 2)))
#         self.__capacity_loss_li =self.__d_0*( self.__b_2_ref * math.exp((-self.__Ea_b_2 / self.__R * (1 / self.__temp - 1 / self.__TEMP_REF))*self.__fec))
#         self.__capacity_gain_pos =0
#         self.__capacity_neg = (self.__c_0**2 -(2*self.__c_2*self.__c_0*self.__fec))**0.5
#         #self.__capacity_neg = 0
#
#     def calculate_resistance_increase(self, battery_state: LithiumIonState) -> None:
#         self.__a_2 = self.__a_2_ref * math.exp((-self.__Ea_a2 / self.__R) * (1 / self.__temp - 1 / self.__TEMP_REF))
#         self.__resistance_increase =self.__resistance_increase
#
#
#     def get_degradation(self) -> float:
#             return 0
#
#     def get_resistance_increase(self) -> float:
#         return self.__resistance_increase
#
#     def reset(self, lithium_ion_state: LithiumIonState) -> None:
#         pass
#
#     def close(self) -> None:
#         pass
#
#     def get_Li_inventory_loss(self) -> float:
#         return self.__capacity_loss_li
#
#     def get_Li_pos_electrode_capacity(self) -> float:
#         return self.__capacity_gain_pos
#
#     def get_Li_neg_electrode_capacity(self) -> float:
#         return self.__capacity_neg
