import pandas

from simses.analysis.data.abstract_data import Data
from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.commons.state.system import SystemState


class SystemData(Data):

    """
    Provides time series data from SystemState
    """

    def __init__(self, config: GeneralSimulationConfig, data: pandas.DataFrame):
        super().__init__(config, data)

    @property
    def id(self) -> str:
        return str(int(self._get_first_value(SystemState.SYSTEM_AC_ID))) + '.' + \
               str(int(self._get_first_value(SystemState.SYSTEM_DC_ID)))

    @property
    def time(self):
        return self._get_data(SystemState.TIME)

    @property
    def power(self):
        return self._get_data(SystemState.AC_POWER_DELIVERED)

    @property
    def aux_power(self):
        return self._get_data(SystemState.AUX_LOSSES)

    @property
    def ac_pe_power(self):
        return self.power - self.aux_power

    @property
    def energy_difference(self):
        soc = self._get_difference(SystemState.SOC)
        capacity = self.initial_capacity
        return soc * capacity

    @property
    def soc(self):
        return self._get_data(SystemState.SOC)

    @property
    def capacity(self):
        return self._get_data(SystemState.CAPACITY) / 1000.0

    @property
    def state_of_health(self):
        return self._get_data(SystemState.SOH)

    @property
    def storage_fulfillment(self):
        return self._get_data(SystemState.FULFILLMENT)

    @property
    def dc_power(self):
        return self._get_data(SystemState.DC_POWER_INTERMEDIATE_CIRCUIT)

    @property
    def dc_power_storage(self):
        return self._get_data(SystemState.DC_POWER_STORAGE)

    @property
    def dc_power_additional(self):
        return self._get_data(SystemState.DC_POWER_ADDITIONAL)

    @property
    def dc_power_loss(self):
        return self._get_data(SystemState.DC_POWER_LOSS)

    @property
    def ac_power_target(self):
        return self._get_data(SystemState.AC_POWER)

    @property
    def is_top_level_system(self) -> bool:
        return self.id == '0.0'

    @classmethod
    def get_system_data(cls, path: str, config: GeneralSimulationConfig) -> list:
        system_data: [pandas.DataFrame] = cls._get_system_data_for(path, SystemState, SystemState.TIME,
                                                                   SystemState.SYSTEM_AC_ID, SystemState.SYSTEM_DC_ID)
        res: [SystemData] = list()
        for data in system_data:
            res.append(SystemData(config, data))
        # solution for duplicate information if only one ac system was simulated
        if len(res) == 2:
            systems = res[:]
            for system in systems:
                if not system.is_top_level_system:
                    res.remove(system)
        Data.sort_by_id(res)
        return res
