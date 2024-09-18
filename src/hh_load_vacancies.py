import requests

from src.base_hh_load_vacancies import BaseLoadVacancies


class HeadHunterAPI(BaseLoadVacancies):
    """Класс получает информацию о вакансиях с сайта HeadHunter"""

    def __init__(self, file_worker: str = "data/json_vacancies.json"):
        """Конструктор обьекта запроса инфо через API сервис"""

        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []  # конечный список, в который складываются вакансии list[dict]
        super().__init__(file_worker)

    def load_vacancies(self, keyword: str):
        """Метод загрузки данных вакансий из API сервиса"""

        self.__params["text"] = keyword
        while self.__params.get("page") != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)
            vacancies = response.json()["items"]
            self.__vacancies.extend(vacancies)
            self.__params["page"] += 1

        return self.__vacancies

    @property
    def vacancies(self):
        """Получение списка вакансий"""
        return self.__vacancies


if __name__ == "__main__":
    hh = HeadHunterAPI()  # Создаем экземпляр класса

    company_name = "Сбербанк"  # Динамическое название компаний
    hh.load_vacancies(company_name)  # Метод загрузки вакансий
    vacancy = hh.vacancies  # Получаем список вакансий

    # Получаем название компаний
    print([i['employer']['name'] for i in vacancy if company_name in i['employer']['name']])
