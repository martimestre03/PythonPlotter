# 📊 Serial IMU Data Logger & Visualizer 🚀

This Python script lets you capture and visualize data from an IMU sensor (accelerometer + gyroscope) over a serial connection. It also tracks button press events and highlights them on the graph!

---

## ✨ Features

✅ Connects to your device via a serial port (e.g., ESP32)  
✅ Logs accelerometer (ax, ay, az) and gyroscope (gx, gy, gz) data  
✅ Tracks button fall events (when button changes from 1 ➡️ 0)  
✅ Computes a custom total acceleration signal  
✅ Applies a rolling average filter to smooth out noise  
✅ Displays beautiful real-time plots with vertical lines for button events

---

## 🛠️ Requirements

- Python 3.x
- `pyserial`
- `numpy`
- `matplotlib`

📦 Install with:

```
pip install pyserial numpy matplotlib
```

---

## ▶️ How to Use

1. Edit the script and set your COM port:
   ```python
   SERIAL_PORT = "COM5"
   ```

2. Run the script:
   ```
   python your_script_name.py
   ```

3. When prompted, press Enter to start a 30-second data capture session.

---

## 📈 Output

- 3 plots: Accelerometer, Gyroscope, and Filtered Total Acceleration  
- Vertical dashed lines indicate button fall events (red)

---

## 🔎 Notes

- Your serial device must send data in this format:
  ```
  millis,gx,gy,gz,ax,ay,az,button
  ```
- Sampling rate: 100 Hz (1 sample every 10 ms)

---

## 📝 License

MIT License – Free to use, share, and modify!

---

Made with ❤️ for data and sensors!
