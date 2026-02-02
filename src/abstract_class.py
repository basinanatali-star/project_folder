import requests
import json
from typing import List, Dict, Any, Union, Optional
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
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 100}
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

        self.__vacancies = []  # Очищаем предыдущие результаты
        self.__params['text'] = search_query
        self.__params['page'] = 0

        while self.__params.get('page',0) < 1:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)

                if response.status_code != 200:
                    print(f"Ошибка API: {response.status_code}")
                    break

                data = response.json()

                if 'items' not in data:
                    print("Неверный формат ответа API")
                    break

                vacancies_page: List[Dict[str, Any]] = data['items']
                self.__vacancies.extend(vacancies_page)
                self.__params['page'] += 1

                if self.__params['page'] >= data.get('pages', 1):
                    break

            except requests.exceptions.RequestException as e:
                print(f"Ошибка соединения: {e}")
                break

            except json.JSONDecodeError as e:
                print(f"Ошибка парсинга JSON: {e}")
                break

        return self.__vacancies


if __name__ == "__main__":
    api = HeadHunterAPI()

    # Тест подключения
    is_connected = api.connect()
    print(f"Подключение к API: {'Успешно' if is_connected else 'Не удалось'}")

    # 3. Получаем вакансии
    print("\nПолучаем вакансии по запросу 'Флорист'...")
    vacancies = api.get_vacancies("Флорист")

    # 4. Выводим результаты
    print(vacancies)
