import psycopg2

from src.creator_db import CreateDB


class SaveVacancyToDB(CreateDB):
    def __init__(self, database_name):
        super().__init__(database_name)
        self.__config_db = self.get_config()

    def save_vacancy_to_database(self, list_employers_and_vacancies) -> None:
        """ Сохранение данных о вакансии в базу данных."""

        conn = psycopg2.connect(dbname=self.database_name, **self.__config_db)
        with conn.cursor() as cur:
            for item in list_employers_and_vacancies:
                for employer, vacancies in item.items():
                    employer_id = employer.employer_id
                    name = employer.name
                    city = employer.city
                    url = employer.url
                    employer_url = employer.employer_url

                    cur.execute(
                        """
                            INSERT INTO employers (external_id, name, city, url, link_to_profile)
                            VALUES (%s, %s, %s, %s, %s)
                            RETURNING id
                        """,
                        (employer_id, name, city, url, employer_url)
                    )
                    employer_id = cur.fetchone()[0]
                    for vacancy in vacancies:
                        job_title = vacancy.job_title
                        requirements = vacancy.requirements
                        responsibility = vacancy.responsibility
                        salary_from = vacancy.salary_from
                        salary_to = vacancy.salary_to
                        job_link = vacancy.job_link
                        experience = vacancy.experience
                        cur.execute(
                            """
                            INSERT INTO vacancies (job_title,
                                                   employer_id,
                                                   requirements,
                                                   responsibility,
                                                   experience,
                                                   salary_from,
                                                   salary_to,
                                                   job_link)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT DO NOTHING;
                            """,
                            (job_title,
                                  employer_id,
                                  requirements,
                                  responsibility,
                                  experience,
                                  salary_from,
                                  salary_to,
                                  job_link)
                        )

        conn.commit()
        conn.close()
