import logging
import os

class TrainingLogger:
    def __init__(self, log_directory, log_filename):
        """
        Initializes the training logger.
        :param log_directory: Directory where the log file will be saved.
        :param log_filename: Name of the log file.
        """
        self.log_directory = log_directory
        self.log_filename = log_filename
        self.full_log_path = os.path.join(log_directory, log_filename)
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """
        Sets up the logger.
        """
        # Ensure the directory exists
        os.makedirs(self.log_directory, exist_ok=True)

        # Create logger
        logger = logging.getLogger(self.log_filename)
        logger.setLevel(logging.INFO)  # You can make this configurable if needed

        # Create file handler which logs even debug messages
        fh = logging.FileHandler(self.full_log_path)
        fh.setLevel(logging.INFO)  # You can make this configurable if needed

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(fh)

        return logger

    def log_message(self, level, message):
        """
        Logs a message.
        :param level: Logging level (e.g., 'info', 'warning', 'error').
        :param message: Message to be logged.
        """
        if level.lower() == 'info':
            self.logger.info(message)
        elif level.lower() == 'warning':
            self.logger.warning(message)
        elif level.lower() == 'error':
            self.logger.error(message)
        # You can expand this method to include other logging levels

    def close_logger(self):
        """
        Closes the logger and its handlers.
        """
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
