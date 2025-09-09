from src.creator_db import CreateDB
from src.db_manager import DBManager
from src.head_hunter_api import HeadHunterAPI
from src.save_vacancy_to_db import SaveVacancyToDB
from src.utils import (
    read_json,
    db_creation_request,
    get_list_titles_and_id,
    only_salary_request,
    get_command_from_user,
    get_result,
)


def user_interaction() -> None:
    """Основная функция для запуска приложения"""

    user_request_create_db = db_creation_request()
    db_name = input("Введите название базы данных\n").lower()

    if user_request_create_db == "1":
        try:
            new_db = CreateDB(db_name)
            new_db.create_new_db()
            new_db.create_tables()
            print("База данных успешно создана")
        except Exception as e:
            return print(f"Ошибка создания базы данных: {e}")

        try:
            list_id_employers = read_json()
        except FileNotFoundError as e:
            return print(f"Файл с ID компаний не найден: {e}")
        except Exception as e:
            return print(f"Возникла ошибка при чтении файла: {e}")

        ids_list, names_list = get_list_titles_and_id(list_id_employers)
        only_with_salary = only_salary_request()

        print("Сейчас будут загружены вакансии следующих компаний:")
        for employer_name in names_list:
            print(employer_name)

        hh_api = HeadHunterAPI()
        hh_vacancies = hh_api.get_vacancies(ids_list, only_with_salary)
        save_vacancies = SaveVacancyToDB(new_db.database_name)
        save_vacancies.save_vacancy_to_database(hh_vacancies)

    db_manager = DBManager(db_name)
    selector = get_command_from_user()
    get_result(db_manager, selector)


if __name__ == "__main__":
    user_interaction()
