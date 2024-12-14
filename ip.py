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

    # Prepare the text content
    if "error" not in ipv4_location:
        location_text = f"Location (IPv4): {ipv4_location['city']}, {ipv4_location['region']}, {ipv4_location['country']}\n"
    else:
        location_text = f"Error: {ipv4_location['error']}\n"

    results = (
        f"IPv4: {ipv4}\n"
        f"IPv6: {ipv6}\n"
        f"{location_text}"
        f"Time/Date: {current_time}\n"
    )

    # Insert the text into the textbox
    results_textbox.delete("1.0", tk.END)
    results_textbox.insert(tk.END, results)

# Function to reset the text box
def reset_results():
    results_textbox.delete("1.0", tk.END)
    results_textbox.insert(tk.END, "Results will appear here...\n")

# Create the GUI window
root = tk.Tk()
root.title("IP Address Finder")

# Set the background color of the window
background_color = "#B1D690"
header_color = "#6B8E23"  # Darker green for the header
root.configure(bg=background_color)

# Window size and layout
root.geometry("500x400")
root.resizable(False, False)

# Create a header frame for the title
header_frame = tk.Frame(root, bg=header_color, height=50)
header_frame.pack(fill=tk.X)

# Title Label inside the header frame
title_label = tk.Label(header_frame, text="IP Address and Location Finder", font=("Helvetica", 16, "bold"), fg="white", bg=header_color)
title_label.pack(pady=10)

# Textbox to display results
results_textbox = tk.Text(root, font=("Helvetica", 12), width=60, height=15, wrap=tk.WORD, bg="#F0F0F0")
results_textbox.pack(pady=10)
results_textbox.insert(tk.END, "Results will appear here...\n")

# Button to fetch IP addresses
fetch_button = tk.Button(root, text="Fetch IP Addresses", command=fetch_ip_data, font=("Helvetica", 12), bg="#A9C67A")
fetch_button.pack(pady=5)

# Button to reset the text box
reset_button = tk.Button(root, text="Refresh", command=reset_results, font=("Helvetica", 12), bg="#D9A67A")
reset_button.pack(pady=5)

# Run the application
root.mainloop()
