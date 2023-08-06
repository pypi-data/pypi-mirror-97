import scipy.interpolate

from simses.commons.config.simulation.redox_flow import RedoxFlowConfig
from simses.commons.state.technology.redox_flow import RedoxFlowState
from simses.technology.redox_flow.stack.electrolyte.abstract_electrolyte import ElectrolyteSystem


class VanadiumSystem(ElectrolyteSystem):
    """The parameters of VanadiumSystem are based on experimental data of an electrolyte consisting of 1.6 M Vanadium in
    aqueous sulphuric acid (2 M H2SO4) from GfE (Gesellschaft für Elektrometallurgie mbH)."""

    def __init__(self, capacity: float, redox_flow_config: RedoxFlowConfig):
        super().__init__(capacity)
        self.__max_soc = redox_flow_config.max_soc
        self.__concentration_v = 1600  # mol/m^3
        self.__density_electrolyte = 1334  # kg/m^3
        self.__capacity_density = self.FARADAY * self.__concentration_v / 2

        soc_arr = [0.15, 0.5, 0.85]
        visc_arr_an = [0.0045, 0.0043, 0.0037]
        self.__visc_interp_an = scipy.interpolate.interp1d(soc_arr, visc_arr_an, kind='linear',
                                                           fill_value='extrapolate')
        soc_arr = [0.15, 0.5, 0.85]
        visc_arr_ca = [0.004, 0.0037, 0.0034]
        self.__visc_interp_ca = scipy.interpolate.interp1d(soc_arr, visc_arr_ca, kind='linear',
                                                           fill_value='extrapolate')
        self.__min_viscosity = self.__visc_interp_ca(self.__max_soc)
        self.__max_viscosity = self.__visc_interp_an(0.0)

    def get_viscosity_anolyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        The parameter for the viscosity are based on experimental measurements performed at ZAE Bayern by Lisa Hoffmann.
        Literature source: Hoffmann, Lisa. Physical properties of a VRFB-electrolyte and their impact on the
        cell-performance. MA. RWTH Aachen, 2018.
        """
        soc = redox_flow_state.soc
        viscosity = self.__visc_interp_an(soc)
        return viscosity

    def get_viscosity_catholyte(self, redox_flow_state: RedoxFlowState) -> float:
        """
        The parameter for the viscosity are based on experimental measurements performed at ZAE Bayern by Lisa Hoffmann.
        Literature source: Hoffmann, Lisa. Physical properties of a VRFB-electrolyte and their impact on the
        cell-performance. MA. RWTH Aachen, 2018.
        """
        soc = redox_flow_state.soc
        viscosity = self.__visc_interp_ca(soc)
        return viscosity

    def get_min_viscosity(self):
        return self.__min_viscosity

    def get_max_viscosity(self):
        return self.__max_viscosity

    def get_vanadium_concentration(self) -> float:
        return self.__concentration_v  # mol/m^3

    def get_capacity_density(self) -> float:
        return self.__capacity_density  # As/m^3

    def get_electrolyte_density(self) -> float:
        return self.__density_electrolyte

    def close(self):
        super().close()
