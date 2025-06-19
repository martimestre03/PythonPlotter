
import serial
import matplotlib.pyplot as plt
import time
import numpy as np

SERIAL_PORT = "COM5"
BAUD_RATE = 115200
SAMPLING_PERIOD = 0.01  # 100Hz = 10ms per sample

def open_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.001)
        print(f"Connected to {SERIAL_PORT}")
        return ser
    except serial.SerialException as e:
        print(f"Error: {e}")
        exit()

def rolling_average(data, window_size=5):
    cumsum = np.cumsum(np.insert(data, 0, 0))  # cumulative sum
    result = (cumsum[window_size:] - cumsum[:-window_size]) / window_size
    # Pad the beginning to keep same length
    padding = [result[0]] * (window_size - 1)
    return np.array(padding + list(result))

def capture_data(duration=30):
    ser = open_serial()
    time_data, button_data = [], []
    ax_data, ay_data, az_data = [], [], []
    gx_data, gy_data, gz_data = [], [], []
    total_accel_data = []
    button_fall_events = []
    sample_index = 0
    last_button = None
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            while ser.in_waiting:
                line = ser.readline().decode("utf-8", errors="ignore").strip()
                if not line or line.startswith("millis"):
                    continue
                parts = line.split(',')
                if len(parts) < 8:
                    continue

                try:
                    gx, gy, gz = map(float, parts[1:4])
                    ax, ay, az = map(float, parts[4:7])
                    button = int(parts[7])
                except ValueError:
                    continue

                t = sample_index * SAMPLING_PERIOD
                sample_index += 1

                time_data.append(t)
                ax_data.append(ax)
                ay_data.append(ay)
                az_data.append(az)
                gx_data.append(gx)
                gy_data.append(gy)
                gz_data.append(gz)
                button_data.append(button)

                # Custom accel calculation
                total_accel = (ay**2 + (az + 1)**2 - gx/100)
                total_accel_data.append(total_accel)

                if last_button == 1 and button == 0:
                    button_fall_events.append(t)

                last_button = button

        except Exception as e:
            print("Error during serial read:", e)
            continue

    # Apply rolling window of 5 to total_accel
    # Apply rolling window of 5 to total_accel (continuous version)
    filtered_total_accel = rolling_average(total_accel_data, window_size=5)

    return {
        "time": np.array(time_data),
        "ax": np.array(ax_data),
        "ay": np.array(ay_data),
        "az": np.array(az_data),
        "gx": np.array(gx_data),
        "gy": np.array(gy_data),
        "gz": np.array(gz_data),
        "button": np.array(button_data),
        "total_accel": np.array(total_accel_data),
        "filtered_total_accel": filtered_total_accel,
        "button_fall_events": button_fall_events
    }

def plot_data(data):
    fig, axs = plt.subplots(4, 1, figsize=(14, 12), sharex=True)

    axs[0].plot(data["time"], data["ax"], label="Ax", color='red')
    axs[0].plot(data["time"], data["ay"], label="Ay", color='blue')
    axs[0].plot(data["time"], data["az"], label="Az", color='green')
    axs[0].set_ylabel("Accel (g)")
    axs[0].legend()
    axs[0].grid()

    axs[1].plot(data["time"], data["gx"], label="Gx", color='orange')
    axs[1].plot(data["time"], data["gy"], label="Gy", color='purple')
    axs[1].plot(data["time"], data["gz"], label="Gz", color='cyan')
    axs[1].set_ylabel("Gyro (°/s)")
    axs[1].legend()
    axs[1].grid()

    axs[2].plot(data["time"], data["filtered_total_accel"], label="Total Accel", color='brown')
    axs[2].set_ylabel("Total Accel (g)")
    axs[2].legend()
    axs[2].grid()

    # axs[3].plot(data["time"], data["button"], label="Button", color='black')
    # axs[3].set_ylabel("Button State")
    # axs[3].set_xlabel("Time (s)")
    # axs[3].set_ylim(-0.2, 1.2)
    # axs[3].legend()
    # axs[3].grid()

    # Add vertical lines for button fall (1 → 0)
    for t_event in data["button_fall_events"]:
        for ax in axs:
            ax.axvline(x=t_event, color='red', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    input("🔁 Press Enter to start 30s recording (button falling edge triggers)...")
    recorded_data = capture_data()
    plot_data(recorded_data)

