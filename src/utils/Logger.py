import logging
import os
import traceback

class Logger:
    def __init__(self):
        self.logger = self.__set_logger()

    def __set_logger(self):
        log_directory = 'src/utils/log'
        log_filename = 'app.log'
        
        # Crear el directorio si no existe
        os.makedirs(log_directory, exist_ok=True)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        # Asegurarse de que no se acumulen handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        logger.addHandler(file_handler)
        return logger

    def add_to_log(self, level: str, message):
        try:
            if level == "critical":
                self.logger.critical(message)
            elif level == "debug":
                self.logger.debug(message)
            elif level == "error":
                self.logger.error(message)
            elif level == "info":
                self.logger.info(message)
            elif level == "warn":
                self.logger.warning(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)
