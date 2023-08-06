from simses.commons.state.abstract_state import State


class SystemState(State):
    """
    Current physical state of the system with the main electrical parameters.
    """

    SYSTEM_AC_ID = 'StorageSystemAC'
    SYSTEM_DC_ID = 'StorageSystemDC'
    AC_POWER = 'AC power in W'
    PE_LOSSES = 'PE_losses in W'
    FULFILLMENT = 'Fulfillment in p.u.'
    AC_POWER_DELIVERED = 'AC_P_delivered in W'
    # DC_VOLTAGE_INPUT = 'DC voltage input in V'
    DC_VOLTAGE = 'DC voltage in V'
    DC_CURRENT = 'DC current in A'
    AUX_LOSSES = 'Aux losses in W'
    DC_POWER_INTERMEDIATE_CIRCUIT = 'DC power of intermediate circuit in W'
    DC_POWER_STORAGE = 'DC power of storage in W'
    DC_POWER_LOSS = 'DC power loss in W'
    DC_POWER_ADDITIONAL = 'DC power additional in W'
    STORAGE_POWER_LOSS = 'DC power loss of storage technology in W'
    SOC = 'SOC in p.u.'
    SOH = 'State of Health in p.u.'
    CAPACITY = 'Capacity in Wh'
    TEMPERATURE = 'Temperature in K'
    MAX_CHARGE_POWER = 'Maximum charging power in W'
    MAX_DISCHARGE_POWER = 'Maximum discharging power in W'

    def __init__(self, system_id: int, storage_id: int):
        super().__init__()
        self._initialize()
        self.set(self.SYSTEM_AC_ID, system_id)
        self.set(self.SYSTEM_DC_ID, storage_id)

    @property
    def ac_power(self) -> float:
        return self.get(self.AC_POWER)

    @ac_power.setter
    def ac_power(self, value: float) -> None:
        self.set(self.AC_POWER, value)

    @property
    def pe_losses(self) -> float:
        return self.get(self.PE_LOSSES)

    @pe_losses.setter
    def pe_losses(self, value: float) -> None:
        self.set(self.PE_LOSSES, value)

    @property
    def fulfillment(self) -> float:
        return self.get(self.FULFILLMENT)

    @fulfillment.setter
    def fulfillment(self, value: float) -> None:
        self.set(self.FULFILLMENT, value)

    @property
    def ac_power_delivered(self) -> float:
        return self.get(self.AC_POWER_DELIVERED)

    @ac_power_delivered.setter
    def ac_power_delivered(self, value: float) -> None:
        self.set(self.AC_POWER_DELIVERED, value)

    # @property
    # def dc_voltage_input(self) -> float:
    #     return self.get(self.DC_VOLTAGE_INPUT)
    #
    # @dc_voltage_input.setter
    # def dc_voltage_input(self, value: float) -> None:
    #     self.set(self.DC_VOLTAGE_INPUT, value)

    @property
    def voltage(self) -> float:
        return self.get(self.DC_VOLTAGE)

    @voltage.setter
    def voltage(self, value: float) -> None:
        self.set(self.DC_VOLTAGE, value)

    @property
    def dc_current(self) -> float:
        return self.get(self.DC_CURRENT)

    @dc_current.setter
    def dc_current(self, value: float) -> None:
        self.set(self.DC_CURRENT, value)

    @property
    def aux_losses(self) -> float:
        return self.get(self.AUX_LOSSES)

    @aux_losses.setter
    def aux_losses(self, value: float) -> None:
        self.set(self.AUX_LOSSES, value)

    @property
    def dc_power_intermediate_circuit(self) -> float:
        return self.get(self.DC_POWER_INTERMEDIATE_CIRCUIT)

    @dc_power_intermediate_circuit.setter
    def dc_power_intermediate_circuit(self, value: float) -> None:
        self.set(self.DC_POWER_INTERMEDIATE_CIRCUIT, value)

    @property
    def dc_power_loss(self) -> float:
        return self.get(self.DC_POWER_LOSS)

    @dc_power_loss.setter
    def dc_power_loss(self, value: float) -> None:
        self.set(self.DC_POWER_LOSS, value)

    @property
    def storage_power_loss(self) -> float:
        return self.get(self.STORAGE_POWER_LOSS)

    @storage_power_loss.setter
    def storage_power_loss(self, value: float) -> None:
        self.set(self.STORAGE_POWER_LOSS, value)

    @property
    def dc_power_additional(self) -> float:
        return self.get(self.DC_POWER_ADDITIONAL)

    @dc_power_additional.setter
    def dc_power_additional(self, value: float) -> None:
        self.set(self.DC_POWER_ADDITIONAL, value)

    @property
    def dc_power_storage(self) -> float:
        return self.get(self.DC_POWER_STORAGE)

    @dc_power_storage.setter
    def dc_power_storage(self, value: float) -> None:
        self.set(self.DC_POWER_STORAGE, value)

    @property
    def soc(self) -> float:
        return self.get(self.SOC)

    @soc.setter
    def soc(self, value: float) -> None:
        self.set(self.SOC, value)

    @property
    def soh(self) -> float:
        return self.get(self.SOH)

    @soh.setter
    def soh(self, value: float) -> None:
        self.set(self.SOH, value)

    @property
    def capacity(self) -> float:
        return self.get(self.CAPACITY)

    @capacity.setter
    def capacity(self, value: float) -> None:
        self.set(self.CAPACITY, value)

    @property
    def temperature(self) -> float:
        return self.get(self.TEMPERATURE)

    @temperature.setter
    def temperature(self, value: float) -> None:
        self.set(self.TEMPERATURE, value)

    @property
    def max_charge_power(self) -> float:
        return self.get(self.MAX_CHARGE_POWER)

    @max_charge_power.setter
    def max_charge_power(self, value: float) -> None:
        self.set(self.MAX_CHARGE_POWER, value)

    @property
    def max_discharge_power(self) -> float:
        return self.get(self.MAX_DISCHARGE_POWER)

    @max_discharge_power.setter
    def max_discharge_power(self, value: float) -> None:
        self.set(self.MAX_DISCHARGE_POWER, value)

    @property
    def id(self) -> str:
        return 'SYSTEM' + str(self.get(self.SYSTEM_AC_ID)) + str(self.get(self.SYSTEM_DC_ID))

    # ac_power = property(get_ac_power, set_ac_power)
    # pe_losses = property(get_pe_losses, set_pe_losses)
    # fulfillment = property(get_fulfillment, set_fulfillment)
    # ac_power_delivered = property(get_ac_power_delivered, set_ac_power_delivered)
    # dc_voltage_input = property(get_dc_voltage_input, set_dc_voltage_input)
    # dc_voltage = property(get_dc_voltage, set_dc_voltage)
    # dc_current = property(get_dc_current, set_dc_current)
    # time = property(get_time, set_time)
    # aux_losses = property(get_aux_losses, set_aux_losses)
    # dc_power = property(get_dc_power, set_dc_power)
    # dc_power_loss = property(get_dc_power_loss, set_dc_power_loss)
    # soc = property(get_soc, set_soc)
    # capacity = property(get_capacity, set_capacity)

    @classmethod
    def sum_parallel(cls, system_states: []):
        system_state = SystemState(0, 0)
        for state in system_states:
            system_state.add(state)
        # average values
        size = len(system_states)
        system_state.divide_by(size, SystemState.FULFILLMENT)
        system_state.divide_by(size, SystemState.TIME)
        # calculate capacity weighted soc and soh
        system_state.soc = 0
        system_state.soh = 0
        for state in system_states:
            system_state.soc += state.soc * state.capacity / system_state.capacity
            system_state.soh += state.soh * state.capacity / system_state.capacity
        return system_state

    @property
    def is_charge(self) -> bool:
        return self.ac_power > 0

    @classmethod
    def sum_serial(cls, states: []):
        raise Exception('Not implemented yet')
