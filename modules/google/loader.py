from google.cloud import bigquery

class BigQuery:
    def __init__(self, frame, project_id, target_table  ) -> None:
        self.__project_id = project_id
        self.__client = bigquery.Client(project=self.__project_id)
        self.__target_table = target_table
        self.__frame = frame
        try:
            print(self.__frame.info())
        except Exception as e:
            print('erro em obter informações')
        self.__job_config = bigquery.LoadJobConfig(
            autodetect=True,
            write_disposition = 'WRITE_TRUNCATE' #'WRITE_APPEND',
        )

    def upload(self):
        load_job = self.__client.load_table_from_dataframe(
            self.__frame,
            self.__target_table,
            job_config=self.__job_config
        )
        print('Carregando tabela no BigQuery...')
        load_job.result()
        table = self.__client.get_table(self.__target_table)
        print(table.num_rows, '\n')
        