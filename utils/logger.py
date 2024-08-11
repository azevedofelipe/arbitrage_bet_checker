import os
import logging
import datetime
from typing import Union, Literal

class LoggerClass:
    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }

    def __init__(
        self, filename: Union[str, None] = None, folder: Union[str, None] = "logs"
    ) -> None:
        self.start_time = datetime.datetime.now()

        if filename:
            if folder:
                self.filename = os.path.join(folder, filename)
                if not os.path.exists(folder):
                    os.makedirs(folder)
            else:
                self.filename = filename
        else:
            current_time = self.start_time.strftime("%d-%m-%Y %Hh%Mm")
            if folder:
                self.filename = os.path.join(folder, f"arb_logs_{current_time}.log")
                if not os.path.exists(folder):
                    os.makedirs(folder)
            else:
                self.filename = f"arb_logs_{current_time}.log"

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create file handler
        file_handler = logging.FileHandler(self.filename, encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def log(
        self,
        message: str,
        level: Literal["debug", "info", "warning", "error", "critical"] = "info",
    ):
        log_level = self.LOG_LEVELS.get(level, self.LOG_LEVELS["info"])
        self.logger.log(log_level, message)

# Initialize logger
logger = LoggerClass()