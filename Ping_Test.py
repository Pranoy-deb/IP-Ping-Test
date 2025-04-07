import subprocess
import platform
import concurrent.futures  # For threading to speed up the scanning

def ping_ip(ip):
    """
    Ping an IP address and return True if reachable, False otherwise.
    Uses OS-specific ping commands for compatibility.
    """
    # Determine the correct ping count parameter based on OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    # Build the ping command (1 packet for speed)
    command = ["ping", param, "1", ip]
    
    # Run the command and suppress output for cleaner operation
    # Set timeout=1 to prevent hanging on unresponsive IPs
    try:
        result = subprocess.run(command, 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL,
                               timeout=1)
        return result.returncode == 0  # Return True if ping was successful
    except subprocess.TimeoutExpired:
        return False  # Consider timeout as unreachable

def scan_ips(start, end, network="172.16.172"):
    """
    Scan a range of IP addresses using multiple threads for faster operation.
    Returns a list of reachable IPs.
    """
    reachable_ips = []
    
    # Use ThreadPoolExecutor to parallelize ping operations
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Create future objects for each IP
        future_to_ip = {
            executor.submit(ping_ip, f"{network}.{i}"): f"{network}.{i}" 
            for i in range(start, end + 1)
        }
        
        # Process completed pings as they finish
        for future in concurrent.futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                if future.result():  # If ping was successful
                    reachable_ips.append(ip)
                    print(f"{ip} is reachable ✅")
                else:
                    print(f"{ip} is not reachable ❌")
            except Exception as e:
                print(f"Error pinging {ip}: {e}")
    
    return reachable_ips

if __name__ == "__main__":
    # Get user input for IP range
    start_ip = int(input("Enter your start IP (0-255): "))
    end_ip = int(input("Enter your end IP (0-255): "))
    
    # Validate input
    if not (0 <= start_ip <= 255 and 0 <= end_ip <= 255):
        print("Invalid IP range. Please enter values between 0-255.")
    else:
        print(f"\nScanning IPs from {start_ip} to {end_ip}...\n")
        
        # Start the scan and get reachable IPs
        reachable = scan_ips(start_ip, end_ip)
        
        # Print summary
        print(f"\nScan complete. Found {len(reachable)} reachable IPs:")
        for ip in reachable:
            print(f"- {ip}")