from config import PATH_TO_DB_INI
from src.creator_db import CreateDB
from src.head_hunter_api import HeadHunterAPI
from src.save_vacancy_to_db import SaveVacancyToDB


def user_interaction():
    """Основная функция для запуска приложения"""
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies([3529, 1740,9498112, 80, 991318, 2180, 445136, 1455, 2748, 78638], True, '')

    new_db = CreateDB('vacancies')
    new_db.create_new_db()
    new_db.create_tables()
    save = SaveVacancyToDB(new_db.database_name)
    save.save_vacancy_to_database(hh_vacancies)
if __name__ == '__main__':
    a =user_interaction()

cv = [
      {3529: 'СБЕР'},
      {1740: 'Яндекс'},
      {9498112: 'Яндекс Крауд'},
      {80: 'Альфа-Банк'},
      {991318: 'WINLINE'},
      {2180: 'Ozon'},
      {445136:'ООО АйТи-Солюшн'},
      {1455: 'HeadHunter'},
      {2748: 'Ростелеком'},
      {78638: 'Т-Банк'}
      ]