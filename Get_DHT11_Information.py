import tkinter as tk
from tkinter import messagebox
import requests
import csv
import time
import threading
import os
from datetime import datetime


class DataLoggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ESP8266 Data Logger")

        # Labels and Entries for ESP IP Address and Time Interval
        tk.Label(root, text="ESP8266 IP Address:").grid(row=0, column=0, padx=10, pady=10)
        self.esp_ip_entry = tk.Entry(root, width=30)
        self.esp_ip_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Time Interval (seconds):").grid(row=1, column=0, padx=10, pady=10)
        self.time_interval_entry = tk.Entry(root)
        self.time_interval_entry.grid(row=1, column=1, padx=10, pady=10)

        # Start and Stop Buttons
        self.start_button = tk.Button(root, text="Start Logging", command=self.start_logging)
        self.start_button.grid(row=2, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=1, padx=10, pady=10)

        # Initialize variables
        self.logging_thread = None
        self.logging_active = False

    def get_data(self, esp_ip):
        try:
            response = requests.get(esp_ip)
            if response.status_code == 200:
                data = response.text.split(", ")
                temp = float(data[0].split(": ")[1].split(" ")[0])
                humidity = float(data[1].split(": ")[1].split(" ")[0])
                time_of_day = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                return temp, humidity, time_of_day
            else:
                messagebox.showerror("Error",
                                     f"Failed to retrieve data from {esp_ip}. Status code: {response.status_code}")
                return None, None, None
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching data from {esp_ip}: {str(e)}")
            return None, None, None

    def save_to_csv(self, temp, humidity, time_of_day):
        csv_file = "DHT11_Info.csv"
        file_exists = os.path.isfile(csv_file)

        try:
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Temp', 'Humidity', 'ToD'])  # Write headers only if file is empty
                writer.writerow([temp, humidity, time_of_day])
            print(f"Data saved: Temp={temp}, Humidity={humidity}, Time={time_of_day}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data to CSV: {str(e)}")

    def start_logging(self):
        esp_ip = self.esp_ip_entry.get().strip()
        time_interval = self.time_interval_entry.get().strip()

        if not esp_ip or not time_interval:
            messagebox.showerror("Error", "Please enter ESP8266 IP address and Time Interval.")
            return

        # Add http:// prefix if not present
        if not esp_ip.startswith("http://") and not esp_ip.startswith("https://"):
            esp_ip = "http://" + esp_ip

        try:
            time_interval = float(time_interval)
            if time_interval <= 0:
                raise ValueError("Time Interval must be a positive number.")
        except ValueError:
            messagebox.showerror("Error", "Invalid Time Interval. Please enter a positive number.")
            return

        self.logging_active = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.logging_thread = threading.Thread(target=self.log_data_thread, args=(esp_ip, time_interval))
        self.logging_thread.start()

    def stop_logging(self):
        self.logging_active = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        if self.logging_thread and self.logging_thread.is_alive():
            self.logging_thread.join()

    def log_data_thread(self, esp_ip, time_interval):
        while self.logging_active:
            start_time = time.time()
            temp, humidity, time_of_day = self.get_data(esp_ip)
            if temp is not None and humidity is not None and time_of_day is not None:
                self.save_to_csv(temp, humidity, time_of_day)
            else:
                messagebox.showwarning("Warning", f"Failed to retrieve data from {esp_ip}")

            elapsed_time = time.time() - start_time
            if elapsed_time < time_interval:
                time.sleep(time_interval - elapsed_time)
            else:
                messagebox.showwarning("Warning",
                                       f"Data collection took longer than the specified interval ({time_interval} seconds).")


# Create the GUI window
root = tk.Tk()
app = DataLoggerGUI(root)
root.mainloop()
