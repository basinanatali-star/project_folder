from typing import List
from src.vacancy import Vacancy


def show_vacancies_preview(vacancies: List[Vacancy]) -> None:
    """Показать краткий список вакансий"""
    if not vacancies:
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"{i}. Название вакансии: {vacancy.name}")

        salary_display = vacancy.salary.get("display", "не указана") if vacancy.salary else "не указана"
        print(f"   Зарплата: {salary_display}")

        employer_name = vacancy.employer.get("name", "нет") if vacancy.employer else "нет"
        print(f"   Компания: {employer_name}")

        area_name = vacancy.area.get("name", "N/A") if vacancy.area else "N/A"
        print(f"   Регион: {area_name}")

        print(f"   Ссылка: {vacancy.url}")
        print("-" * 10)
