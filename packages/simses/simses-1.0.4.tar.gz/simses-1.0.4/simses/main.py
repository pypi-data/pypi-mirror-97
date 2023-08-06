import os
import threading
from configparser import ConfigParser
from multiprocessing import Queue

from simses.analysis.storage import StorageAnalysis
from simses.commons.config.log import LogConfig
from simses.commons.state.system import SystemState
from simses.commons.utils.utilities import create_directory_for
from simses.simulation.simulator import StorageSimulation


class SimSES(threading.Thread):

    """
    SimSES is a simulation and analysis tool for complex energy storage systems. The tool can be used via the run method
    (or alternatively as a Thread with its start method). The simulation and analysis can be run separately, the
    analysis takes the results of the last run from the configured simulation.

    SimSES can be configured via the INI files in config. DEFAULT configs (*.defaults.ini) can be overwritten by
    LOCAL configs (*.local.ini). Furthermore, the configs can be overwritten by a ConfigParser passed to the SimSES
    constructor. This is especially useful for sensitivity analysis.

    The processing package provides a functionality for multiple simulations and analysis by using all available cores.
    For this purpose, python's multiprocessing package is used. An example as well as a readme is provided in the
    processing package how to use and configure it.

    SimSES can also be used directly in other tools by providing the run_one_simulation_step and
    evaluate_multiple_simulation_steps methods. With these methods SimSES can be integrated in other simulation
    frameworks acting as a storage system. SimSES needs to be closed manually after the simulation from outer scope is
    completed.
    """

    def __init__(self, path: str, name: str, do_simulation: bool = True, do_analysis: bool = True,
                 simulation_config: ConfigParser = None, analysis_config: ConfigParser = None, queue: Queue = None,
                 batch_dir: str = 'batch/'):
        """
        Constructor of SimSES

        Parameters
        ----------
        path :
            absolute path where to store results
        name :
            simulation name (will be concatenated with path to a unique path)
        do_simulation :
            flag for allowing or prohibiting execution of the simulation
        do_analysis :
            flag for allowing or prohibiting execution of the analysis
        simulation_config :
            ConfigParser overwriting configuration provided by INI files for simulation
        analysis_config :
            ConfigParser overwriting configuration provided by INI files for analysis
        queue :
            PrinterQueue provides progess information for the user in case of using the processing package
        batch_dir :
            Relative path of directory for comparison of results from multiple simulations using the processing package
        """
        super().__init__()
        self.__do_simulation = do_simulation
        self.__do_analysis = do_analysis
        self.__name: str = name
        batch_dir = path + batch_dir
        path = path + name + '/'
        if self.__do_simulation:
            create_directory_for(path)
            self.__storage_simulation: StorageSimulation = StorageSimulation(path, simulation_config, queue)
        if self.__do_analysis:
            self.__storage_analysis: StorageAnalysis = StorageAnalysis(path, analysis_config, batch_dir)

    @property
    def name(self) -> str:
        """
        Returns
        -------
        str:
            string representation of the simulation name
        """
        return self.__name

    def run(self) -> None:
        """
        Runs the configured simulation and analysis and closes afterwards
        """
        self.run_simulation()
        self.run_analysis()
        self.close()

    def run_one_simulation_step(self, time: float, power: float = None) -> None:
        """
        Runs only one step of the simulation with the given time and power. The system is configured as mentioned
        in the class description.

        If no power value is provided, the configured energy management system will provide a power value for
        the given time.

        Calculated values can be received via the state property. It provides information about the whole
        storage system, e.g. SOC.

        Parameters
        ----------
        time :
            epoch timestamp in s
        power :
            power value in W
        """
        self.__storage_simulation.run_one_step(ts=time, power=power)

    def evaluate_multiple_simulation_steps(self, start: float, timestep: float, power: list) -> [SystemState]:
        """
        Runs multiple steps of the simulation with the given start time, timestep and power list. The system is
        configured as mentioned in the class description.

        If no power list is provided, the simulation will not be advanced.

        Calculated values will be returned. They provide information about the whole storage system, e.g. SOC,
        for each timestep.

        Parameters
        ----------
        start :
            start time in s
        timestep :
            timestep in s
        power :
            list of power for each timestep in W

        Returns
        ----------
        list:
            Returns a list of system states for each timestep
        """
        return self.__storage_simulation.evaluate_multiple_steps(start, timestep, power)

    def run_simulation(self) -> None:
        """
        Runs only the simulation as configured, if allowed
        """
        if self.__do_simulation:
            self.__storage_simulation.run()

    def run_analysis(self) -> None:
        """
        Runs only the analysis as configured, if allowed
        """
        if self.__do_analysis:
            self.__storage_analysis.run()

    @property
    def state(self) -> SystemState:
        """
        Usage only supported in combination with run_one_simulation_step

        Returns
        -------
        SystemState:
            current state of the system providing information of calculated results
        """
        return self.__storage_simulation.state

    def close(self) -> None:
        """
        Closes all resources of simulation and analysis
        """
        self.close_simulation()
        self.close_analysis()

    def close_simulation(self) -> None:
        """
        Closes all resources of simulation
        """
        if self.__do_simulation:
            self.__storage_simulation.close()

    def close_analysis(self) -> None:
        """
        Closes all resources of analysis
        """
        if self.__do_analysis:
            self.__storage_analysis.close()

    @classmethod
    def set_log_config(cls, configuration: ConfigParser) -> None:
        """
        Class method for setting the global log configuration

        Parameters
        ----------
        configuration :
            ConfigParser will overwrite global log configuration
        """
        LogConfig.set_config(configuration)


if __name__ == "__main__":
    # minimum working example
    # config_generator: SimulationConfigGenerator = SimulationConfigGenerator()
    # config_generator.set_simulation_time('2014-01-01 00:00:00', '2014-02-01 00:00:00')
    # config: ConfigParser = config_generator.get_config()
    path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    result_path: str = os.path.join(path, 'results').replace('\\','/') + '/'
    simulation_name: str = 'simses_1'
    simses: SimSES = SimSES(result_path, simulation_name, do_simulation=True, do_analysis=True)
    # simses: SimSES = SimSES(result_path, simulation_name, do_simulation=True, do_analysis=True, simulation_config=config)
    simses.start()
    simses.join()
