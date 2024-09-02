# ESP8266 Data Logger

## Overview

The ESP8266 Data Logger is a Python application that uses the `tkinter` library to create a graphical user interface (GUI) for logging data from an ESP8266 device. 
The application retrieves temperature and humidity data from the ESP8266 and saves it to a CSV file at regular intervals.

## Features

- Enter the ESP8266 IP address and time interval for data logging.
- Start and stop data logging using GUI buttons.
- Data is saved to a CSV file with headers: `Temp`, `Humidity`, and `ToD`.
- Error handling and user notifications for failed data retrieval and file operations.

## Requirements

- Python 3.x
- `requests` library (for HTTP requests)
- `tkinter` library (included with Python)
- `csv` library (included with Python)
- `threading` library (included with Python)
- `datetime` library (included with Python)

## Installation

1. Clone the repository or download the code files.

2. Install the required libraries using pip:

    ```bash
    pip install requests
    ```

3. Ensure that you have Python 3.x installed on your system.

## Usage

1. Open a terminal or command prompt and navigate to the directory containing the `data_logger.py` file.

2. Run the application:

    ```bash
    python data_logger.py
    ```

3. The GUI window will appear:

<img width="272" alt="DHT11 Data Logger GUI" src="https://github.com/user-attachments/assets/fa89525f-1435-4878-a3a6-0f4a0c6bfb19">

4. Enter the ESP8266 IP address and the desired time interval (in seconds) for data logging.

<img width="270" alt="DHT11 Data Logger GUI Info Added" src="https://github.com/user-attachments/assets/6935d102-f162-401e-b0c2-3b163f313c6b">

5. Click the "Start Logging" button to begin data collection:

<img width="446" alt="DHT11 Data Logger Logging" src="https://github.com/user-attachments/assets/8969e7d9-fd4b-4e01-8ba7-126852d4096f">

6. Click the "Stop Logging" button to stop data collection:

7. Data will be saved in a file named `DHT11_Info.csv` in the same directory as the script.
<img width="125" alt="DHT11 Data Logger CSV" src="https://github.com/user-attachments/assets/882d34af-4bf2-4d00-bb16-8f462a3afa36">


## Code Description

- **DataLoggerGUI**: The main class responsible for the GUI and data logging functionality.
  - **`__init__`**: Initializes the GUI components.
  - **`get_data`**: Retrieves data from the ESP8266 and parses it.
  - **`save_to_csv`**: Saves the retrieved data to a CSV file.
  - **`start_logging`**: Starts a new thread to log data at regular intervals.
  - **`stop_logging`**: Stops the data logging process.
  - **`log_data_thread`**: Runs in a separate thread to continuously log data.

## Notes

- Ensure that the ESP8266 device is accessible over the network and responds with data in the expected format.
- The time interval for data logging must be a positive number.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The `tkinter` library for GUI development.
- The `requests` library for HTTP communication.
- The Python standard libraries (`csv`, `threading`, `datetime`) used in the implementation.
