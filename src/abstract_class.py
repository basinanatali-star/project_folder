import requests
import json
from typing import List, Dict, Any, Union
from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями"""

    @abstractmethod
    def get_vacancies(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Получает вакансии по поисковому запросу"""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Проверяет подключения к API"""
        pass


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    __url: str
    __headers: Dict[str, str]
    __params: Dict[str, Union[Any, int]]
    __vacancies: List[Dict[str, Any]]

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"per_page": 100}
        self.__vacancies = []

    def connect(self) -> bool:
        """Публичный метод проверки подключения к API HH.ru"""
        return self.__connect()

    def __connect(self) -> bool:
        """Приватный метод проверки подключения к API HH.ru"""
        try:
            response = requests.get(self.__url, headers=self.__headers, timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_vacancies(self, search_query: str, **kwargs: Any) -> List[Dict[str, Any]]:
        """Получить вакансии по поисковому запросу с hh.ru"""
        if not self.__connect():
            print("Ошибка подключения к API HeadHunter")
            return []

        self.__vacancies.clear()
        params = {"text": search_query, "page": 0, "per_page": 100, **kwargs}

        while True:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=params, timeout=10)
                response.raise_for_status()

                data = response.json()
                vacancies_page = data.get("items", [])

                if not vacancies_page:
                    break

                self.__vacancies.extend(vacancies_page)
                params["page"] += 1
                total_pages = data.get("pages", 1)

                if params["page"] >= total_pages:
                    break

            except requests.exceptions.RequestException as e:
                print(f"Ошибка сети: {e}")
                break
            except json.JSONDecodeError as e:
                print(f"Ошибка JSON: {e}")
                break

        print(f"Получено {len(self.__vacancies)} вакансий")
        return self.__vacancies[:]
