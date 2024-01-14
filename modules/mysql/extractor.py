from sqlalchemy import create_engine, text
from datetime import datetime 
import pandas as pd
import logging
import os


class TabelaNome:
    def __init__(self, conf) -> None:
        self.__QUERY = conf['PATH_SQL'] if os.path.exists(conf['PATH_SQL']) else None

        self.__DB_USER = conf['DB_USER']
        self.__DB_PASS = conf['DB_PASS']
        self.__DB_HOST = conf['DB_HOST']
        self.__DB_PORT = conf['DB_PORT']
        self.__DATABASE = conf['DATABASE']
        connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(self.__DB_USER, 
                                                                         self.__DB_PASS, 
                                                                         self.__DB_HOST, 
                                                                         self.__DB_PORT, 
                                                                         self.__DATABASE)

        self.__engine = create_engine(connect_string)

        if self.__QUERY:
             with open('consulta.sql', 'r') as file:
                self.__query = file.read()

    def __trata_dados(self, **kwargs) -> None:
        df = kwargs.get('dataframe')
        return df
        
    def __transform(self, **kwargs) -> None:
        df = self.__trata_dados(dataframe=df)
        return df

    def updater(self):

            try:
                logging.info(f'Getting data at the source...')
                with self.__engine.connect() as self.__conn:
                    self.frame = pd.read_sql(text(self.__query), self.__conn)
                logging.info(f'Data obtained, shape: {self.frame.shape}')
            except Exception as e:
                logging.error(e)
            
            new_keys = []
            for key in self.frame.keys():
                new_keys.append(key.replace(".",""))
            self.frame.columns = new_keys
            logging.info(f'Processing data...')
            self.frame = self.__transform(self.frame)
            self.frame['LAST_UPDATE'] = datetime.now()
            self.memoria = (self.frame.memory_usage().sum() / (1024*1024))
            self.linhas = len(self.frame)
            logging.info(f'results: [Rows: {self.linhas}, MegaBytes:{self.memoria}]')

if __name__ == '__main__':
	confs = {
            "DB_USER":"user",
            "DB_PASS":"pass",
            "DB_HOST":"host",
            "DB_PORT":"3308",
            "DATABASE":"database"
        }
	frame = TabelaNome(conf=confs)
	df = frame.frame.copy()
	print(df, '\n\t\t\t\t\t\t\t\t\t\t\t\t Test Ok \n\n')