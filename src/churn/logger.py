# Import necessary libraries
import logging # Python's built-in logging module
import sys # System-specific parameters and functions
import os # Operating system-related functions
from datetime import datetime # Import the datetime class from the datetime module

# Generate a filename for the log file using the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create a path to store log files inside a "logs" directory in the current working directory
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE) 

# Create the "logs" directory if it doesn't exist
os.makedirs (logs_path, exist_ok=True) 

# Create the full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure the logging module
logging.basicConfig(
    filename=LOG_FILE_PATH, # Set the log file path
    level=logging.DEBUG, # Set the logging level to DEBUG, which includes all levels of log messages
    format='[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s: %(message)s'
    # Define the log message format. Here:
    # - %(asctime)s: The timestamp of the log message
    # - %(lineno)d: The line number where the log message was issued
    # - %(name)s: The name of the logger (usually the name of the Python module)
    # - %(levelname)s: The log level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # - %(message)s: The actual log message content
)
