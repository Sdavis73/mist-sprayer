
# /host/serial_controller.py
import serial, json, time, csv, pathlib
PORT = "COM4"       # Adjust to your ESP32 port on Windows 11
BAUD = 115200
TARGET_RH = 55
HYST = 3
COOLDOWN_SEC = 60
MIST_SEC = 6

LOG = pathlib.Path("logs/mist_log.csv")
LOG.parent.mkdir(exist_ok=True)

def decide_and_command(s, rh, last_mist_ts):
    now = time.time()
    if rh is None:
        return last_mist_ts, "sensor_error"
    need_mist = rh < (TARGET_RH - HYST)
    cooldown_ok = (now - last_mist_ts) > COOLDOWN_SEC
    if need_mist and cooldown_ok:
        cmd = {"cmd": "mist", "duration": MIST_SEC}
        s.write((json.dumps(cmd) + "\n").encode())
        return now, "mist"
    return last_mist_ts, "none"

with serial.Serial(PORT, BAUD, timeout=1) as s, open(LOG, "a", newline="") as f:
    writer = csv.writer(f)
    if LOG.stat().st_size == 0:
        writer.writerow(["ts","t_c","rh","action"])
    last_mist_ts = 0
    while True:
        line = s.readline().decode(errors="ignore").strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        if msg.get("type") == "telemetry":
            data = msg.get("data", {})
            if data.get("ok"):
                t = data.get("t_c")
                rh = data.get("rh")
                last_mist_ts, action = decide_and_command(s, rh, last_mist_ts)
                writer.writerow([time.time(), t, rh, action])
                print(f"T={t:.1f}C RH={rh:.1f}% action={action}")
            else:
                writer.writerow([time.time(), None, None, "telemetry_error"])
                print("Telemetry error")

