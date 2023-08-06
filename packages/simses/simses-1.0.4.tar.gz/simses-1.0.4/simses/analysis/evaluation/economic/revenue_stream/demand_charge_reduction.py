from datetime import datetime

import numpy
import pytz

from simses.analysis.data.energy_management import EnergyManagementData
from simses.analysis.data.system import SystemData
from simses.analysis.evaluation.economic.revenue_stream.abstract_revenue_stream import RevenueStream
from simses.analysis.evaluation.result import EvaluationResult, Unit, Description
from simses.analysis.utils import get_fractional_years
from simses.commons.config.analysis.economic import EconomicAnalysisConfig
from simses.commons.log import Logger
from simses.commons.utils.utilities import add_month_to, add_year_to, get_average_from, get_maximum_from


class DemandChargeReduction(RevenueStream):

    class BillingPeriod:
        MONTHLY: str = 'monthly'
        YEARLY: str = 'yearly'
        OPTIONS: [str] = [MONTHLY, YEARLY]

    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData,
                 economic_analysis_config: EconomicAnalysisConfig):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self.__log: Logger = Logger(type(self).__name__)
        self.__billing_period = economic_analysis_config.demand_charge_billing_period
        self.__demand_charge = economic_analysis_config.demand_charge_price
        self.__demand_charge_average_interval = economic_analysis_config.demand_charge_average_interval
        self.__key_results: [EvaluationResult] = list()
        self.__seconds_per_year = 24 * 60 * 60 * 365
        if self.__billing_period not in self.BillingPeriod.OPTIONS:
            raise Exception('Please configure demand charge billing period to one of the following options: ' +
                            str(self.BillingPeriod.OPTIONS) + '. The current billing cycle is set to ' +
                            str(self.__billing_period) + '.')

    def __get_demand_charge_in_billing_period_for(self, time: numpy.ndarray, power: numpy.ndarray) -> list:
        start: float = time[0]
        # Calculate demand charge based on absolute power values
        power: numpy.ndarray = numpy.column_stack([time, abs(power)])
        billing_period_date: datetime = self.__get_initial_billing_period_for(start)
        billing_period_start: float = billing_period_date.timestamp()
        billing_period_date = self.__get_next_billing_period(billing_period_date)
        billing_period_end: float = billing_period_date.timestamp()
        interval_end = start - start % self.__demand_charge_average_interval + self.__demand_charge_average_interval
        power_interval: list = list()
        power_avg_in_interval: list = list()
        power_max_for_billing_period: list = list()
        tstmp_start: float = start
        tstmp_last: float = start
        for tstmp, value in power:
            power_interval.append(value)
            tstmp_last = tstmp
            if tstmp >= interval_end:  # get average power values for demand charge interval
                power_avg_in_interval.append(get_average_from(power_interval))
                power_interval.clear()
                interval_end += self.__demand_charge_average_interval
            if tstmp >= billing_period_end:  # get maximum power values for billing period
                # scale values accordingly to days that have passed in the respective billing period
                factor: float = (tstmp - tstmp_start) / (billing_period_end - billing_period_start)
                power_max_for_billing_period.append(get_maximum_from(power_avg_in_interval) * factor)
                power_avg_in_interval.clear()
                tstmp_start = tstmp
                billing_period_start = billing_period_end
                billing_period_date = self.__get_next_billing_period(billing_period_date)
                billing_period_end: float = billing_period_date.timestamp()
        # add remaining values, but scale down to passed time in current billing period
        factor: float = (tstmp_last - tstmp_start) / (billing_period_end - billing_period_start)
        power_avg_in_interval.append(get_average_from(power_interval))
        power_max_for_billing_period.append(get_maximum_from(power_avg_in_interval) * factor)
        # convert maximum power values into demand charge
        return list(numpy.array(power_max_for_billing_period) * self.__demand_charge / 1000.0)

    def __get_initial_billing_period_for(self, tstmp: float) -> datetime:
        date = datetime.fromtimestamp(tstmp, tz=pytz.UTC)
        # start of month
        date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if self.__billing_period == self.BillingPeriod.YEARLY:
            # start of year
            date = date.replace(month=1)
        return date

    def __get_next_billing_period(self, date: datetime) -> datetime:
        if self.__billing_period == self.BillingPeriod.MONTHLY:
            date = add_month_to(date)
        else:  # self.__billing_period == self.BillingPeriod.YEARLY
            date = add_year_to(date)
        return date

    def __get_cashflow_in_project_years_for(self, time: numpy.ndarray, demand_charge: list) -> numpy.ndarray:
        # date handling
        start: float = time[0]
        project_date = datetime.fromtimestamp(start, tz=pytz.UTC)
        project_date = add_year_to(project_date)
        project_year_end: float = project_date.timestamp()
        billing_period_dt = self.__get_initial_billing_period_for(start)
        # cashflow calculation
        cashflow: [float] = []
        cashflow_in_project_years: list = list()
        while demand_charge:
            cashflow.append(demand_charge.pop(0))
            billing_period_start: float = billing_period_dt.timestamp()
            billing_period_dt = self.__get_next_billing_period(billing_period_dt)
            billing_period_end: float = billing_period_dt.timestamp()
            if billing_period_end >= project_year_end:
                factor: float = (project_year_end - billing_period_start) / (billing_period_end - billing_period_start)
                last_cashflow: float = cashflow[-1]
                cashflow[-1] *= factor
                cashflow_in_project_years.append(sum(cashflow))
                cashflow = [last_cashflow * (1.0 - factor)]
                project_date = add_year_to(project_date)
                project_year_end = project_date.timestamp()
        if cashflow:
            # Determine if remaining cashflow is part of a new project year or needs to be added to the last
            total_fractional_years = get_fractional_years(time[0], time[-1])
            if len(cashflow_in_project_years) <= total_fractional_years:
                cashflow_in_project_years.append((sum(cashflow)))
            else:
                cashflow_in_project_years[-1] += sum(cashflow)
        return numpy.array(cashflow_in_project_years)

    def __print_warning(self):
        time = self._energy_management_data.time
        if time[1] - time[0] > self.__demand_charge_average_interval:
            self.__log.warn('Simulation timestep is larger than DEMAND_CHARGE_AVERAGE_INTERVAL (' +
                             str(self.__demand_charge_average_interval) + ' sec). Economic evaluation for peak shaving '
                                                                          'may not be representative.')

    def get_cashflow(self) -> numpy.ndarray:
        self.__print_warning()
        # get data for calculation
        time: numpy.ndarray = self._energy_management_data.time
        load_power: numpy.ndarray = self._energy_management_data.load_power
        pv_power: numpy.ndarray = self._energy_management_data.pv_power
        storage_power: numpy.ndarray = self._system_data.power
        # calculate power arrays
        grid_power_base: numpy.ndarray = load_power - pv_power
        grid_power_storage: numpy.ndarray = load_power - pv_power + storage_power
        # calculate demand charge arrays
        demand_charge_base: list = self.__get_demand_charge_in_billing_period_for(time, grid_power_base)
        demand_charge_storage: list = self.__get_demand_charge_in_billing_period_for(time, grid_power_storage)
        # calculate cashflow arrays
        cashflow_base: numpy.ndarray = self.__get_cashflow_in_project_years_for(time, demand_charge_base)
        cashflow_storage: numpy.ndarray = self.__get_cashflow_in_project_years_for(time, demand_charge_storage)
        # append cashflow to key results
        self.__key_results.append(EvaluationResult(Description.Economical.DemandCharges.COST_WITHOUT_STORAGE,
                                                   Unit.EURO, cashflow_base))
        self.__key_results.append(EvaluationResult(Description.Economical.DemandCharges.COST_WITH_STORAGE,
                                                   Unit.EURO, cashflow_storage))
        return cashflow_base - cashflow_storage

    def get_evaluation_results(self):
        return self.__key_results

    def get_assumptions(self):
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.DemandCharges.CYCLE, Unit.NONE,
                                            self.__billing_period))
        assumptions.append(EvaluationResult(Description.Economical.DemandCharges.PRICE, Unit.EURO_PER_KW,
                                            self.__demand_charge))
        assumptions.append(EvaluationResult(Description.Economical.DemandCharges.INTERVAL, Unit.MINUTES,
                                            self.__demand_charge_average_interval / 60.0))
        return assumptions

    def close(self):
        self.__log.close()
