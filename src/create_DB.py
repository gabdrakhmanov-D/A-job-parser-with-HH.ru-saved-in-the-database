import psycopg2
from configparser import ConfigParser

from config import PATH_TO_DB_INI


class CreateDB:
    database_name: str

    def __init__(self, database_name):
        self.database_name = database_name
        self.db = self.get_config()


    def get_config(self, filename=PATH_TO_DB_INI, section="postgresql"):
        parser = ConfigParser()
        parser.read(filename)
        self.db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                self.db[param[0]] = param[1]
            return self.db
        else:
            raise Exception(
                'Section {0} is not found in the {1} file.'.format(section, filename))

    def create_new_db(self):
        conn = psycopg2.connect(dbname='postgres', **self.db)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.db)

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
                        company_id INT REFERENCES companies(company_id),
                        job_title VARCHAR NOT NULL,
                        job_link TEXT UNIQUE,
                        salary_from INTEGER,
                        salary_to INTEGER,
                        requirements TEXT,
                        responsibility TEXT,
                        experience VARCHAR(255)                        
                    )
                """)

        conn.commit()
        conn.close()