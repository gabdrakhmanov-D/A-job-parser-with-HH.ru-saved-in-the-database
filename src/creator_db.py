import psycopg2
from configparser import ConfigParser

from config import PATH_TO_DB_INI


class CreateDB:
    database_name: str

    def __init__(self, database_name):
        self.database_name = database_name
        self.__config_db = self.get_config()


    def get_config(self, filename:str=PATH_TO_DB_INI, section:str= "postgresql") -> dict:
        """ Метод для получения конфигурации базы данных """
        parser = ConfigParser()
        parser.read(filename)
        self.__config_db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.__config_db[param[0]] = param[1]
            return self.__config_db
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, filename))

    def create_new_db(self):
        """ Метод, который создает новую базу данных """
        conn = psycopg2.connect(dbname='postgres', **self.__config_db)
        conn.autocommit = True
        cur = conn.cursor()
        try:
            cur.execute(f"CREATE DATABASE {self.database_name}")
            conn.close()
        except psycopg2.errors.DuplicateDatabase:
            return


    def create_tables(self):
        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS employers (
                        id SERIAL PRIMARY KEY,
                        external_id VARCHAR(100) NOT NULL,
                        name VARCHAR(100) NOT NULL,
                        city VARCHAR(50) NOT NULL,
                        url VARCHAR(100) NOT NULL,
                        link_to_profile VARCHAR(100) NOT NULL
                    )
                """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        job_title VARCHAR NOT NULL,
                        employer_id INT REFERENCES employers(id),
                        requirements TEXT,
                        responsibility TEXT,
                        experience VARCHAR(50),
                        salary_from INTEGER,
                        salary_to INTEGER,
                        job_link TEXT UNIQUE                        
                    )
                """)

        conn.commit()
        conn.close()
