from src.database_connect import db_create, db_create_table, load_to_database_company
from src.dbmanager import DBManager
from src.config import config


def main():

    db_create()  # Функция создания DB
    db_create_table()  # Функция создания таблиц в DB
    load_to_database_company()  # Функция загрузки инфо о вакансиях в таблицы DB

    params = config()  # Задаем конфигурацию параметров для DB

    db_company = DBManager('company', params)

    user_enter = input("""\nВыберите действие:
1. Получить количество вакансий по каждой компании?
2. Получить все вакансии по каждой компании?
3. Получить среднюю зарплату по всем компаниям?
4. Вывести вакансии, у которых зарплата больше чем средняя по всем компаниям?
5. Вывести вакансии по ключевому слову в названии вакансии?\n""")

    if user_enter == "1":
        result = db_company.get_companies_and_vacancies_count()
        for res in result:
            print(f"{res[0]} - {res[1]} вакансий.")

    elif user_enter == "2":
        result = db_company.get_all_vacancies()
        for res in result:
            print(f"Компания: {res[0]}, Вакансия: {res[1]}, Зарплата: от {res[2]} до {res[3]} руб., Ссылка: {res[5]}")

    elif user_enter == "3":
        print(db_company.get_avg_salary())

    elif user_enter == "4":
        result = db_company.get_vacancies_with_higher_salary()
        for res in result:
            print(f"{res[2]}, зарплата: от {res[3]} до {res[4]} руб., ссылка: {res[6]}, описание: {res[7]}")

    elif user_enter == "5":
        keyword = input("Введите ключевое слово:\n").title()
        result = db_company.get_vacancies_with_keyword(f"{keyword}")

        for res in result:
            print(f"{res[2]}, зарплата: от {res[3]} до {res[4]} руб., ссылка: {res[6]}, описание: {res[7]}")


if __name__ == "__main__":
    main()
