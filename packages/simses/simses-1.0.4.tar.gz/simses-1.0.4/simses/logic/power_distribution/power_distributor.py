from abc import ABC, abstractmethod

from simses.commons.state.system import SystemState


class PowerDistributor(ABC):

    """
    PowerDistributor incorporates a logic on how to distribute power between several systems. The logic is based on the
    system state of each system.
    """

    def __init__(self):
        super().__init__()
        # self._max_system_power: dict = dict()

    @abstractmethod
    def set(self, time: float, states: [SystemState]) -> None:
        """
        Setting information from all system states necessary for the PowerDistributor

        Parameters
        ----------
        states :
            list of current system states
        time :
            current simulation time as epoch time
        """
        pass

    @abstractmethod
    def get_power_for(self, power: float, state: SystemState) -> float:
        """
        Calculates the power share of the overall to be distributed power to a specific system specified with system state

        Parameters
        ----------
        power :
            overall power to be distributed to all systems
        state :
            system state of system to calculate a specific power share of power

        Returns
        -------
        float:
            power share of specified system with corresponding system state
        """
        pass

    # def set_max_system_power_for(self, ac_system_id: int, max_power: float) -> None:
    #     self._max_system_power[ac_system_id] = max_power

    def close(self):
        pass
