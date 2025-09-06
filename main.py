from config import PATH_TO_DB_INI
from src.creator_db import CreateDB
from src.head_hunter_api import HeadHunterAPI
from src.save_vacancy_to_db import SaveVacancyToDB


def user_interaction():
    """Основная функция для запуска приложения"""
    hh_api = HeadHunterAPI()
     # hh_api.get_items('employers/', {"text": "альфа",'only_with_vacancies': True, "page": 0, "per_page": 100})
    return hh_api.get_list_employers('сбер')
    # hh_vacancies = hh_api.get_vacancies()
    # new_db = CreateDB('vacancies')
    # new_db.create_new_db()
    # save = SaveVacancyToDB(new_db.database_name)
    # save.save_vacancy_to_database(hh_vacancies)
if __name__ == '__main__':
    print(user_interaction())
