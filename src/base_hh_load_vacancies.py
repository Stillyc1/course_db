from abc import ABC, abstractmethod


class BaseLoadVacancies(ABC):
    """Базовый класс для получения вакансий из hh_api"""

    @abstractmethod
    def __init__(self, file_worker: str):
        """Атрибут в конструкторе для явного указания пути до файла, куда можно сохранить данные"""
        self.file_worker = file_worker

    @abstractmethod
    def load_vacancies(self) -> object:
        """Метод загрузки вакансий и сохранения в List[dict]"""
        pass
