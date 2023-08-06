# import math
# from simses.commons.cycle_detection.cycle_detector import CycleDetector
# from simses.technology.lithium_ion.degradation_model.calendar_degradation_model.calendar_degradation_model import \
#
# from simses.commons.state.technology.lithium_ion import LithiumIonState
# from simses.technology.lithium_ion.cell.type import CellType
# from simses.technology.lithium_ion.degradation.calendar.calendar_degradation import \
#     CalendarDegradationModel
#
#
# class NRELCalendarDegradationModel(CalendarDegradationModel):
#
#     def __init__(self, cell_type: CellType,cycle_detector: CycleDetector):
#         super().__init__(cell_type,cycle_detector)
#         self._cell: CellType = cell_type
#         self.__initial_capacity =self._cell.get_capacity()
#         self.__Li_inventory_capacity = self.__initial_capacity
#         self.__resistance_increase = 0
#
#         self.__initial_capacity = self._cell.get_nominal_capacity()
#         self.__b_0 = 1.07
#         self.__Ea_01 = 28640  # J
#         self.__capacity_loss_li= 0
#         self.__capacity_pos = 0
#         self.__capacity_neg = 0
#         self.__Ah = 65
#         self.__TEMP_REF = 298.15  #
#         self.__SOC_REF = 1  # pu
#         self.__R = 8.3144598  # J/(K*mol)
#         self.__F = 96485  # C/mol
#         self.__V_ref = 3.7   # V
#         self.__U_ref = 0.08   # V
#         self.__d3 = 0.46   # Ah
#         self.__d0_ref = 75.10  # Ah
#         self.__Ea_d01 = 34300   # J/mol
#         self.__Ea_d02 = 74860  # J/mol
#         self.__b1_ref = 3.503e-3   # day^-0.5
#         self.__Ea_b1 = 35392  # J/mol
#         self.__alpha_b_1 = 1
#         self.__gamma_b_1 = 2.472
#         self.__b3_ref = 2.805e-2
#         self.__Ea_b3 = 42800  # J/mol
#         self.__alpha_b_3 = 0.0066
#         self.__beta_b_1 = 2.157
#         self.__taw_b3 = 5
#         self.__taw_a3 = 100
#         self.__theta = 0.135
#         self.__a0_1 = 0.442
#         self.__a0_2 = -0.199
#         self.__Ea_01 = 28640  # J
#         self.__Ea_02 = -46010  # J/mol
#         self.__a1_ref = 0.0134  # day^-1/2
#         self.__Ea_a1 = 36100  # J/mol
#         self.__alpha_a_1 = -1
#         self.__gamma_a_1 = 2.433
#         self.__beta_a_1 = 1.870
#         self.__alpha_a4 = -1.0
#         self.__Ea_a2 = -29360  # J/mol
#         self.__a2_ref = 46.05  #
#         self.__a3_ref = 0.145  #
#         self.__Ea_a3 = -29360  # J/mol
#         self.__a2_ref = 46.05  # Ah
#         self.__a3_ref = 0.145  # Ah
#         self.__Ea_a2 = -29360  # J/mol
#         self.__Ea_a4 = 77470  # J/mol
#         self.__a4_ref = 5.357e-4  # day^-1
#         self.__alpha_a_4 = -1
#         self.__b2_ref = 1.541e-5
#         self.__Ea_b2 = -42800  # J/mol
#         self.__R0_ref = 1.155e-3
#         self.__Ea_r0 = -28640 # J/mol
#         self.__temp_ref = 318
#         #self.__d0_ini = (self.__d0_ref* math.exp((-self.__Ea_d01 / self.__R) * (1 / self.__temp_ref - 1 / self.__TEMP_REF) - ((self.__Ea_d02 / self.__R) ** 2 * (
#                     #1 / self.__temp_ref - 1 / self.__TEMP_REF) ** 2)))
#
#         self.__pos_electrode_loss = 0
#         self.__neg_electrode_less = 0
#         self.__capacity_pos_change = 0
#         self.__inventory_loss = 0
#
#
#     def calculate_degradation(self, time: float, battery_state: LithiumIonState) -> None:
#         soc = battery_state.soc
#         voltage = self._cell.get_open_circuit_voltage(battery_state) / self._cell.get_serial_scale()
#         temp = battery_state.temperature
#         self.__RPT= 298
#         curr=battery_state.current
#         self.__u_val = 0.08
#         time_passed = time- battery_state.time
#         time_hour=time
#         self.__d_0 = (self.__d0_ref* math.exp((-self.__Ea_d01 / self.__R) * (1 / self.__RPT - 1 / self.__TEMP_REF) - ((self.__Ea_d02 / self.__R) ** 2 * (
#                     1 / self.__RPT - 1 / self.__TEMP_REF) ** 2)))
#         #self.__capacity_pos = self.__d_0
#         self.__dod = self._cycle_detector.get_depth_of_cycle()
#         qloss = (self.__initial_capacity - battery_state.capacity / battery_state.nominal_voltage) / self.__initial_capacity
#         self.__b_1 = self.__b1_ref * math.exp((-self.__Ea_b1 / self.__R) * (1 / temp - 1 / self.__TEMP_REF))*(self.__alpha_b_1 * self.__F / self.__R * (self.__u_val / temp - self.__U_ref / self.__TEMP_REF)*(self.__gamma_b_1 * (self.__dod ) ** self.__beta_b_1))
#         virtual_time_one= (qloss / self.__d_0 * self.__b_1) ** 2
#         self.__b_3= self.__b3_ref * math.exp((-self.__Ea_b3 / self.__R) * (1 / temp - 1 / self.__TEMP_REF))* math.exp( self.__alpha_b_3 * self.__F / self.__R * (self._cell.get_open_circuit_voltage(battery_state) / temp - self.__V_ref / self.__TEMP_REF))*(1+(self.__theta*self.__dod))
#         #self.__b_4=math.exp(self.__alpha_b_3 * self.__F / self.__R * (voltage / temp - self.__V_ref / self.__TEMP_REF))
#         #ma
#            # self.__alpha_b_1 * self.__F / self.__R * (self.__u_val / temp - self.__U_ref / self.__TEMP_REF)) * math.exp(
#             #self.__gamma_b_1 * (soc) ** self.__beta_b_1)
#         # math.exp( self.__alpha_b_3 * self.__F / self.__R * (self._cell.get_open_circuit_voltage(battery_state) / temp - self.__V_ref / self.__TEMP_REF))
#         #self.__b_2 = * (1 + (self.__theta * self.__dod))       # self.__R*(voltage/ temp - self.__V_ref / self.__TEMP_REF)
#         #self.__inventory_loss = self.__b_1*(virtual_time+time_passed) ** 0.5
#         virtual_time_second = math.log((1 - (qloss/ self.__b_3 * self.__d_0)) * self.__taw_b3,2.718)
#         #(self.__d_0 * (self.__b_1 * (time_passed + virtual_time_one)) +
#         capacity_loss=(self.__d_0 * (self.__b_1 * (time_passed + virtual_time_one)**0.5) + ( self.__b3_ref * (1 - math.exp(-time_passed + virtual_time_second / self.__taw_b3))))
#         capacity_loss-= qloss  # relative qloss in pu
#         self.__inventory_loss = capacity_loss * self.__initial_capacity
#         #self.__inventory_loss = self.__Li_inventory_capacity - self.__inventory_loss
#         self.__capacity_pos_change =-self.__d3 * (1 - math.exp( -time_hour*curr/ 228))
#         #self.__capacity_pos = 0
#         #self.__capacity_neg = 0
#     def calculate_resistance_increase(self, time: float, battery_state: LithiumIonState) -> None :
#         soc = battery_state.soc
#         temp = battery_state.temperature
#         self.__dod = 1 - soc
#         time_passed = time - battery_state.time
#         #soc = battery_state.soc
#         #temp = battery_state.temperature
#         #nominal_voltage = battery_state.nominal_voltage
#
#         self.__a_3 = self.__a3_ref *math.exp((-self.__Ea_a3/ self.__R) * (1 / temp - 1 / self.__TEMP_REF))
#         self.__a_1 = self.__a1_ref * math.exp((-self.__Ea_a1 / self.__R) * (1 / temp - 1 / self.__TEMP_REF))*math.exp(self.__gamma_a_1 * (self.__dod) ** self.__beta_a_1)
#         self.__a_4=  self.__a4_ref * math.exp((-self.__Ea_a4 / self.__R) * (1 / temp - 1 / self.__TEMP_REF))*math.exp(self.__alpha_a_4 * self.__F / self.__R * (4/ temp - self.__U_ref / self.__TEMP_REF))
#         math.exp(self.__gamma_a_1 * (self.__dod) ** self.__beta_a_1)
#         #self.__a_4 = self.__a4_ref * math.exp((-self.__Ea_a4 / self.__R) * (1 / temp - 1 / self.__TEMP_REF))
#         #math.exp(self.__alpha_a_4 * self.__F / self.__R * (
#                     #self._cell.get_open_circuit_voltage(battery_state) / temp - self.__V_ref / self.__TEMP_REF))
#      #resistance_increase = self.__R0_ref * (math.exp(-self.__Ea_r0 / self.__R * (1 / temp - 1 / self.__TEMP_REF)))*(
#                                                # ((self.__a0_1 * (math.exp(-self.__Ea_a1 / self.__R * (1 / temp - 1 / self.__TEMP_REF))))
#                                     #+ (self.__a0_2*(math.exp(-self.__Ea_a2 / self.__R * (1 / temp - 1 / self.__TEMP_REF))))) +
#                                     #(self.__a_4 * time_passed)+(self.__a_1*(time_p
#         resistance_increase = ((self.__a_4 * time_passed)+((self.__a_1*(time_passed)**0.5)+self.__a_3*(1-math.exp(-time_passed/self.__taw_a3))))
#          #resis= self.__a_3*(1-math.exp(-time_passed/self.__taw_a3)
#         # resistance_increase = ((self.__a_4 * time_passed)+((self.__a_1*(time_passed)**0.5)
#
#         self.__resistance_increase = resistance_increase
#
#     def get_degradation(self) -> float:
#         return 0
#
#     def get_resistance_increase(self) -> float:
#         return self.__resistance_increase
#
#     def reset(self, battery_state: LithiumIonState) -> None:
#         pass
#     def close(self) -> None:
#         pass
#
#     def get_Li_inventory_capacity(self) -> float:
#         return self.__inventory_loss
#
#     def get_pos_electrode_capacity(self) -> float:
#         return self.__capacity_pos_change
#
#     def get_Li_neg_electrode_capacity(self) -> float:
#         return self.__neg_electrode_less
