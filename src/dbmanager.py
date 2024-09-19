import psycopg2

from src.config import config


class DBManager:
    """Класс для взаимодействия с базой данных"""

    def __init__(self, db_name: str, params_db: dict):
        self.avg_salary = None
        self.params_db = params_db  # Создаем параметры для кодключения
        self.db_name = db_name  # получаем имя базы данных

    def get_companies_and_vacancies_count(self):
        """Метод считает количество вакансий по каждой компании"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # создаем подключение к базе данных

        with conn.cursor() as cur:
            cur.execute(
                """
            SELECT company_name, COUNT(vacancy.company_id) FROM company
            INNER JOIN vacancy ON company.company_id=vacancy.company_id
            GROUP BY company_name
            """
            )
            result = cur.fetchall()
            # for res in result:
            #     print(res)

        conn.close()
        return result

    def get_all_vacancies(self):
        """Метод выводит список вакансий со всеми данными"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # создаем подключение к базе данных

        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT company_name, vacancy_name, salary_from, salary_to, salary_currency, url
                    FROM company
                    RIGHT JOIN vacancy USING(company_id)
                    """
            )
            result = cur.fetchall()

        conn.close()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # создаем подключение к базе данных

        with conn.cursor() as cur:
            cur.execute("""SELECT AVG(salary_from) FROM vacancy""")
            result = cur.fetchall()

        conn.close()
        average = str(result[0]).split("'")[1]

        self.avg_salary = float(average[0:8])

        return f"Средняя зарплата по всем вакансиям - {self.avg_salary} руб."

    def get_vacancies_with_higher_salary(self):
        """метод выводит список вакансий, у которых зарплата выше средней зарплаты"""
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # создаем подключение к базе данных

        with conn.cursor() as cur:
            cur.execute(
                """
                    SELECT * FROM vacancy
                    WHERE salary_to >= (SELECT AVG(salary_to) 
                    FROM vacancy)
                    """
            )
            result = cur.fetchall()

        conn.close()

        return result

    def get_vacancies_with_keyword(self, keyword):
        """Метод для вывода вакансий по ключевому слову в названии"""
        key_word = keyword.title()
        conn = psycopg2.connect(dbname=self.db_name, **self.params_db)  # создаем подключение к базе данных

        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancy WHERE vacancy_name LIKE '%{key_word}%'""")
            result = cur.fetchall()

        conn.close()

        return result


if __name__ == "__main__":
    params = config("../database.ini")
    test = DBManager("company", params)
    # print(test.get_companies_and_vacancies_count())
    # print(test.get_all_vacancies())
    # print(test.get_avg_salary())
    # print(test.get_vacancies_with_higher_salary())
    # print(test.get_vacancies_with_keyword("стажёр"))
