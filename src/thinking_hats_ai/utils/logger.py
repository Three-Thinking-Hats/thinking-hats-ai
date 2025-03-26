import logging
import os
import sys
import textwrap
from datetime import datetime


class Logger:
    def __init__(self, technique_name, dev):
        self.technique_name = technique_name
        self.dev = dev
        self.logger = logging.getLogger(__name__)
        if dev:
            self._set_up_logger()

    def _set_up_logger(self):
        execution_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        log_file = os.path.join(
            execution_dir,
            f"{self.technique_name}{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        )
        log_folder = os.path.join(execution_dir, "logs")
        os.makedirs(log_folder, exist_ok=True)
        log_file = os.path.join(
            log_folder,
            f"{self.technique_name}{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        )
        file_handler = logging.FileHandler(
            log_file, mode="w", encoding="utf-8"
        )
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(formatter)
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)

    def _wrap_text(self, text):
        return "\n".join(
            "\n".join(textwrap.wrap(line, width=120))
            for line in text.split("\n")
        )

    def log_prompt(self, prompt, notes="No notes"):
        if not self.dev:
            return
        wrapped_prompt = self._wrap_text(prompt)
        self.logger.info(f"PROMPT - {notes}\n{wrapped_prompt}")

    def log_response(self, response, notes="No notes"):
        if not self.dev:
            return
        wrapped_response = self._wrap_text(response)
        self.logger.info(f"RESPONSE - {notes}\n{wrapped_response}")

    def log_response_and_prompt(self, response, notes="No notes"):
        wrapped_response = self._wrap_text(response)
        self.logger.info(
            f"RESPONSE AND PROMPT (Multiagent) - {notes}\n{wrapped_response}"
        )
