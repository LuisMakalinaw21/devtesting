import socket
import requests
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Function to get public IPv4 and IPv6 addresses using ipify API
def get_public_ip(version="ipv4"):
    if version == "ipv6":
        url = "https://api6.ipify.org?format=json"
    else:
        url = "https://api.ipify.org?format=json"
    
    try:
        response = requests.get(url)
        ip_data = response.json()
        return ip_data['ip']
    except Exception as e:
        return f"Error fetching {version}: {str(e)}"

# Function to get location information from ipinfo.io API (for IPv4 only)
def get_location(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        data = response.json()
        return {
            'ip': data.get('ip', 'N/A'),
            'city': data.get('city', 'N/A'),
            'region': data.get('region', 'N/A'),
            'country': data.get('country', 'N/A'),
            'loc': data.get('loc', 'N/A'),  # Latitude and Longitude
            'timezone': data.get('timezone', 'N/A')
        }
    except Exception as e:
        return {"error": str(e)}

# Function to check if the IP address is within private or reserved ranges
def is_private_ip(ip):
    private_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255")
    ]
    ip_parts = list(map(int, ip.split('.')))
    
    for start, end in private_ranges:
        start_parts = list(map(int, start.split('.')))
        end_parts = list(map(int, end.split('.')))
        if start_parts[0] <= ip_parts[0] <= end_parts[0]:
            if start_parts[1] <= ip_parts[1] <= end_parts[1]:
                if start_parts[2] <= ip_parts[2] <= end_parts[2]:
                    if start_parts[3] <= ip_parts[3] <= end_parts[3]:
                        return True
    return False

# Function to get the current time and date
def get_current_time():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Function that runs when the button is clicked
def fetch_ip_data():
    # Get the public IPv4 and IPv6 addresses
    ipv4 = get_public_ip("ipv4")
    ipv6 = get_public_ip("ipv6")
    
    # Get location details for IPv4
    ipv4_location = get_location(ipv4) if "Error" not in ipv4 else {"error": ipv4}
    
    # Check if IPv4 is private
    ipv4_status = "Private" if is_private_ip(ipv4) else "Public"
    
    # Get the current time and date
    current_time = get_current_time()

    # Update the textboxes with the fetched data
    ipv4_textbox.delete(1.0, tk.END)
    ipv4_textbox.insert(tk.END, f"IPv4: {ipv4} ({ipv4_status})")

    ipv6_textbox.delete(1.0, tk.END)
    ipv6_textbox.insert(tk.END, f"IPv6: {ipv6}")
    
    if "error" not in ipv4_location:
        location_text = f"Location (IPv4): {ipv4_location['city']}, {ipv4_location['region']}, {ipv4_location['country']}"
    else:
        location_text = f"Error: {ipv4_location['error']}"

    location_textbox.delete(1.0, tk.END)
    location_textbox.insert(tk.END, location_text)
    
    time_textbox.delete(1.0, tk.END)
    time_textbox.insert(tk.END, f"Time/Date: {current_time}")

# Function to refresh the data
def refresh_data():
    fetch_ip_data()

# Create the GUI window
root = tk.Tk()
root.title("IP Address Finder")

# Set the background color of the window
background_color = "#B1D690"
root.configure(bg=background_color)

# Window size and layout
root.geometry("500x400")
root.resizable(False, False)

# Title Label with background color
header_color = "#4E6E2F"  # Darker color for the header
title_label = tk.Label(root, text="IP Address and Location Finder", font=("Helvetica", 16, "bold"), bg=header_color, fg="white")
title_label.pack(fill=tk.X, pady=10)

# Textboxes to display IPv4, IPv6, location, and time with background color
ipv4_textbox = tk.Text(root, height=2, width=50, font=("Helvetica", 12), bg="white", wrap=tk.WORD)
ipv4_textbox.pack(pady=5)

ipv6_textbox = tk.Text(root, height=2, width=50, font=("Helvetica", 12), bg="white", wrap=tk.WORD)
ipv6_textbox.pack(pady=5)

location_textbox = tk.Text(root, height=4, width=50, font=("Helvetica", 12), bg="white", wrap=tk.WORD)
location_textbox.pack(pady=5)

time_textbox = tk.Text(root, height=2, width=50, font=("Helvetica", 12), bg="white", wrap=tk.WORD)
time_textbox.pack(pady=10)

# Button to fetch and refresh IP data with background color
fetch_button = tk.Button(root, text="Fetch IP Addresses", command=fetch_ip_data, font=("Helvetica", 12), bg="#A9C67A")
fetch_button.pack(pady=10)

# Refresh Button to reset and fetch new data
refresh_button = tk.Button(root, text="Refresh", command=refresh_data, font=("Helvetica", 12), bg="#A9C67A")
refresh_button.pack(pady=5)

# Run the application
root.mainloop()
