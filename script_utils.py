"""Small utility functions for simple battery modeling."""

import numpy as np


def soc_after_discharge(initial_soc, current_a, hours, capacity_ah):
    """Return SOC after discharging for a given time.

    SOC is represented in range [0.0, 1.0].
    """
    if capacity_ah <= 0:
        raise ValueError("capacity_ah must be > 0")
    used_ah = current_a * hours
    next_soc = initial_soc - (used_ah / capacity_ah)
    return max(0.0, min(1.0, next_soc))


def estimate_terminal_voltage(ocv_v, current_a, internal_resistance_ohm):
    """Estimate terminal voltage using a basic R-int model."""
    return ocv_v - (current_a * internal_resistance_ohm)


def estimate_energy_wh(nominal_voltage_v, capacity_ah):
    """Estimate nominal stored energy in Wh."""
    if nominal_voltage_v < 0 or capacity_ah < 0:
        raise ValueError("nominal_voltage_v and capacity_ah must be >= 0")
    return nominal_voltage_v * capacity_ah


class BatteryCell:
    """Small battery object for quick experiments."""

    def __init__(
        self,
        capacity_ah,
        chemistry="NMC",
        nominal_voltage_v=3.7,
        internal_resistance_ohm=0.02,
    ):
        if capacity_ah <= 0:
            raise ValueError("capacity_ah must be > 0")
        self.capacity_ah = float(capacity_ah)
        self.chemistry = chemistry
        self.nominal_voltage_v = float(nominal_voltage_v)
        self.internal_resistance_ohm = float(internal_resistance_ohm)
        self.soc = 1.0

    def discharge(self, current_a, hours):
        """Update SOC after a discharge step and return new SOC."""
   
   
        self.soc = soc_after_discharge(self.soc, current_a, hours, self.capacity_ah)
        return self.soc

    def terminal_voltage(self, current_a):
        """Estimate terminal voltage at current SOC and load current."""
        ocv_v = self.nominal_voltage_v * (0.9 + 0.1 * self.soc)
        return estimate_terminal_voltage(ocv_v, current_a, self.internal_resistance_ohm)

    def energy_wh(self):
        """Return remaining energy estimate in Wh."""
        full_energy = estimate_energy_wh(self.nominal_voltage_v, self.capacity_ah)
        return full_energy * self.soc

    def summary(self):
        """Print a short battery status summary."""
        print(
            f"BatteryCell({self.chemistry}) | "
            f"capacity={self.capacity_ah:.1f}Ah | "
            f"SOC={self.soc:.1%} | "
            f"energy={self.energy_wh():.1f}Wh"
        )


def build_fuel_cell_pwl_definition(
    p_min=10.0,
    p_max=100.0,
    segments=4,
    a=0.690,
    b=0.0286,
    c=0.000245,
):
    """Create one PWL definition for H2(P)=a+bP+cP^2 on [p_min, p_max].

    Returns a dictionary with breakpoints and segment line parameters:
    - breakpoints_kw: x_k
    - h2_values_kgph: y_k
    - slopes_beta: beta_k
    - intercepts_alpha: alpha_k where alpha_k = y_{k-1} - beta_k * x_{k-1}
    """
    if segments < 1:
        raise ValueError("segments must be >= 1")
    if p_max <= p_min:
        raise ValueError("p_max must be greater than p_min")

    def h2_curve(power_kw):
        return a + b * power_kw + c * (power_kw ** 2)

    breakpoints = np.linspace(p_min, p_max, segments + 1)
    h2_values = h2_curve(breakpoints)
    slopes = (h2_values[1:] - h2_values[:-1]) / (breakpoints[1:] - breakpoints[:-1])
    intercepts = h2_values[:-1] - slopes * breakpoints[:-1]

    return {
        "breakpoints_kw": breakpoints,
        "h2_values_kgph": h2_values,
        "slopes_beta": slopes,
        "intercepts_alpha": intercepts,
        "segments": segments,
        "p_min": p_min,
        "p_max": p_max,
        "coeff_a": a,
        "coeff_b": b,
        "coeff_c": c,
   
    }


# Comment 1

# comment 2