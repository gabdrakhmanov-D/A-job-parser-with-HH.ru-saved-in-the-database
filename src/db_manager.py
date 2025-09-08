import psycopg2

from src.creator_db import CreateDB


class DBManager(CreateDB):
    def __init__(self, database_name):
        super().__init__(database_name)
        self.__config_db = self.get_config()

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """ Получает список всех компаний и количество вакансий у каждой компании."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                        """ SELECT employers.name, COUNT(*) FROM employers
                            JOIN vacancies ON vacancies.employer_id=employers.id
                            GROUP BY employers.name
                        """
                        )
            rows = cur.fetchall()

        conn.commit()
        conn.close()

        return rows

    def get_all_vacancies(self) -> list[tuple]:
        """ Получает список всех вакансий с указанием названия компании,
         названия вакансии, зарплаты и ссылки на вакансию."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT employers.name, vacancies.job_title, vacancies.salary_from, vacancies.job_link from vacancies
                    JOIN employers ON vacancies.employer_id=employers.id
                """
            )
            rows = cur.fetchall()

        conn.commit()
        conn.close()

        return rows


    def get_avg_salary(self) -> int:
        """ Получает среднюю зарплату по вакансиям."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT AVG(salary) FROM 
                   (SELECT AVG(salary_from) as salary FROM vacancies
                    UNION
                    SELECT AVG(salary_to) as salary FROM vacancies)
                """
            )
            salary = round(cur.fetchone()[0], 2)

        conn.commit()
        conn.close()

        return int(salary)



    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT * FROM vacancies
                    WHERE salary_from >
                   (SELECT AVG(salary) FROM 
                   (SELECT AVG(salary_from) as salary FROM vacancies
                    UNION
                    SELECT AVG(salary_to) as salary FROM vacancies))
                """
            )
            rows = cur.fetchall()

        conn.commit()
        conn.close()

        return rows

    def get_vacancies_with_keyword(self, keyword:str) -> list[tuple]:
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        keyword_capitalize = f'%{keyword.capitalize()}%'
        keyword_lower =  f'{keyword.lower()}%'

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT * FROM vacancies
                          WHERE job_title LIKE %s OR job_title LIKE %s
                      """, (keyword_capitalize, keyword_lower)
            )
            rows = cur.fetchall()

        conn.commit()
        conn.close()

        return rows
