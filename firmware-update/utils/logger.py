import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """
    Logger class for handling application logging.
    Logs are written to /var/log/firmware-update.log with proper timestamps.
    """
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not Logger._initialized:
            self.logger = logging.getLogger('FirmwareUpdate')
            self.logger.setLevel(logging.DEBUG)

            # Create log directory if it doesn't exist
            log_dir = '/var/log/'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir, exist_ok=True)

            # Set up file handler with rotation
            log_file = os.path.join(log_dir, 'firmware-update.log')
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(file_handler)
            Logger._initialized = True

    @classmethod
    def get_logger(cls):
        """
        Get the singleton logger instance.
        
        Returns:
            Logger: The logger instance
        """
        if cls._instance is None:
            cls._instance = Logger()
        return cls._instance

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)

    def exception(self, message):
        """Log an exception with traceback."""
        self.logger.exception(message) 