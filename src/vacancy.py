from typing import List, Dict, Any, Optional, Union


class Vacancy:
    """Класс для работы с вакансиями"""

    name: str
    url: str
    salary: Optional[Dict[str, Union[int, float, str]]]
    description: str
    requirements: str

    @staticmethod
    def _safe_strip(value: Any) -> str:
        """Безопасно убирает пробелы, если не None"""
        return (str(value or "")).strip() or "Не указано"

    def __init__(
        self,
        name: Any,
        url: Any,
        salary: Optional[Dict[str, Union[int, float, str]]] = None,
        description: str | None = None,
        requirements: str | None = None,
        **kwargs: Any,
    ) -> None:

        self.name = self._safe_strip(name)
        self.url = self._safe_strip(url)
        self.description = self._safe_strip(description)
        self.requirements = self._safe_strip(requirements)
        self.salary = self._validate_salary(salary) or {}
        self.id = kwargs.get("id")
        self.employer = kwargs.get("employer", {})
        self.area = kwargs.get("area", {})

    @staticmethod
    def _validate_salary(salary_data: dict | None) -> dict:
        """Валидация данных о зарплате"""
        if not salary_data:
            return {"from": 0, "to": 0, "currency": "не указана", "display": "Зарплата не указана"}

        salary_from = salary_data.get("from", 0) or 0
        salary_to = salary_data.get("to", 0) or 0
        currency = salary_data.get("currency", "RUR")

        if salary_from == 0 and salary_to == 0:
            display_text = "Зарплата не указана"
        elif salary_from == 0:
            display_text = f"до {salary_to} {currency}"
        elif salary_to == 0:
            display_text = f"от {salary_from} {currency}"
        elif salary_from == salary_to:
            display_text = f"{salary_from} {currency}"
        else:
            display_text = f"от {salary_from} до {salary_to} {currency}"

        return {"from": salary_from, "to": salary_to, "currency": currency, "display": display_text}

    @property
    def avg_salary(self) -> float:
        """Вычисляет среднюю зарплату для сравнения"""
        if self.salary is None:
            return 0.0

        from_salary = float(self.salary.get("from", 0) or 0)
        to_salary = float(self.salary.get("to", 0) or 0)

        if from_salary == 0 and to_salary == 0:
            return 0.0
        elif from_salary == 0:
            return to_salary
        elif to_salary == 0:
            return from_salary
        else:
            return (from_salary + to_salary) / 2

    def __eq__(self, other: object) -> bool:
        """Проверка на равенство по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other: object) -> bool:
        """Проверка на меньше по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other: object) -> bool:
        """Проверка на меньше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: object) -> bool:
        """Проверка на больше по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: object) -> bool:
        """Проверка на больше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Vacancy":
        """Создает объект Vacancy из словаря API HH.ru"""
        snippet = data.get("snippet", {})
        return cls(
            name=data.get("name"),
            url=(data.get("alternate_url") or data.get("url") or data.get("apply_alternate_url") or "Не указано"),
            salary=data.get("salary"),
            description=snippet.get("requirement", ""),
            requirements=snippet.get("responsibility", ""),
            id=data.get("id"),
            employer=data.get("employer", {}),
            area=data.get("area", {}),
        )

    @staticmethod
    def cast_to_object_list(vacancy_list: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список словарей в список объектов Vacancy"""
        return [Vacancy.from_dict(vacancy_data) for vacancy_data in vacancy_list]
