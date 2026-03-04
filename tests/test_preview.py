import pytest
from typing import List
from src.vacancy import Vacancy
from src.preview import show_vacancies_preview


class TestShowVacanciesPreview:

    def test_empty_vacancies_list(self, capsys: pytest.CaptureFixture[str]) -> None:

        vacancies: List[Vacancy] = []
        show_vacancies_preview(vacancies)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_one_vacancy_with_all_data(self, capsys: pytest.CaptureFixture[str]) -> None:

        vacancy = Vacancy(
            name="Python Developer",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            employer={"name": "Яндекс"},
            area={"name": "Москва"},
            url="https://hh.ru/vacancy/123"
        )
        vacancies = [vacancy]
        show_vacancies_preview(vacancies)
        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')

        assert lines[0] == "1. Название вакансии: Python Developer"
        assert "Зарплата:" in lines[1]
        assert lines[2] == "   Компания: Яндекс"
        assert lines[3] == "   Регион: Москва"
        assert lines[4] == "   Ссылка: https://hh.ru/vacancy/123"
        assert lines[5] == "----------"

    def test_vacancy_without_salary(self, capsys: pytest.CaptureFixture[str]) -> None:

        vacancy = Vacancy(
            name="Java Developer",
            salary=None,
            employer={"name": "Google"},
            area={"name": "СПб"},
            url="https://hh.ru/vacancy/456"
        )
        vacancies = [vacancy]

        show_vacancies_preview(vacancies)
        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')
        assert lines[0] == "1. Название вакансии: Java Developer"
        assert lines[1] == "   Зарплата: Зарплата не указана"
        assert lines[2] == "   Компания: Google"
        assert lines[3] == "   Регион: СПб"
        assert lines[4] == "   Ссылка: https://hh.ru/vacancy/456"
        assert lines[5] == "----------"

    def test_multiple_vacancies(self, capsys: pytest.CaptureFixture[str]) -> None:

        vacancies = [
            Vacancy(
                name="Python Developer",
                salary={"from": 40000,"to": 0, "currency": "RUR", "display": "от 40000 RUR"},
                employer={"name": "Яндекс"},
                area={"name": "Москва"},
                url="https://hh.ru/vacancy/123"
            ),
            Vacancy(
                name="Java Developer",
                salary={"from": 0, "to": 0, "currency": "не указана", "display": "Зарплата не указана"},
                employer={"name": "Google"},
                area={"name": "СПб"},
                url="https://api.hh.ru/employers/1383228"
            )
        ]

        show_vacancies_preview(vacancies)
        captured = capsys.readouterr()
        lines = captured.out.strip().split('\n')

        assert lines[0] == "1. Название вакансии: Python Developer"
        assert "Зарплата:" in lines[1]
        assert lines[2] == "   Компания: Яндекс"
        assert lines[3] == "   Регион: Москва"
        assert lines[4] == "   Ссылка: https://hh.ru/vacancy/123"
        assert lines[5] == "----------"
        assert lines[6] == "2. Название вакансии: Java Developer"
        assert lines[7] == "   Зарплата: Зарплата не указана"
        assert lines[8] == "   Компания: Google"
        assert lines[9] == "   Регион: СПб"
        assert lines[10] == "   Ссылка: https://api.hh.ru/employers/1383228"
        assert lines[11] == "----------"