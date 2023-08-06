from simses.system.thermal.solar_irradiation.solar_irradiation_model import SolarIrradiationModel


class NoSolarIrradiationModel(SolarIrradiationModel):
    """
        NoSolarIrradiationModel returns a value of 0.0 for the thermal load due to the solar irradiation
        """

    def __init__(self):
        super().__init__()
        pass

    def get_heat_load(self, time_stamp) -> float:
        return 0.0  # Not applicable

    def get_global_horizontal_irradiance(self,time_step) -> float:
        return 0.0  # Not applicable
