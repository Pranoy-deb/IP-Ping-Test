import subprocess
import platform
import concurrent.futures
import socket
import os
import csv
from colorama import Fore, Style, init

init(autoreset=True)  # Auto-reset terminal color


# List of common ports (can be customized)
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
    443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080
]


def ping_ip(ip):
    """Ping an IP address to check if it's reachable."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=1)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def resolve_hostname(ip):
    """Resolve hostname for the given IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Hostname not found"


def scan_single_port(ip, port):
    """Check if a single TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.3)  # shorter timeout
            if sock.connect_ex((ip, port)) == 0:
                return port
    except:
        pass
    return None


def scan_ports(ip, ports=COMMON_PORTS):
    """Scan selected TCP ports on the IP address."""
    open_ports = []

    def check_port(port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(0.3)  # shorter timeout
                if sock.connect_ex((ip, port)) == 0:
                    return port
        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_port, port): port for port in ports}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                open_ports.append(result)

    return sorted(open_ports)


def scan_ips(start, end, network="172.16.172", full_scan=False, all_ports=False):
    """Scan a range of IPs for reachability, hostname, and optionally ports."""
    reachable_ips = []

    # Use all ports if the user selects this option
    ports_to_scan = range(1, 65536) if all_ports else COMMON_PORTS

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        future_to_ip = {
            executor.submit(ping_ip, f"{network}.{i}"): f"{network}.{i}"
            for i in range(start, end + 1)
        }

        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():
                    hostname = resolve_hostname(ip)
                    print(f"{Fore.GREEN}[✅] {ip} is reachable | Hostname: {hostname}")

                    ports = []
                    if full_scan:
                        print(f"{Fore.CYAN}    → Scanning ports on {ip}...")
                        ports = scan_ports(ip, ports=ports_to_scan)

                    reachable_ips.append((ip, hostname, ports))
                    if full_scan:
                        port_info = f"{Fore.CYAN}Open ports: {ports}" if ports else f"{Fore.RED}No open ports"
                        print(f"{Fore.YELLOW}    → {ip} | {hostname} | {port_info}")
                else:
                    print(f"{Fore.RED}[❌] {ip} is not reachable")
            except Exception as e:
                print(f"{Fore.RED}[⚠️] Error scanning {ip}: {e}")

    return reachable_ips


def get_ip_range_and_base():
    """Prompt the user for base IP and range."""
    try:
        base_ip = input(f"{Fore.MAGENTA}Enter base IP (e.g., 192.168.1) or press Enter for default [172.16.172]: {Style.RESET_ALL}").strip()
        if not base_ip:
            base_ip = "172.16.172"

        if len(base_ip.split(".")) != 3 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in base_ip.split(".")):
            print(f"{Fore.RED}Invalid base IP format.")
            return None, None, None

        start_ip = int(input(f"{Fore.MAGENTA}Enter start IP (last octet, 0-255): {Style.RESET_ALL}"))
        end_ip = int(input(f"{Fore.MAGENTA}Enter end IP (last octet, 0-255): {Style.RESET_ALL}"))

        if 0 <= start_ip <= 255 and 0 <= end_ip <= 255:
            return start_ip, end_ip, base_ip
        else:
            print(f"{Fore.RED}IP range must be between 0 and 255.")
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter valid numbers.")
    return None, None, None


def export_to_csv(data, base_filename="scan_result"):
    """Export scan results to a CSV file with a unique filename."""
    # Find the next available filename (scan_result_1.csv, scan_result_2.csv, etc.)
    counter = 1
    while os.path.exists(f"{base_filename}_{counter}.csv"):
        counter += 1

    filename = f"{base_filename}_{counter}.csv"
    
    # Write data to the new CSV file
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Hostname", "Open Ports"])
        for ip, hostname, ports in data:
            writer.writerow([ip, hostname, ", ".join(map(str, ports)) if ports else "None"])
    
    print(f"\n{Fore.GREEN}Results saved to {filename}{Style.RESET_ALL}")

def ask_full_port_scan():
    """Prompt the user to choose if they want to scan all ports or just common ports."""
    response = input("Scan ALL ports (1-65535)? [y/N]: ").strip().lower()
    return response == 'y'


def main():
    """Main program logic."""
    print(f"\n{Fore.GREEN}{'=' * 50}")
    print(f"{Fore.YELLOW}              Network Scanner Tool")
    print(f"{Fore.GREEN}{'=' * 50}")
    print(f"{Fore.CYAN}1. Ping & Hostname Test")
    print(f"{Fore.CYAN}2. Ping, Hostname & Port Scan Test")
    print(f"{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}")

    try:
        choice = int(input(f"{Fore.MAGENTA}Choose an option (1 or 2): {Style.RESET_ALL}"))
        if choice not in [1, 2]:
            print(f"{Fore.RED}Invalid choice. Exiting.")
            return

        start_ip, end_ip, base_ip = get_ip_range_and_base()
        if start_ip is None or end_ip is None or base_ip is None:
            return

        print(f"\n{Fore.YELLOW}Scanning IPs from {base_ip}.{start_ip} to {base_ip}.{end_ip}...\n")
        
        # Check if we need to scan all ports or just common ports
        use_all_ports = False
        if choice == 2:
            use_all_ports = ask_full_port_scan()

        results = scan_ips(start_ip, end_ip, network=base_ip, full_scan=(choice == 2), all_ports=use_all_ports)

        print(f"\n{Fore.GREEN}{'=' * 50}")
        print(f"{Fore.CYAN}Scan complete. Found {len(results)} reachable IP(s):")

        for ip, hostname, ports in results:
            if choice == 1:
                print(f"{Fore.YELLOW}- {ip} | Hostname: {hostname}")
            else:
                port_info = f"{Fore.CYAN}Open ports: {ports}" if ports else f"{Fore.RED}No open ports"
                print(f"{Fore.YELLOW}- {ip} | Hostname: {hostname} | {port_info}")

        print(f"{Fore.GREEN}{'=' * 50}{Style.RESET_ALL}")

        export = input(f"\n{Fore.MAGENTA}Do you want to export results to CSV? (y/n): {Style.RESET_ALL}").lower()
        if export == "y":
            export_to_csv(results)

    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()

