import psycopg2

from src.config import config
from src.hh_load_vacancies import HeadHunterAPI


def db_create() -> None:
    """Функция создает DB для загрузки вакансий"""
    params = config()  # Получаем параметры для входа и создания DataBase

    conn = psycopg2.connect(dbname="postgres", **params)  # Коннект с DB
    conn.autocommit = True
    cur = conn.cursor()  # Курсор для работы с DB

    cur.execute(f"DROP DATABASE company")  # Удаление базы данных (обновляем)
    cur.execute(f"CREATE DATABASE company")  # Создание базы данных

    cur.close()  # Закрытие курсора
    conn.close()  # закрытие коннекта


def db_create_table() -> None:
    """Функция создает таблицы в DB"""
    params = config()
    conn = psycopg2.connect(dbname="company", **params)

    with conn.cursor() as cur:
        cur.execute(
            """
                CREATE TABLE company (
                    id SERIAL UNIQUE,
                    company_id INT PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL);
                CREATE TABLE vacancy (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES company(company_id),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary_from INT DEFAULT(0),
                    salary_to INT DEFAULT(0),
                    salary_currency VARCHAR(50),
                    url VARCHAR(255),
                    description TEXT)
            """
        )

    conn.commit()
    conn.close()


def load_to_database_company() -> None:
    """Функция записывает в DB данные о вакансиях"""
    params = config()
    conn = psycopg2.connect(dbname="company", **params)

    hh = HeadHunterAPI()  # создаем экз. класса ApiHH
    hh_employers = hh.load_vacancies()  # список компаний id и name
    hh_vacancy = hh.correct_vacancy(10)  # список вакансий

    for employer in hh_employers:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO company (company_id, company_name)
                VALUES (%s, %s)
                RETURNING company_id
                """,
                vars=(employer['id'], employer["name"]),
            )

            company_id = cur.fetchone()[0]

            for vacancy in hh_vacancy:
                if int(vacancy['employer']['id']) == int(company_id):
                    cur.execute(
                        """
                        INSERT INTO vacancy (company_id, vacancy_name, salary_from, salary_to, 
                        salary_currency, url, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            company_id,
                            vacancy["name"],
                            vacancy["salary"]["from"],
                            vacancy["salary"]["to"],
                            vacancy["salary"]["currency"],
                            vacancy["url"],
                            vacancy["snippet"]['responsibility'],
                        ),
                    )
                else:
                    continue

    conn.commit()
    conn.close()


if __name__ == '__main__':
    db_create('../database.ini')
    db_create_table('../database.ini')
    load_to_database_company('../database.ini')
