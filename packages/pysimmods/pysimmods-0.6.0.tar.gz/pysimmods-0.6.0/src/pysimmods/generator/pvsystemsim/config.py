"""This module contains the config model of the PV plant system."""
import math

from pysimmods.other.invertersim.config import InverterConfig
from pysimmods.model.config import ModelConfig
from pysimmods.generator.pvsim.config import PVConfig


class PVSystemConfig(ModelConfig):
    """Config parameters of the PV plant System.

    Consists of a :class:`~.PVConfig` and an :class:`~.InverterConfig`
    object.

    """

    def __init__(self, params):
        super().__init__(params)
        params["pv"]["sign_convention"] = self.sign_convention
        params["inverter"]["sign_convention"] = self.sign_convention

        self.pv = PVConfig(params["pv"])
        self.inverter = InverterConfig(params["inverter"])

    @property
    def p_min_kw(self):
        """Minimum active power of pv system in kW, this property is
        used by :class:`.mosaik.flexibility_model.FlexibilityModel`.

        With passive sign convention, this is the maximum power this
        plant can generate.

        """
        if self.psc:
            return self._get_abs_p_max()
        else:
            return 0

    @property
    def p_max_kw(self):
        """Maximum active power of pv plant in kW, this property is
        used by :class:`.mosaik.flexibility_model.FlexibilityModel`.

        With active sign convention, this is the maximum power this
        plant can generate

        """
        if self.psc:
            return 0
        else:
            return self._get_abs_p_max()

    @property
    def q_min_kvar(self):
        """Minimum reactive power of pv plant in kVAr.

        For certain combinations, this is the maximum absolute power
        this plant can generate.

        """
        if self.psc and self.inverter.inverter_mode == "capacitive":
            return self._get_abs_q_max()
        elif self.asc and self.inverter.inverter_mode == "inductive":
            return self._get_abs_q_max()
        else:
            return 0

    @property
    def q_max_kvar(self):
        """Maximum reactive power of pv plant in kVAr.

        For certain combinations, this is the maximum absolute power
        this plant can generate.

        """
        if self.psc and self.inverter.inverter_mode == "inductive":
            return self._get_abs_q_max()
        elif self.asc and self.inverter.inverter_mode == "capacitive":
            return self._get_abs_q_max()
        else:
            return 0

    @property
    def default_schedule(self):
        return self.pv.default_schedule

    def _get_abs_p_max(self):
        if self.pv.p_peak_kw > self.inverter.sn_kva:
            return self.inverter.sn_kva * self.gsign
        else:
            return self.pv.p_peak_kw * self.gsign

    def _get_abs_q_max(self):
        const_cos_phi_modes = ["p_set", "q_set"]
        variable_cos_phi_modes = ["cos_phi_set", "pq_set", "qp_set"]

        if self.inverter.q_control in const_cos_phi_modes:
            q_max_kvar = self.inverter.sn_kva * math.sin(
                math.acos(self.inverter.cos_phi)
            )

            return q_max_kvar * self.gsign

        elif self.inverter.q_control in variable_cos_phi_modes:
            return self.inverter.sn_kva * self.gsign

        else:
            return 0
