from configparser import ConfigParser

import pandas
import pytest

from simses.analysis.data.system import SystemData
from simses.analysis.evaluation.technical.technical_evaluation import *
from simses.commons.config.analysis.general import GeneralAnalysisConfig
from simses.commons.config.simulation.general import GeneralSimulationConfig
from simses.commons.state.system import SystemState


def create_analysis_config():
    analysis_config: ConfigParser = ConfigParser()
    return GeneralAnalysisConfig(config=analysis_config)

timestep = 1
n = 2
yearstart = 2020

def create_general_config() -> GeneralSimulationConfig:
    simulation_config: ConfigParser = ConfigParser()
    simulation_config.add_section('GENERAL')
    simulation_config.set('GENERAL', 'TIME_STEP', str(timestep))

    return GeneralSimulationConfig(simulation_config)

# build configs for testing
gen_sim_config = create_general_config()
analysis_config = create_analysis_config()

dstart = datetime(yearstart, 1, 1).timestamp()
time_test = pandas.array([dstart + timestep * i for i in range(n)])

# Round-trip efficiency:
@pytest.mark.parametrize('storage_power, soc, result',
                          [
                              ([0, -3600 * 10],     [0.1, 0.09],    100),   # only one-way discharged, 100%
                              ([0, 3600*10],        [0, 0.005],     50),    # only one-way charged, 50%
                              ([3600*10, -3600 * 10], [0, 0],      100),   # round trip, 100%, no soc-change
                              ([3600*10, -1800*10], [0, 0],      50),      # round-trip, 50%, no soc-change
                              ([3600 * 10, -1800 * 10], [0, 0.005], 100),  # round trip, 100%, soc-change
                              ([3600 * 10, -1800 * 10], [0, 0.0025], 71.076758)  # round-trip, 50%, soc-change
                          ]
                         )
def test_round_trip_efficiency(storage_power, soc, result):

    capacity = [1000, 1000]
    system_dict = {SystemState.TIME: time_test, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.SOC: soc, SystemState.CAPACITY: capacity,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.round_trip_efficiency - result) <= 1e-5


# Capacity_remaining:
@pytest.mark.parametrize('soh, result',
                          [
                              ([0, 0], 0),
                              ([0, 0.5], 50),
                              ([0, -1], -100),
                              ([0, 2], 200)
                          ]
                         )
def test_capacity_remaining(soh, result):

    system_dict = {SystemState.TIME: time_test, SystemState.SOH: soh,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.capacity_remaining - result) <= 1e-5

# Energy_throughput:
@pytest.mark.parametrize('storage_power, result',
                          [
                                ([0, -3600 * 10], 0.01),
                                ([0, 3600 * 10], 0.01),
                                ([3600 * 10, 3600 * 10], 0.02),
                                ([0, 0], 0)
                          ]
                         )
def test_energy_throughput(storage_power, result):

    system_dict = {SystemState.TIME: time_test, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.energy_throughput - result) <= 1e-5

# Mean_SOC:
@pytest.mark.parametrize('soc, result',
                          [
                                ([0, 0], [0, 0, 0]),
                                ([0.1, 0.2], [10, 15, 20]),
                                ([1, 0], [0, 50, 100]),
                          ]
                         )
