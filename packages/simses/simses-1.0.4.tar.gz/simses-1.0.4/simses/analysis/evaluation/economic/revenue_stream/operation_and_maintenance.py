import math
from datetime import datetime, timedelta

import numpy
from pytz import timezone

from simses.analysis.data.energy_management import EnergyManagementData
from simses.analysis.data.system import SystemData
from simses.analysis.evaluation.economic.revenue_stream.abstract_revenue_stream import RevenueStream
from simses.analysis.evaluation.result import EvaluationResult, Description, Unit
from simses.analysis.utils import get_fractional_years
from simses.commons.config.analysis.economic import EconomicAnalysisConfig


class OperationAndMaintenanceRevenue(RevenueStream):

    """ Calculates the yearly costs due to maintenance and operation of the storage technology"""

    __UTC: timezone = timezone('UTC')
    __BERLIN: timezone = timezone('Europe/Berlin')

    def __init__(self, energy_management_data: EnergyManagementData, system_data: SystemData, economic_analysis_config: EconomicAnalysisConfig):
        super().__init__(energy_management_data, system_data, economic_analysis_config)
        self.__annual_relative_o_and_m_costs = economic_analysis_config.annual_realative_o_and_m_costs  # p.u.
        self.__cashflow_list = []
        self.__shorter_than_one_year = True
        #self.__annual_absolut_o_and_m_costs = self.__annual_relative_o_and_m_costs * self._investment_cost  # EUR
        # self.__investment_cost = self._investment_cost

    def get_cashflow(self) -> numpy.ndarray:
        annual_absolute_o_and_m_cost = self.__annual_relative_o_and_m_costs * self._investment_cost
        time = self._energy_management_data.time  # UTC+0

        # calculate number of fractional project years
        total_fractional_years = get_fractional_years(time[0], time[-1])

        # create cashflow list
        self.__cashflow_list = [annual_absolute_o_and_m_cost * (-1)] * int(math.ceil(total_fractional_years))

        # costs for last year scaled down to the time that has passed of that year
        self.__cashflow_list[-1] *= (total_fractional_years - math.floor(total_fractional_years))

        # true_start: float = time[0]  # UTC+0
        # billing_year_date: datetime = self.__get_start_month_in_first_billing_year(true_start)  # UTC+0 get first hour of start month
        # billing_year_start: float = billing_year_date.timestamp()  # UTC+1
        # billing_year_date: datetime = self.__get_next_billing_year(billing_year_date)
        # billing_year_end: float = billing_year_date.timestamp()  # UTC+1
        # # start of fist billing year for calculation of year duration
        # begin_year: float = self.__get_first_hour_of_fist_billing_year(billing_year_start).timestamp() # begin of current year UTC+1
        # duration_first_billing_year = billing_year_end - begin_year  # total time of whole year, in which true_start is
        # if (time[-1]) < billing_year_end:
        #     billing_year_end = time[-1]
        #     self.__shorter_than_one_year = True
        # else:
        #     self.__shorter_than_one_year = False
        #
        # # costs for first year scaled down with factor depending on the starting month
        # factor = - (billing_year_end - billing_year_start) / duration_first_billing_year
        # # iterate through whole simulationtime and add annual costs to array
        # t_last = true_start
        # if self.__shorter_than_one_year == False:
        #     for t in time:
        #         t_last = t
        #         if t >= billing_year_end:  #  t - 3600 because array time is in UTC and billing_year_end is in UTC + 1
        #             self.__cashflow_list.append(factor * annual_absolute_o_and_m_cost)
        #             factor = - 1
        #             billing_year_start = billing_year_end
        #             billing_year_date: datetime = self.__get_next_billing_year(billing_year_date)
        #             billing_year_end: float = billing_year_date.timestamp()
        #     # add remaining costs for the last billing year, but scaled down to the number of started months
        #     billing_year_date: datetime = self.__get_last_month_in_last_billing_year(t_last)  # last month of operation in las billing year
        #     billing_year_end: float = billing_year_date.timestamp()
        #     # duration last year
        #     billing_year_date: datetime = self.__get_next_billing_year(billing_year_date)
        #     end_last_year: float = billing_year_date.timestamp()
        #     duration_last_biling_year = end_last_year - billing_year_start
        #     # costs for last or only year scaled down with factor depending on the end month
        #     factor = (end_last_year - billing_year_start) / duration_last_biling_year
        #     costs_last_year = - factor * annual_absolute_o_and_m_cost
        #     self.__cashflow_list.append(costs_last_year)
        # else:
        #     self.__cashflow_list.append(factor * annual_absolute_o_and_m_cost)
        return numpy.array(self.__cashflow_list)

    def __get_start_month_in_first_billing_year(self, tstmp: float) -> datetime:
        """Returns begin of current month 20xx-xx-01 00:00:00"""
        date = datetime.fromtimestamp(tstmp, tz=self.__BERLIN)
        return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_first_hour_of_fist_billing_year(self, tstmp: float) -> datetime:
        """Returns begin of current year 20xx-01-01 00:00:00"""
        date = datetime.fromtimestamp(tstmp, tz=self.__BERLIN)
        return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_next_billing_year(self, date: datetime) -> datetime:
        """Returns begin of following year 20xx-01-01 00:00:00"""
        return date.replace(year=date.year+1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    def __get_last_month_in_last_billing_year(self, tstmp: float) -> datetime:
        """Returns last day of last month of operation in last billing year"""
        date = datetime.fromtimestamp(tstmp, tz=self.__BERLIN)
        if date.month == 12:
            return date.replace(day=31)
        return date.replace(month=date.month+1, day=1, hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

    def get_evaluation_results(self) -> [EvaluationResult]:
        key_results: [EvaluationResult] = list()
        key_results.append(EvaluationResult(Description.Economical.OperationAndMaintenance.TOTAL_O_AND_M_COST,
                                            Unit.EURO, -1 * sum(self.__cashflow_list)))
        return key_results

    def get_assumptions(self) -> [EvaluationResult]:
        assumptions: [EvaluationResult] = list()
        assumptions.append(EvaluationResult(Description.Economical.OperationAndMaintenance.ANNUAl_O_AND_M_COST,
                                            Unit.EURO, self.__annual_relative_o_and_m_costs * self._investment_cost))
        return assumptions

    def close(self):
        pass

