import json

from config import PATH_TO_EMPLOYERS_ID
from src.creator_db import CreateDB
from src.db_manager import DBManager


def read_json(file=PATH_TO_EMPLOYERS_ID) -> dict:
    """Функция для чтения файла json"""
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def db_creation_request() -> str:
    """ Запрос пользователя о создании БД """
    while True:
        result = input(
            "Выберите вариант: \n"
            "1. Скачать вакансии и сохранить их в новую базу данных.\n"
            "2. Открыть существующую базу данных с вакансиями.\n"
        )
        if result not in ["1", "2"]:
            print("Вы ввели недопустимое значение, повторите попытку")
        else:
            return result


def get_list_titles_and_id(list_id_employers: list) -> tuple[list, list]:
    """ Функция для возврата списков ID и названий компаний """
    ids_list = []
    names_list = []
    for employer in list_id_employers:
        for employer_id, employer_name in employer.items():
            ids_list.append(int(employer_id))
            names_list.append(employer_name)
    return ids_list, names_list


def only_salary_request() -> bool:
    """ Запрос пользователя о загрузке вакансий с указанием или нет зарплаты """
    while True:
        with_salary = input(
            "Вы хотите загрузить вакансии в которых указана зарплата?\n Да/Нет: "
        ).lower()
        if with_salary == "да":
            return True
        elif with_salary == "нет":
            return False
        print("Вы ввели некорректное значение, повторите ввод.")


def get_command_from_user():
    """ Запрос пользователя о выборе выдачи результата """
    while True:
        selector = input(
            "Выберите команду которую необходимо выполнить:\n"
            "1. Получить список всех компаний и количество вакансий у каждой компании.\n"
            "2. Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.\n"
            "3. Получить среднюю зарплату по вакансиям.\n"
            "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.\n"
            "5. Получить список всех вакансий, в названии которых содержатся ключевое слово\n"
            "0. Для выхода из программы. \n"
        )
        if selector in ["0", "1", "2", "3", "4", "5"]:
            return selector
        print("Вы ввели некорректное значение, повторите ввод.")


def get_result(db_manager: DBManager, selector) -> None:
    """ Функция для печати результата в консоль """
    if selector == "1":
        print(db_manager.get_companies_and_vacancies_count())

    elif selector == "2":
        print(db_manager.get_all_vacancies())

    elif selector == "3":
        print(f'Cредняя зарплата по вакансиям: {db_manager.get_avg_salary()} RUB')

    elif selector == "4":
        print(db_manager.get_vacancies_with_higher_salary())

    elif selector == "5":
        keyword = input("Введите слово, которое содержится в вакансии: ")
        print(db_manager.get_vacancies_with_keyword(keyword))


def chek_db(db_name: str) -> bool:
    db_found = CreateDB(db_name).chek_db()
    create = False

    if not db_found:
        user_request_to_create = input(
            'Такой базы данных не существует, вы хотите её создать и сохранить в неё вакансии?\n Да/Нет   ').lower()
        if user_request_to_create == 'да':
            create = True
            return create
    return create
