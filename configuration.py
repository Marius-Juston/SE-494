import datetime
import json
import logging
import os


class Config:
    def __init__(self, config_file='config.json'):
        self.__config = json.load(open(config_file, 'r'))

        for k, v in self.__config.items():
            setattr(self, k, v)

        log_dir = self.__config['LOG_DIRECTORY']

        if not os.path.exists(log_dir):
            print(f"The path {log_dir} does not exist, creating folder")

            os.makedirs(log_dir, exist_ok=True)

        logging_filename = f'{datetime.datetime.now().strftime("%Y-%m-%d-%H")}.log'

        full_path = os.path.join(log_dir, logging_filename)
        full_path = os.path.abspath(full_path)

        print("Saving logs to:", full_path)

        logging.basicConfig(filename=full_path, format='%(asctime)s:%(levelname)s:%(funcName)s:%(lineno)d:%(message)s', level=logging.DEBUG)


if __name__ == '__main__':
    data = Config()
    print(data.SQL_SERVER_NAME)
