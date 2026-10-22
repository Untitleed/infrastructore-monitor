from monitor import get_speed, get_status

assert get_speed(0) == "FAST"
assert get_speed(199.99) == "FAST"
assert get_speed(200) == "NORMAL"
assert get_speed(500) == "NORMAL"
assert get_speed(500.01) == "SLOW"
assert get_speed(None) == "N/A"

assert get_status(200) == "ONLINE"
assert get_status(201) == "ONLINE"
assert get_status(301) == "REDIRECT"
assert get_status(404) == "OFFLINE"
assert get_status(503) == "OFFLINE"
assert get_status("ERROR") == "CONNECTION ERROR"

print("All tests passed!")