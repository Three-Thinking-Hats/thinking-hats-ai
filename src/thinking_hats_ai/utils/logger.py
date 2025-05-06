import logging
import os
import sys
import textwrap
from datetime import datetime


class Logger:
    """
    A utility class for logging prompts and responses to timestamped log files during development.

    This logger is only active when `dev` is True, helping to control logging behavior based on the environment.
    Log files are stored in a 'logs' directory relative to the script execution path.
    """

    def __init__(self, technique_name, dev):
        """
        Initializes the Logger instance.

        Args:
            technique_name (str): A label or identifier used in naming the log file.
            dev (bool): If True, logging is enabled; otherwise, logging is disabled.
        """
        self.technique_name = technique_name
        self.dev = dev
        self.logger = logging.getLogger(__name__)

    def start_logger(self, file_name):
        """
        Starts the logger if in development mode by setting up a file handler.

        Args:
            file_name (str): The base name for the log file.
        """
        if self.dev:
            self._set_up_logger(file_name)

    def _set_up_logger(self, file_name):
        """
        Configures the logger with a file handler and formatter.

        Log files are created in a 'logs' directory with a timestamp.

        Args:
            file_name (str): The base name for the log file.
        """
        execution_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        log_folder = os.path.join(execution_dir, "logs")
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(
            log_folder,
            f"{self.technique_name}-{file_name}-{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        )
        file_handler = logging.FileHandler(
            log_file, mode="w", encoding="utf-8"
        )
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        self.logger.handlers.clear()
        self.logger.addHandler(file_handler)

    def _wrap_text(self, text):
        """
        Wraps long lines of text to a width of 120 characters.

        Args:
            text (str): The input text to be wrapped.

        Returns:
            str: The wrapped text.
        """
        return "\n".join(
            "\n".join(textwrap.wrap(line, width=120))
            for line in text.split("\n")
        )

    def log_prompt(self, prompt, notes="No notes"):
        """
        Logs a prompt message to the log file if in development mode.

        Args:
            prompt (str): The prompt text to log.
            notes (str, optional): Additional context or comments. Defaults to "No notes".
        """
        if not self.dev:
            return
        wrapped_prompt = self._wrap_text(prompt)
        self.logger.info(f"PROMPT - {notes}\n{wrapped_prompt}\n")

    def log_response(self, response, notes="No notes"):
        """
        Logs a response message to the log file if in development mode.

        Args:
            response (str): The response text to log.
            notes (str, optional): Additional context or comments. Defaults to "No notes".
        """
        if not self.dev:
            return
        wrapped_response = self._wrap_text(response)
        self.logger.info(f"RESPONSE - {notes}\n{wrapped_response}\n")

    def log_response_and_prompt(self, response, notes="No notes"):
        """
        Logs a combined prompt and response message, used for multiagent logging.

        Args:
            response (str): The combined prompt and response to log.
            notes (str, optional): Additional context or comments. Defaults to "No notes".
        """
        wrapped_response = self._wrap_text(response)
        self.logger.info(
            f"RESPONSE AND PROMPT (Multiagent) - {notes}\n{wrapped_response}"
        )
