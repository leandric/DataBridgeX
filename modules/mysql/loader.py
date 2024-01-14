import pandas as pd
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

class LoaderMySQL:
    def __init__(self, frame, conf, target_table='new_table') -> None:
        self.__frame = frame
        self.__target_table = target_table
        self.__DB_USER = conf['DB_USER']
        self.__DB_PASS = conf['DB_PASS']
        self.__DB_HOST = conf['DB_HOST']
        self.__DB_PORT = conf['DB_PORT']
        self.__DATABASE = conf['DATABASE']
        self.__connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(self.__DB_USER, 
                                                                         self.__DB_PASS, 
                                                                         self.__DB_HOST, 
                                                                         self.__DB_PORT, 
                                                                         self.__DATABASE)
        self.__engine = create_engine(self.__connect_string)

    def upload(self):
        try:
            logging.info(f'Loading Mysql Table: {self.__target_table}')
            with self.__engine.connect() as connection:
                            self.__frame.to_sql(name=self.__target_table,
                                                con=connection,
                                                if_exists='replace',
                                                index=False)
            logging.info(f'{self.__frame.shape[0]} rows and {self.__frame.shape[1]} loaded columns.')
        except Exception as e:
            logging.error(e)
        finally:
            self.__engine.dispose()