def test_mean_soc(soc, result):

    system_dict = {SystemState.TIME: time_test, SystemState.SOC: soc,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert all(abs(i) <= 1e-5 for i in [sum(x) for x in zip(uut.mean_soc, np.negative(result))])

# FEC:
@pytest.mark.parametrize('storage_power, capacity, result',
                          [
                                ([0, 0], [10, 10], 0),
                                ([0, 3600 * 10], [10, 10], 1),
                                ([0, -3600 * 10], [10, 10], 0), # discharging is not considered
                          ]
                         )
def test_equivalent_full_cycles(storage_power, capacity, result):

    system_dict = {SystemState.TIME: time_test, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.CAPACITY: capacity,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.equivalent_full_cycles - result) <= 1e-5


# Depth of Discharges:
@pytest.mark.parametrize('soc, result',
                          [
                                ([0.8, 0.3, 0.3, 0.3, 0.3, 0.3], 50),
                                ([0.2, 0.2, 0.3, 0.3, 0.3, 0.3], 0), # no discharge
                                ([0.6, 0.4, 0.3, 0.3, 0.3, 0.3], 30),
                                ([0.6, 0.4, 0.6, 0.4, 0.6, 0.4], 20),
                                ([0.6, 0.4, 0.6, 0.6, 0.6, 0.2], 30),
                                ([0.6, 0.0, 1.0, 0.4, 0.8, 0.2], 60),
                                ([1.0, 0.99, 0.98, 1.0, 0.99, 1.0], 1.5),
                          ]
                         )
def test_depth_of_discharges(soc, result):
    n_temp = 6
    time_test_temp = pandas.array([dstart + timestep * i for i in range(n_temp)])
    system_dict = {SystemState.TIME: time_test_temp, SystemState.SOC: soc,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.depth_of_discharges - result) <= 1e-5


# Changes_of_sign:
@pytest.mark.parametrize('storage_power, result',
                          [
                                ([0, 0, 0, 0], 0),
                                ([0, -1, 0, 0], 0), # 0 is not a change of sign
                                ([0, 0, 1, 0], 0), # 0 is not a change of sign
                                ([0, 1, -1, 0], 1/3), # if 3,00003 days -> method rounds to three days
                                ([-1, 1, -1, 1], 1),
                                ([1, 1, 1, -1], 1/3)
                          ]
                         )
def test_changes_of_sign(storage_power, result):
    timestep_temp = 60*60*24+1
    n_temp = 4
    time_test_temp = pandas.array([dstart + timestep_temp * i for i in range(n_temp)])

    system_dict = {SystemState.TIME: time_test_temp, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.changes_of_sign - result) <= 1e-5

# Resting times:
@pytest.mark.parametrize('storage_power, result',
                          [
                                ([0, 0, 0, 0, 0, 0], 6/60), # resting times in minutes
                                ([0, 0, 1, 0, 0, 0], 2.5/60),
                                ([0, 0, 1, 1, 0, 0], 2/60),
                                ([1, -1, -1, 1, 1, 1], 'Never in resting mode'),
                                ([-1, 1, -1, 1, 1, 0], 1/60),
                                ([0, 1, 0, -1, 0, 1], 1/60)
                          ]
                         )
def test_resting_times(storage_power, result):
    n_temp = 6
    time_test_temp = pandas.array([dstart + timestep * i for i in range(n_temp)])
    system_dict = {SystemState.TIME: time_test_temp, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    if result is float:
        assert abs(uut.resting_times - result) <= 1e-5
    elif result is str:
        assert type(uut.resting_times) == str


# Energy_swapsign:
@pytest.mark.parametrize('storage_power, capacity, result',
                          [
                                ([0, 0, 0, 0, 0, 0], [10, 10, 10, 10, 10, 10], 'No energy was charged'),
                                ([0, 3600 * 10, 0, 0, 0, 0], [10, 10, 10, 10, 10, 10], 100),
                                ([-100, 3600 * 10, -100, -200, 3600 * 10, 0], [10, 10, 10, 10, 10, 10], 100),
                                ([-100, 3600 * 10, -100, 3600 * 10 *3, 0, 0], [10, 10, 10, 10, 10, 10], 200),
                                ([0, 3600 * 10, 3600 * 10, 0, 0, 0], [10, 10, 10, 10, 10, 10], 200),
                                ([0, 3600 * 10, 0, 3600 * 10, 0, 3600 * 10], [10, 10, 10, 10, 10, 10], 300),
                                ([3600 * 10, 3600 * 10, 0, 3600 * 10, 0, 3600 * 10], [10, 10, 10, 10, 10, 10], 400),
                                ([-100, 3600 * 10, 0, 3600 * 10, 0, -100], [10, 10, 10, 10, 10, 10], 200),
                          ]
                         )
def test_energy_swapsign(storage_power, capacity, result):
    n_temp = 6
    time_test_temp = pandas.array([dstart + timestep * i for i in range(n_temp)])
    system_dict = {SystemState.TIME: time_test_temp, SystemState.AC_POWER_DELIVERED: storage_power,
                   SystemState.CAPACITY: capacity,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    if isinstance(result, (int, float, complex)) and not isinstance(result, bool):
        assert abs(uut.energy_swapsign - result) <= 1e-5
    elif result is str:
        assert type(uut.energy_swapsign) == str


# average_fulfillment.
@pytest.mark.parametrize('storage_fulfillment, result',
                          [
                              ([0, 0], 0),
                              ([1, 1], 100),
                              ([0, 1], 50)
                          ]
                         )
def test_average_fulfillment(storage_fulfillment, result):

    system_dict = {SystemState.TIME: time_test, SystemState.FULFILLMENT: storage_fulfillment,
                   SystemState.SYSTEM_AC_ID: 1, SystemState.SYSTEM_DC_ID: 1}
    system_data = SystemData(gen_sim_config, pandas.DataFrame(system_dict))

    uut = TechnicalEvaluation(system_data, analysis_config)
    assert abs(uut.average_fulfillment - result) <= 1e-5
