#%%

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from financial_tools import create_financial_matrix, print_profit_summary
from script_utils import BatteryCell, build_fuel_cell_pwl_definition

#%%
np.random.seed(42)

dates = pd.date_range(start="2026-01-01", periods=10, freq="ME")

df1 = pd.DataFrame(
    {
        "Date": dates,
        "Revenue": np.random.uniform(10_000, 50_000, 10).round(2),
        "Expenses": np.random.uniform(5_000, 30_000, 10).round(2),
    }
)
df1["Profit"] = (df1["Revenue"] - df1["Expenses"]).round(2)
#%%
df2 = pd.DataFrame(
    {
        "Date": dates,
        "Revenue": np.random.uniform(15_000, 60_000, 10).round(2),
        "Expenses": np.random.uniform(7_000, 35_000, 10).round(2),
    }
)
df2["Profit"] = (df2["Revenue"] - df2["Expenses"]).round(2)

df3 = pd.DataFrame(
    {
        "Date": dates,
        "Revenue": np.random.uniform(20_000, 70_000, 10).round(2),
        "Expenses": np.random.uniform(10_000, 40_000, 10).round(2),
    }
)
df3["Profit"] = (df3["Revenue"] - df3["Expenses"]).round(2)

df4 = pd.DataFrame(
    {
        "Date": dates,
        "Revenue": np.random.uniform(25_000, 80_000, 10).round(2),
        "Expenses": np.random.uniform(12_000, 45_000, 10).round(2),
    }
)
df4["Profit"] = (df4["Revenue"] - df4["Expenses"]).round(2)

combined_df = (
    df1.set_index("Date")
    .add(df2.set_index("Date"), fill_value=0)
    .reset_index()
)
combined_df["Profit"] = (combined_df["Revenue"] - combined_df["Expenses"]).round(2)

print("DataFrame 1:")
print(df1)
print("\nDataFrame 2:")
print(df2)
print("\nAdded DataFrame:")
print(combined_df)
print_profit_summary(combined_df, "DataFrame 1 + 2")
financial_matrix_12 = create_financial_matrix(combined_df)

combined_df_34 = (
    df3.set_index("Date")
    .add(df4.set_index("Date"), fill_value=0)
    .reset_index()
)
combined_df_34["Profit"] = (combined_df_34["Revenue"] - combined_df_34["Expenses"]).round(2)

print("\nDataFrame 3:")
print(df3)
print("\nDataFrame 4:")
print(df4)
print("\nAdded DataFrame 3 and 4:")
print(combined_df_34)
print_profit_summary(combined_df_34, "DataFrame 3 + 4")
financial_matrix_34 = create_financial_matrix(combined_df_34)

# %%

# Create a 2D engine efficiency map as a 100x100 NumPy array.
rpm_axis = np.linspace(800, 7000, 100)
torque_axis = np.linspace(0, 300, 100)
rpm_grid, torque_grid = np.meshgrid(rpm_axis, torque_axis)

peak_efficiency = 0.42
rpm_center = 3200
torque_center = 180

rpm_shape = np.exp(-((rpm_grid - rpm_center) / 1700) ** 2)
torque_shape = np.exp(-((torque_grid - torque_center) / 95) ** 2)

engine_map_100x100 = 0.18 + peak_efficiency * rpm_shape * torque_shape

low_load_penalty = 0.10 * np.exp(-(torque_grid / 45) ** 2)
high_speed_penalty = 0.08 * np.clip((rpm_grid - 5500) / 1500, 0, 1)
engine_map_100x100 = engine_map_100x100 - low_load_penalty - high_speed_penalty
engine_map_100x100 = np.clip(engine_map_100x100, 0.05, 0.45)

#%%

print("Engine map shape:", engine_map_100x100.shape)
print(engine_map_100x100)

plt.figure(figsize=(9, 6))
heatmap = plt.imshow(
    engine_map_100x100,
    origin="lower",
    aspect="auto",
    extent=[rpm_axis.min(), rpm_axis.max(), torque_axis.min(), torque_axis.max()],
    cmap="viridis",
)
plt.colorbar(heatmap, label="Efficiency")
plt.contour(
    rpm_axis,
    torque_axis,
    engine_map_100x100,
    levels=8,
    colors="white",
    linewidths=0.7,
    alpha=0.75,
)
plt.title("2D Engine Efficiency Map (Efficiency in Decimal)")
plt.xlabel("Engine Speed (RPM)")
plt.ylabel("Torque (Nm)")
plt.tight_layout()
plt.show()

# TODO: call the battery function here.
battery_cell = BatteryCell(capacity_ah=100, chemistry="NMC")
battery_cell.summary()

# One main call for the PWL definition (from the fuel-cell MILP curve).
pwl_definition = build_fuel_cell_pwl_definition(p_min=10, p_max=100, segments=4)
print("\nFuel-cell PWL definition:")
print("Breakpoints [kW]:", np.round(pwl_definition["breakpoints_kw"], 2))
print("Slopes beta [kg/h per kW]:", np.round(pwl_definition["slopes_beta"], 4))
print("Intercepts alpha [kg/h]:", np.round(pwl_definition["intercepts_alpha"], 4))