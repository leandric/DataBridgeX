from sqlalchemy import create_engine, text
from datetime import datetime 
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class TabelaNome:
    def __init__(self, conf) -> None:
        self.__QUERY = conf['PATH_SQL'] #if os.path.exists(conf['PATH_SQL']) else None

        self.__DB_USER = conf['DB_USER']
        self.__DB_PASS = conf['DB_PASS']
        self.__DB_HOST = conf['DB_HOST']
        self.__DB_PORT = conf['DB_PORT']
        self.__DATABASE = conf['DATABASE']
        self.__connect_string = f"mssql+pyodbc://{self.__DB_USER}:{self.__DB_PASS}@{self.__DB_HOST}:{self.__DB_PORT}/{self.__DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
        self.__engine = create_engine(self.__connect_string)

        if self.__QUERY:
             with open(self.__QUERY, 'r') as file:
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

confs = {
        "PATH_SQL":'sql//teste.sql',
        "DB_USER":"leandric",
        "DB_PASS":"azul#123",
        "DB_HOST":"PEGASUSWIN",
        "DB_PORT":"1433",
        "DATABASE":"AdventureWorks2022"}
if __name__ == '__main__':

    
    frame = TabelaNome(conf=confs)
    frame.updater()
    df = frame.frame.copy()
    print(df, '\n\t\t\t\t\t\t\t\t\t\t\t\t Test Ok \n\n')