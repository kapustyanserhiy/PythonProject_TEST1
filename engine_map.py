import numpy as np
import matplotlib.pyplot as plt


def create_engine_map(size=100):
    """
    Create a 2D engine efficiency map.

    Returns:
        rpm_axis: 1D array with engine speed values [rpm]
        torque_axis: 1D array with torque values [Nm]
        engine_map: 2D NumPy array with shape (size, size)
    """
    rpm_axis = np.linspace(800, 7000, size)
    torque_axis = np.linspace(0, 300, size)

    rpm_grid, torque_grid = np.meshgrid(rpm_axis, torque_axis)

    peak_efficiency = 0.42
    rpm_center = 3200
    torque_center = 180

    rpm_shape = np.exp(-((rpm_grid - rpm_center) / 1700) ** 2)
    torque_shape = np.exp(-((torque_grid - torque_center) / 95) ** 2)

    engine_map = 0.18 + peak_efficiency * rpm_shape * torque_shape

    # Penalize very low load and very high speed regions.
    low_load_penalty = 0.10 * np.exp(-(torque_grid / 45) ** 2)
    high_speed_penalty = 0.08 * np.clip((rpm_grid - 5500) / 1500, 0, 1)
    engine_map = engine_map - low_load_penalty - high_speed_penalty

    return rpm_axis, torque_axis, np.clip(engine_map, 0.05, 0.45)


def plot_engine_map(rpm_axis, torque_axis, engine_map):
    plt.figure(figsize=(9, 6))
    heatmap = plt.imshow(
        engine_map,
        origin="lower",
        aspect="auto",
        extent=[rpm_axis.min(), rpm_axis.max(), torque_axis.min(), torque_axis.max()],
        cmap="viridis",
    )
    plt.colorbar(heatmap, label="Efficiency")
    plt.contour(
        rpm_axis,
        torque_axis,
        engine_map,
        levels=8,
        colors="white",
        linewidths=0.7,
        alpha=0.75,
    )
    plt.title("2D Engine Efficiency Map")
    plt.xlabel("Engine speed [rpm]")
    plt.ylabel("Torque [Nm]")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    rpm, torque, engine_map_100x100 = create_engine_map(size=100)

    print("Engine map shape:", engine_map_100x100.shape)
    print(engine_map_100x100)

    plot_engine_map(rpm, torque, engine_map_100x100)
