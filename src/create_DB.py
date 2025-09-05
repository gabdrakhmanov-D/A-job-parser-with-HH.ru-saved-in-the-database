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

        cur.execute(f"DROP DATABASE {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE companies (
                        company_id SERIAL PRIMARY KEY,
                        company_name VARCHAR(255) NOT NULL
                    )
                """)

        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        job_title VARCHAR NOT NULL,
                        company_id INT REFERENCES companies(company_id),
                        requirements TEXT,
                        responsibility TEXT,
                        experience VARCHAR(255),
                        salary_from INTEGER,
                        salary_to INTEGER,
                        job_link TEXT UNIQUE                        
                    )
                """)

        conn.commit()
        conn.close()
