import requests
from datetime import datetime
import time

REQUEST_TIMEOUT = 5
CHECK_INTERVAL = 5
ALERT_THRESHOLD = 3

servers = {
    "web01": "https://www.python.org",
    "web02": "https://httpbin.org/status/503",
    "web03": "http://127.0.0.1:9999",
    "local01": "http://127.0.0.1:8000"
}

def check_server(url):
    try:
        response = requests.get(url, timeout = REQUEST_TIMEOUT)
        response_time = round(response.elapsed.total_seconds() * 1000, 2)
        return response.status_code, response_time
    except requests.exceptions.Timeout:
        return "TIMEOUT", None
    except requests.exceptions.ConnectionError:
        return "CONNECTION ERROR", None
    except requests.exceptions.RequestException:
        return "ERROR", None

def get_status(code):
    if code == "TIMEOUT":
        return "TIMEOUT"
    elif code == "CONNECTION ERROR":
        return "CONNECTION ERROR"
    elif code == "ERROR":
        return "ERROR"
    elif 200 <= code < 300:
        return "ONLINE"
    elif 300 <= code < 400:
        return "REDIRECT"
    elif 400 <= code < 600:
        return "OFFLINE" 

def get_speed(response_time):
    if response_time is None:
        return "N/A"
    elif response_time < 200:
        return "FAST"
    elif response_time >= 200 and response_time <= 500:
        return "NORMAL"
    else:
        return "SLOW"

def save_log(message):
    with open("monitor.log", "a", encoding="utf-8") as file:
        file.write(f"{message}\n")

def format_time(response_time):
    if response_time is None:
        return "N/A"
    else:
        return f"{response_time} ms"

def main():
    failures = {}
    try:
        while True:
            save_log("========== MONITORING CYCLE ==========")
            total = 0
            online = 0
            for key, value in servers.items():
                status, response_time = check_server(value)
                speed = get_speed(response_time)
                time_display = format_time(response_time)
                total += 1
                result = get_status(status)
                now = datetime.now()
                date = now.strftime("%Y-%m-%d %H:%M:%S")
                if result == "ONLINE":
                    online += 1
                    if failures.get(key, 0) >= ALERT_THRESHOLD:
                        recovery = f"{key} RECOVERY"
                        print(recovery)
                        save_log(recovery)
                    failures[key] = 0
                else:
                    failures[key] = failures.get(key, 0) +1
                print(f"{key} -> Consecutive failures: {failures.get(key, 0)}")
                if failures[key] == ALERT_THRESHOLD:
                    alert = f"ALERT: {key} failed {ALERT_THRESHOLD} consecutive checks"
                    print(alert)
                    save_log(alert)
                message = f"{date} {key} -> {status} -> {result} -> {time_display} -> {speed}"
                print(message)
                save_log(message)
            other = total - online
            summary = f"Total servers: {total}\nOnline servers: {online}\nOther statuses: {other}"
            print(summary)
            save_log(summary)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
if __name__ == "__main__":
    main()

# DivFix Infrastructure Monitor - Git practice

