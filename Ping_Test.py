import subprocess
import platform

def ping_ip(ip):
    # OS-specific ping command
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]

    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    return result.returncode == 0  # 0 means success

# Test IPs
start_ip = int(input("Enter your start IP(0-255): "))
end_ip = int(input("Enter your IP range(0-255): "))
for i in range(start_ip, end_ip):
    ip = f"172.16.172.{i}"
    if ping_ip(ip):
        print(f"{ip} is reachable ✅")
    else:
        print(f"{ip} is not reachable ❌")