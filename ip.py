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
    
    # Get the current time and date
    current_time = get_current_time()

    # Update the labels with the fetched data
    ipv4_label.config(text=f"IPv4: {ipv4}")
    ipv6_label.config(text=f"IPv6: {ipv6}")
    
    if "error" not in ipv4_location:
        location_text = f"Location (IPv4): {ipv4_location['city']}, {ipv4_location['region']}, {ipv4_location['country']}"
    else:
        location_text = f"Error: {ipv4_location['error']}"
    
    location_label.config(text=location_text)
    time_label.config(text=f"Time/Date: {current_time}")

# Create the GUI window
root = tk.Tk()
root.title("IP Address Finder")

# Set the background color of the window
background_color = "#B1D690"
root.configure(bg=background_color)

# Window size and layout
root.geometry("500x300")
root.resizable(False, False)

# Title Label with background color
title_label = tk.Label(root, text="IP Address and Location Finder", font=("Helvetica", 16, "bold"), bg=background_color)
title_label.pack(pady=10)

# Labels to display IPv4, IPv6, and location with background color
ipv4_label = tk.Label(root, text="IPv4: Waiting...", font=("Helvetica", 12), bg=background_color)
ipv4_label.pack(pady=5)

ipv6_label = tk.Label(root, text="IPv6: Waiting...", font=("Helvetica", 12), bg=background_color)
ipv6_label.pack(pady=5)

location_label = tk.Label(root, text="Location (IPv4): Waiting...", font=("Helvetica", 12), bg=background_color)
location_label.pack(pady=5)

time_label = tk.Label(root, text="Time/Date: Waiting...", font=("Helvetica", 12), bg=background_color)
time_label.pack(pady=10)

# Button to trigger IP fetching with background color
fetch_button = tk.Button(root, text="Fetch IP Addresses", command=fetch_ip_data, font=("Helvetica", 12), bg="#A9C67A")
fetch_button.pack(pady=10)

# Run the application
root.mainloop()
