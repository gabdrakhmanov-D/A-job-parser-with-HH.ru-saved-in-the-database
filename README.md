#  <p align="center">💼 HH.ru Vacancy Parser </p>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/poetry%2B-blueviolet?logo=python)
![PostgreSQL](https://img.shields.io/badge/postgresql-4169e1?style=for-the-badge&logo=postgresql&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-blue)

Программа для автоматизированного сбора информации о вакансиях с платформы **hh.ru** по заданным работодателям. Инструмент сохраняет данные в реляционную базу данных и предоставляет удобный интерфейс для их последующего анализа.

---

##  <p align="center">🚀 Основные возможности</p>
- Сбор данных о работодателях и их открытых вакансиях через API.
- Автоматическое создание структуры БД (таблицы компаний и вакансий).
- Хранение детальной информации: зарплаты, требования, ссылки, города.
- Вывод аналитических данных о вакансиях и компаниях.

##  <p align="center">🛠 Технологии
- **Язык:** Python
- **База данных:** PostgreSQL
- **Управление зависимостями:** Poetry
- **API:** HeadHunter API

---

##  <p align="center">📦 Установка и настройка  </p>

### 1. Клонирование репозитория  

    bash
    git clone git@github.com:gabdrakhmanov-D/A-job-parser-with-HH.ru-saved-in-the-database.git
    cd A-job-parser-with-HH.ru-saved-in-the-database
    
### 2.Установка зависимостей   
- Для работы используется менеджер пакетов poetry:

      bash
      poetry update

### 3. Конфигурация базы данных  
  1. Найдите в корне проект файл database.ini.example.
  2. Переименуйте его в database.ini.
  3. Заполните параметры подключения к вашей БД PostgreSQL (host, user, password, port).

### 4. Подготовка списка компаний
Для загрузки данных необходимо создать JSON-файл в директории data/.  
Формат файла:  
  
    json
    {
      "companies": [
        {"id": "1740", "name": "Яндекс"},
        {"id": "3529", "name": "Сбер"}
      ]
    }

Пути к файлам конфигурации можно изменить в модуле config.py.

---

##  <p align="center">💻 Использование  </p>
- Запустите основной файл программы:

      bash
      python main.py

- Или через poetry:

      bash
      poetry run python main.py

---

##  <p align="center">📂 Структура проекта (пакет src)</p>   

<table border="0" align="center">
  <tr>
      <th>Модуль</th>
    <th>Описание</th>
      
</tr>
      <tr>
        <th>head_hunter_api.py</th>
 <th>Класс HeadHunterAPI для взаимодействия с внешним API hh.ru.</th></tr>
            <tr>
      <th>vacancy_parser.py	</th>
      <th>Абстрактный класс для расширения парсеров.</th></tr>
                <tr> 
                <th>creator_db.py	</th>
                <th>Класс CreateDB: инициализация структуры таблиц в БД.</th></tr>
                 <tr>
      <th>save_vacancy_to_db.py	</th>
      <th>Класс SaveVacancyToDB: логика записи данных в таблицы.</th></tr>
      <tr>
        <th>db_manager.py	</th>
        <th>Класс DBManager: выполнение SQL-запросов и получение выборки данных.</th></tr>
        <tr>
          <th>vacancies.py</th>
          <th>Класс Vacancy: модель объекта вакансии.</th>
          </tr>
        <tr>
       <th>employer_info.py	</th>
      <th>Класс EmployerInfo: хранение детальной информации о работодателе.</th></tr>
        <tr>
       <th>foundemployers.py	</th>
       <th>Класс FoundEmployers: работа со списком найденных компаний.</th></tr>
      <tr>
      <th>utils.py	</th>  
      <th>Вспомогательные функции (работа с JSON, пользовательский ввод).</th>
  </tr>
</table>

## <p align="center">⚖️ Лицензия</p>  

<p align="center">Проект распространяется под лицензией MIT. Подробности в файле LICENSE.</p>  
