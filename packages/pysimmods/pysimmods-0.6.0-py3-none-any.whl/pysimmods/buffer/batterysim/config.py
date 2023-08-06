"""This module contains the config model for the battery model."""
from pysimmods.model.config import ModelConfig


class BatteryConfig(ModelConfig):
    """Captures the configuration parameters of the battery model

    On intitialization a dictionay with values for all configuration
    parameters has to be passed.

    The configuration parameters are constant during the simulation
    process. That is they are not manipulated in the step-method of
    the battery model and should not be changed during simulation
    from outside.

    Attributes
    ----------
    cap_kwh : float
        Capacity of the battery in [kWh].
    p_charge_max_kw : float
        Maximum charging (consumption) power of battery in [kW].
    p_discharge_max_kw : float
        Maximum discharging (generation) power of battery in [kW].
    soc_min_percent : float
        Minimum state of charge of battery in [%] of capacity.
    eta_pc : list
        Polynomial coefficients for calculating set power dependent eta.
    """

    def __init__(self, params):
        super().__init__(params)

        self.cap_kwh = abs(params["cap_kwh"])
        self.p_charge_max_kw = abs(params["p_charge_max_kw"])
        self.p_discharge_max_kw = abs(params["p_discharge_max_kw"])
        self.soc_min_percent = params["soc_min_percent"]
        self.eta_pc = params["eta_pc"]

        self._default_schedule = [
            50,
            59.451814,
            60,
            60,
            60,
            60,
            50,
            50,
            50,
            35,
            35,
            35,
            35,
            50,
            50,
            70,
            70,
            50,
            35,
            35,
            50,
            51,
            51,
            54,
        ]

    @property
    def p_min_kw(self):
        """Minimum power of battery in kW, this property is used by
        :meth:`.model.Model.get_sample`

        """
        if self.psc:
            return self.p_discharge_max_kw * self.gsign
        else:
            return self.p_charge_max_kw * self.lsign

    @property
    def p_max_kw(self):
        """Maximum power of battery in kW, this property is used by
        :meth:`.model.Model.get_sample`

        """
        if self.psc:
            return self.p_charge_max_kw * self.lsign
        else:
            return self.p_discharge_max_kw * self.gsign

    @property
    def q_min_kvar(self):
        """Needs to be implemented."""
        return 0

    @property
    def q_max_kvar(self):
        """Needs to be implemented."""
        return 0
