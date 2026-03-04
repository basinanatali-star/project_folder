import json
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Union
from src.vacancy import Vacancy


class VacancyStorage(ABC):
    """Абстрактный класс для работы с хранилищем вакансий"""

    @abstractmethod
    def add_vacancy(self, vacancy: Dict[str, Any]) -> bool:
        """Добавляет вакансию в файл"""
        pass

    @abstractmethod
    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """Получает вакансии по указанным критериям"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаляет вакансию по ID"""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Удаляет все вакансии"""
        pass


class JSONVacancyStorage(VacancyStorage):
    """Класс для сохранения информации о вакансиях в JSON-файл"""

    def __init__(self, filename: str = "vacancies.json") -> None:

        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Проверяет существование файла и создает его при необходимости"""
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file)

    def _read_vacancies(self) -> List[Dict[str, Any]]:
        """Читает все вакансии из файла"""
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data: List[Dict[str, Any]] = json.load(file)  # ← Явная типизация
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Записывает вакансии в файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=2)

    @staticmethod
    def _vacancy_to_dict(vacancy: Union[Vacancy, Dict[str, Any]]) -> Dict[str, Any]:
        """Преобразует вакансию в словарь, если это объект Vacancy"""
        if isinstance(vacancy, dict):
            return vacancy.copy()
        elif hasattr(vacancy, "to_dict"):
            result = vacancy.to_dict()
            if isinstance(result, dict):
                return result
        elif hasattr(vacancy, "__dict__"):
            return dict(vacancy.__dict__)

        return {
            "id": getattr(vacancy, "id", None),
            "name": getattr(vacancy, "name", ""),
            "url": getattr(vacancy, "url", ""),
            "salary": getattr(vacancy, "salary", None),
            "description": getattr(vacancy, "description", ""),
            "requirements": getattr(vacancy, "requirements", ""),
        }

    @staticmethod
    def _get_vacancy_id(vacancy: Union[Vacancy, Dict[str, Any]]) -> str:
        """Получает ID вакансии из объекта или словаря"""
        if isinstance(vacancy, dict):
            return vacancy.get("id") or vacancy.get("vacancy_id") or ""
        else:
            return getattr(vacancy, "id", getattr(vacancy, "vacancy_id", ""))

    def add_vacancy(self, vacancy: Union[Vacancy, Dict[str, Any]]) -> bool:
        """Добавляет вакансию, избегая дубликатов"""
        vacancy_dict = self._vacancy_to_dict(vacancy)
        vacancy_id = vacancy_dict.get("id")

        if not vacancy_id or self._is_vacancy_exists(vacancy_id):
            return False

        vacancies = self._read_vacancies()
        vacancies.append(vacancy_dict)
        self._write_vacancies(vacancies)
        return True

    def _is_vacancy_exists(self, vacancy_id: str) -> bool:
        """Проверяет существование вакансии по ID"""
        vacancies = self._read_vacancies()
        return any(v.get("id") == vacancy_id for v in vacancies)

    def get_vacancies(self, **criteria: Any) -> List[Dict[str, Any]]:
        """Получает вакансии по указанным критериям"""

        vacancies = self._read_vacancies()

        if not criteria:
            return vacancies

        filtered_vacancies = []

        for vacancy in vacancies:
            match = True

            for key, value in criteria.items():
                vacancy_value = vacancy.get(key, None)

                if vacancy_value is None:
                    match = False
                    break

                if isinstance(value, str) and isinstance(vacancy_value, str):
                    if value.lower() not in vacancy_value.lower():
                        match = False
                        break

                elif vacancy_value != value:
                    match = False
                    break
            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str) -> bool:
        """Удаляет вакансию по ID"""
        vacancies = self._read_vacancies()

        initial_count = len(vacancies)
        vacancies = [v for v in vacancies if v.get("id") != vacancy_id]

        if len(vacancies) < initial_count:
            self._write_vacancies(vacancies)
            print(f"Вакансия с ID {vacancy_id} удалена")
            return True
        print(f"Вакансия с ID {vacancy_id} не найдена")
        return False

    def clear_all(self) -> None:
        """Удаляет все вакансии из файла"""
        self._write_vacancies([])
        print("Все вакансии удалены")
