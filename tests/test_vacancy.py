from typing import Dict, Any, List, Optional, Union
from src.vacancy import Vacancy


class TestVacancy:

    def test_safe_strip_empty(self) -> None:
        vacancy = Vacancy("Test", "http://test.com")
        assert vacancy._safe_strip(None) == "Не указано"
        assert vacancy._safe_strip("") == "Не указано"
        assert vacancy._safe_strip("  test  ") == "test"

    def test_init_basic(self) -> None:
        vacancy = Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/123",
            description="Работа с Python",
            requirements="Django, PostgreSQL"
        )
        assert vacancy.name == "Python Developer"
        assert vacancy.url == "https://hh.ru/vacancy/123"
        assert vacancy.description == "Работа с Python"
        assert vacancy.requirements == "Django, PostgreSQL"

    def test_init_with_salary(self) -> None:
        salary_data: Dict[str, Union[int, float, str]] = {
            "from": 150000.0,
            "to": 250000.0,
            "currency": "RUR"
        }
        vacancy = Vacancy("Dev", "url", salary=salary_data)
        assert vacancy.salary is not None
        assert vacancy.salary["from"] == 150000
        assert vacancy.salary["to"] == 250000

    def test_validate_salary_cases(self) -> None:
        vacancy = Vacancy("Test", "url")

        assert vacancy._validate_salary(None)["display"] == "Зарплата не указана"

        salary_from = vacancy._validate_salary({"from": 100000})
        assert salary_from["display"] == "от 100000 RUR"

        salary_to = vacancy._validate_salary({"to": 200000})
        assert salary_to["display"] == "до 200000 RUR"

        salary_exact = vacancy._validate_salary({"from": 150000, "to": 150000})
        assert salary_exact["display"] == "150000 RUR"

    def test_from_dict_hh_format(self) -> None:
        hh_data: Dict[str, Any] = {
            "id": "12345",
            "name": " Python dev ",
            "alternate_url": "https://hh.ru/vacancy/12345",
            "salary": {"from": 200000, "currency": "RUR"},
            "employer": {"name": "Yandex"},
            "area": {"name": "Москва"},
            "snippet": {
                "requirement": "Python",
                "responsibility": "Разработка "
            }
        }
        vacancy = Vacancy.from_dict(hh_data)
        assert vacancy.id == "12345"
        assert vacancy.name == "Python dev"
        assert vacancy.url == "https://hh.ru/vacancy/12345"
        assert vacancy.employer["name"] == "Yandex"
        assert "Москва" in vacancy.area["name"]
        assert "Python" in vacancy.description

    def test_avg_salary_calculation(self) -> None:
        no_salary = Vacancy("Test", "url")
        assert no_salary.avg_salary == 0.0

        from_salary = Vacancy("Test", "url", salary={"from": 100000})
        assert from_salary.avg_salary == 100000

        range_salary = Vacancy("Test", "url", salary={"from": 100000, "to": 200000})
        assert range_salary.avg_salary == 150000.0