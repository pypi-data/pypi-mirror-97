import math

import numpy as np

from simses.analysis.data.energy_management import EnergyManagementData
from simses.analysis.data.system import SystemData
from simses.analysis.evaluation.economic.revenue_stream.abstract_revenue_stream import RevenueStream
from simses.analysis.evaluation.result import EvaluationResult, Unit, Description
from simses.commons.config.analysis.economic import EconomicAnalysisConfig


class EnergyCostReduction(RevenueStream):

    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData,
                 economic_analysis_config: EconomicAnalysisConfig):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self.__cashflowlist_storage_nondiscount = []
        self.__cashflowlist_base_nondiscount = []
        self.__price_consumption = economic_analysis_config.electricity_price
        self.__price_generation = economic_analysis_config.pv_feed_in_tariff
        self.__seconds_per_year = 24 * 60 * 60 * 365
        self.__Ws_to_kWh = 1/1000 * 1/3600

    def get_cashflow(self) -> np.ndarray:

        # price consumption per kWh
        price_consumption = self.__price_consumption
        # price generation per kWh
        price_generation = self.__price_generation
        time = self._energy_management_data.time
        generation = self._energy_management_data.pv_power
        load = self._energy_management_data.load_power
        storage = self._system_data.power

        cashflowlist_storage_nondiscount = []
        cashflowlist_base_nondiscount = []
        delta_ts = time[1] - time[0]

        # New Method (vector addition)
        grid_power_base = load - generation
        grid_power_with_storage = load - generation + storage
        # Determine cash flow for base scenario and scenario with storage
        cashflow_base = np.asarray([power * price_consumption if power >= 0
                         else power * price_generation
                         for power in grid_power_base]) * delta_ts * self.__Ws_to_kWh
        cashflow_storage = np.asarray([power * price_consumption if power >= 0
                         else power * price_generation
                         for power in grid_power_with_storage]) * delta_ts * self.__Ws_to_kWh

        # Split list into cash flow list with total cash flow for each project year
        years = (time[-1] - time[0]) / self.__seconds_per_year
        fullyears = int(math.floor(years))
        steps_per_year = int(len(time) / ((time[-1] - time[0]) / self.__seconds_per_year))
        for y in range(fullyears):
            cashflowlist_storage_nondiscount.append(sum(cashflow_storage[y * steps_per_year: (y+1) * steps_per_year]))
            cashflowlist_base_nondiscount.append(sum(cashflow_base[y * steps_per_year: (y+1) * steps_per_year]))

        # Add last year
        if fullyears * steps_per_year < len(cashflow_storage):
            cashflowlist_storage_nondiscount.append(sum(cashflow_storage[fullyears * steps_per_year: -1]))
            cashflowlist_base_nondiscount.append(sum(cashflow_base[fullyears * steps_per_year: -1]))

        self.__cashflowlist_storage_nondiscount = cashflowlist_storage_nondiscount
        self.__cashflowlist_base_nondiscount = cashflowlist_base_nondiscount
        revenue_nondiscount = [- cashflowlist_storage_nondiscount[i] + cashflowlist_base_nondiscount[i] for i in
                               range(len(cashflowlist_base_nondiscount))]
        return np.array(revenue_nondiscount)

    def get_evaluation_results(self):
        key_results: [EvaluationResult] = list()
        key_results.append(EvaluationResult(Description.Economical.SCI.COST_WITHOUT_STORAGE, Unit.EURO, self.__cashflowlist_base_nondiscount))
        key_results.append(EvaluationResult(Description.Economical.SCI.COST_WITH_STORAGE, Unit.EURO, self.__cashflowlist_storage_nondiscount))
        return key_results

    def get_assumptions(self):
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.SCI.COST_ELECTRICITY, Unit.EURO_PER_KWH, self.__price_consumption))
        assumptions.append(EvaluationResult(Description.Economical.SCI.PV_FEED_IN_TARIFF, Unit.EURO_PER_KWH, self.__price_generation))
        return assumptions

    def close(self):
        pass

