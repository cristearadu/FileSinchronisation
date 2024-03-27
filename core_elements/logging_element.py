import logging
from datetime import datetime
from core import Core


class Logger(Core):
    def __init__(self):
        super().__init__()
        self.logs_path = f"{self.root_directory}\\output\\logs_folder"
        self.ensure_directory_exists(self.logs_path)
        self.logger = self.__setup_logger()

    def __setup_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        file_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S.log")
        file_handler = logging.FileHandler(
            f"{self.logs_path}\\{file_name}", encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        return logger
