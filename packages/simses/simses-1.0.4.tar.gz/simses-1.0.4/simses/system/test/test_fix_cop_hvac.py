from configparser import ConfigParser
import pytest
from simses.commons.config.simulation.system import StorageSystemConfig
from simses.system.auxiliary.heating_ventilation_air_conditioning.fix_cop_hvac import \
    FixCOPHeatingVentilationAirConditioning


class TestFixCOPHeatingVentilationAirConditioning:

    # Ensure if path from simulation.defaults.ini to ambient temperature model works
    hvac_model_config: ConfigParser = ConfigParser()
    hvac_model_config.add_section('STORAGE_SYSTEM')
    hvac_model_config.set('STORAGE_SYSTEM', 'HVAC', 'constant_hvac,FixCOPHeatingVentilationAirConditioning,5000,25')
    storage_system_config = StorageSystemConfig(hvac_model_config)
    hvac = 'constant_hvac'
    hvac_model = storage_system_config.hvac[hvac][StorageSystemConfig.HVAC_TYPE]
    hvac_configuration = storage_system_config.hvac[hvac]

    tests_set_point_deviation = 20  # °C
    air_mass = 50000  # in kg
    air_specific_heat = 1006  # J/kgK

    max_thermal_power: int = int(storage_system_config.hvac[hvac][StorageSystemConfig.HVAC_POWER])  # in W
    set_point_temperature: int = int(storage_system_config.hvac[hvac][StorageSystemConfig.HVAC_TEMPERATURE_SETPOINT])  # in °C
    temperature_range = list(range(set_point_temperature - tests_set_point_deviation, set_point_temperature + tests_set_point_deviation, 1))

    def create_model(self):
        if self.hvac_model == FixCOPHeatingVentilationAirConditioning.__name__:
            return FixCOPHeatingVentilationAirConditioning(self.hvac_configuration)

    @pytest.mark.parametrize("temperature_value", temperature_range)
    def test_run_air_conditioning(self, temperature_value):
        uut: FixCOPHeatingVentilationAirConditioning = self.create_model()
        uut.update_air_parameters(self.air_mass,self.air_specific_heat)  # Dummy value for mass of air
        uut.run_air_conditioning([[temperature_value + 273.15]], 0)
        assert abs(uut.get_thermal_power()) <= self.max_thermal_power
        if uut.get_thermal_power() <= 0:
            assert abs(uut.get_thermal_power()/uut.get_scop()) == uut.get_electric_power()
        else:
            assert abs(uut.get_thermal_power()/uut.get_seer()) == uut.get_electric_power()
