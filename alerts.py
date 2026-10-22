def send_alert(server, critical):
    if critical == True:
        print(f"CRITICAL ALERT: {server} is DOWN!")
    else:
        print(f"WARNING: Server {server} is unavailable")



