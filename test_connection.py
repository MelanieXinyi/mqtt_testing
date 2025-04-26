import socket
import subprocess
import platform


def is_connected():
    try:
        # Try to create a socket connection to Google's public DNS server (8.8.8.8)
        # on port 53 (DNS port).  A timeout of 5 seconds is used.
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        # An OSError (which includes socket.gaierror, socket.timeout, and others)
        # will be raised if the connection attempt fails.  This could be due to
        # no network connectivity, the server being unreachable, or a firewall.
        return False

def get_network_type():
    try:
        output = subprocess.check_output(["ip", "link"], universal_newlines=True)
        if "state UP" in output:
            if "ether" in output:
                return "Ethernet"
            elif "wlan" in output:
                return "Wi-Fi"
        output = subprocess.check_output(["ifconfig"], universal_newlines=True)
        if "RUNNING" in output:
            if "eth" in output:
                return "Ethernet"
            elif "wlan" in output or "wlp" in output:
                return "Wi-Fi"
        else:
            return "Unknown"
    except subprocess.CalledProcessError:
        return "Unknown"  # Handle errors with the 'ifconfig' or 'ip' command.

def main():
    """
    Main function to check and print the network status.
    """
    if is_connected():
        network_type = get_network_type()
        print(f"Connected to the internet via {network_type}.")
    else:
        print("Not connected to the internet.")

if __name__ == "__main__":
    main()
