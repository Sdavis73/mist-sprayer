# /firmware/main.py
import time, json
from machine import Pin
import dht
import sys

DHT_PIN = 4
RELAY_PIN = 16
MIST_MAX_SEC = 8
MIST_COOLDOWN_SEC = 60

relay = Pin(RELAY_PIN, Pin.OUT)
sensor = dht.DHT22(Pin(DHT_PIN))
last_mist_ts = 0

def mist_on(duration=MIST_MAX_SEC):
    global last_mist_ts
    now = time.time()
    if now - last_mist_ts < MIST_COOLDOWN_SEC:
        return {"ok": False, "msg": "cooldown"}
    if duration > MIST_MAX_SEC:
        duration = MIST_MAX_SEC
    relay.value(1)
    time.sleep(duration)
    relay.value(0)
    last_mist_ts = time.time()
    return {"ok": True, "msg": f"misted {duration}s"}

def read_sensor():
    try:
        sensor.measure()
        return {"ok": True, "t_c": sensor.temperature(), "rh": sensor.humidity()}
    except Exception as e:
        return {"ok": False, "err": str(e)}

def read_cmd_line():
    # Non-blocking read of a line from stdin if available
    # Expect JSON like {"cmd":"mist","duration":6}
    try:
        if sys.stdin.buffer.peek(1):
            line = sys.stdin.readline().decode().strip()
            if line:
                return json.loads(line)
    except Exception:
        pass
    return None

def loop():
    while True:
        data = read_sensor()
        print(json.dumps({"type":"telemetry","data":data}))
        # Handle an incoming command (optional)
        cmd = read_cmd_line()
        if cmd and cmd.get("cmd") == "mist":
            res = mist_on(cmd.get("duration", MIST_MAX_SEC))
            print(json.dumps({"type":"result","data":res}))
        time.sleep(10)

loop()



