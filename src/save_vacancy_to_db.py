import psycopg2

from src.creator_db import CreateDB


class SaveVacancyToDB(CreateDB):
    def __init__(self, database_name):
        super().__init__(database_name)
        self.__config_db = self.get_config()

    def save_vacancy_to_database(self, list_of_vacancies) -> None:
        """ Сохранение данных о вакансии в базу данных."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)

        with conn.cursor() as cur:
            for vacancy in list_of_vacancies:
                company_name = vacancy.employer_name
                job_title = vacancy.job_title
                requirements = vacancy.requirements
                responsibility = vacancy.responsibility
                salary_from = vacancy.salary_from
                salary_to = vacancy.salary_to
                job_link = vacancy.job_link
                experience = vacancy.experience
                cur.execute(
                    """
                        INSERT INTO companies (company_name)
                        SELECT (%s)
                        WHERE NOT EXISTS (SELECT 1 FROM companies WHERE company_name = (%s));
                        SELECT company_id FROM companies WHERE company_name = (%s)
                    """,
                    (company_name, company_name, company_name)
                )
                company_id = cur.fetchone()[0]
                cur.execute(
                    """
                    INSERT INTO vacancies (job_title,
                                           company_id,
                                           requirements,
                                           responsibility,
                                           experience,
                                           salary_from,
                                           salary_to,
                                           job_link)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (job_title,
                          company_id,
                          requirements,
                          responsibility,
                          experience,
                          salary_from,
                          salary_to,
                          job_link)
                )

        conn.commit()
        conn.close()
