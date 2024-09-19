import psycopg2

from src.config import config
from src.hh_load_vacancies import HeadHunterAPI


def db_create():
    """Функция создает DB для загрузки вакансий"""
    params = config()  # Получаем параметры для входа и создания DataBase

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE company")
    cur.execute(f"CREATE DATABASE company")

    conn.close()


def db_create_table():
    """Функция создает таблицы в DB"""
    params = config()
    conn = psycopg2.connect(dbname='company', **params)

    with conn.cursor() as cur:
        cur.execute("""
                CREATE TABLE company (
                    company_id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL,
                    company_url VARCHAR(255));
                CREATE TABLE vacancy (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES company(company_id),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary_from VARCHAR(50),
                    salary_to VARCHAR(50),
                    salary_currency VARCHAR(50),
                    url VARCHAR(255),
                    description TEXT)
            """)

    conn.commit()
    conn.close()


def load_to_database_company(company_list):
    """Функция записывает в DB данные о вакансиях"""
    params = config()
    conn = psycopg2.connect(dbname='company', **params)

    for company in company_list:
        hh = HeadHunterAPI()
        hh.load_vacancies(company)
        hh.correct_vacancy()
        vacancy_list = hh.vacancies

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO company (company_name, company_url)
                VALUES (%s, %s)
                RETURNING company_id
                """, vars=(company, vacancy_list[0]['employer']['url'])
            )

            company_id = cur.fetchone()[0]

            for vacancy in vacancy_list:
                cur.execute(
                    """
                    INSERT INTO vacancy (company_id, vacancy_name, salary_from, salary_to, 
                    salary_currency, url, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (company_id, vacancy['name'], vacancy['salary']['from'],
                     vacancy['salary']['to'], vacancy['salary']['currency'],
                     vacancy['url'], vacancy['description'])
                )

    conn.commit()
    conn.close()
