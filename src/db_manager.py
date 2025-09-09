import psycopg2
from prettytable import TableStyle, from_db_cursor, PrettyTable
from src.creator_db import CreateDB


class DBManager(CreateDB):
    """ Класс для запроса к БД и выдаче таблиц с результатами. """

    def __init__(self, database_name):
        super().__init__(database_name)
        self.__config_db = self.get_config()

    def get_companies_and_vacancies_count(self) -> PrettyTable | None:
        """Получает список всех компаний и количество вакансий у каждой компании."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT employers.name, COUNT(*) FROM employers
                            JOIN vacancies ON vacancies.employer_id=employers.id
                            GROUP BY employers.name
                            ORDER BY COUNT(*) DESC
                        """
            )
            my_table = from_db_cursor(cur)
            my_table.field_names = ["Название компании", "Количество вакансий"]
            my_table.set_style(TableStyle.DOUBLE_BORDER)

        conn.commit()
        conn.close()

        return my_table

    def get_all_vacancies(self) -> PrettyTable | None:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT employers.name, vacancies.job_title,
                           vacancies.salary_from, vacancies.job_link from vacancies
                    JOIN employers ON vacancies.employer_id=employers.id
                    ORDER BY vacancies.salary_from DESC
                """
            )
            my_table = from_db_cursor(cur)
            my_table.field_names = [
                "Название компании",
                "Вакансия",
                "Зарплата от",
                "Ссылка на вакансию",
            ]
            my_table.set_style(TableStyle.DOUBLE_BORDER)

        conn.commit()
        conn.close()

        return my_table

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям."""

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

    def get_vacancies_with_higher_salary(self) -> PrettyTable | None:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT vacancies.job_title,
                                 employers.name,
                                 vacancies.requirements,
                                 vacancies.responsibility,
                                 vacancies.experience,
                                 vacancies.salary_from,
                                 vacancies.salary_to,
                                 vacancies.job_link
                    FROM vacancies
                    JOIN employers ON vacancies.employer_id=employers.id
                    WHERE salary_from >
                   (SELECT AVG(salary) FROM
                   (SELECT AVG(salary_from) as salary FROM vacancies
                    UNION
                    SELECT AVG(salary_to) as salary FROM vacancies))
                    ORDER BY vacancies.salary_from DESC
                """
            )

            my_table = from_db_cursor(cur)
            my_table.field_names = [
                "Вакансия",
                "Название компании",
                "Требования",
                "Описание",
                "Требуемый опыт",
                "Зарплата от",
                "Зарплата до",
                "Ссылка на вакансию",
            ]
            my_table.set_style(TableStyle.DOUBLE_BORDER)

        conn.commit()
        conn.close()

        return my_table

    def get_vacancies_with_keyword(self, keyword: str) -> PrettyTable | None:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова."""

        keyword_capitalize = f"%{keyword.capitalize()}%"
        keyword_lower = f"{keyword.lower()}%"

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            cur.execute(
                """ SELECT vacancies.job_title,
                                 employers.name,
                                 vacancies.requirements,
                                 vacancies.responsibility,
                                 vacancies.experience,
                                 vacancies.salary_from,
                                 vacancies.salary_to,
                                 vacancies.job_link
                          FROM vacancies
                          JOIN employers ON vacancies.employer_id=employers.id
                          WHERE job_title LIKE %s OR job_title LIKE %s
                          ORDER BY vacancies.salary_from DESC
                      """,
                (keyword_capitalize, keyword_lower),
            )

            my_table = from_db_cursor(cur)
            my_table.field_names = [
                "Вакансия",
                "Название компании",
                "Требования",
                "Описание",
                "Требуемый опыт",
                "Зарплата от",
                "Зарплата до",
                "Ссылка на вакансию",
            ]
            my_table.set_style(TableStyle.DOUBLE_BORDER)
        conn.commit()
        conn.close()

        return my_table
