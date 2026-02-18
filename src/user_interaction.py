from src.abstract_class import HeadHunterAPI
from src.vacancy import Vacancy
from src.vacancy_storage import JSONVacancyStorage
from src.preview import show_vacancies_preview
from typing import List

SourceType = str


def user_interaction() -> None:
    """Основная функция для взаимодействия с пользователем через консоль"""
    hh_api = HeadHunterAPI()
    storage = JSONVacancyStorage("my_vacancies.json")
    storage_filter = JSONVacancyStorage("vacancies_filter.json")

    current_vacancies: List[Vacancy] = []  # ← Добавлена аннотация
    current_source: SourceType = ""

    print("\n" + "=" * 60)
    print("ПРОГРАММА ДЛЯ ПОИСКА ВАКАНСИЙ НА hh.ru")
    print("=" * 60)

    while True:
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1. Поиск вакансий по запросу")
        print("2. Топ N вакансий по зарплате в полученном запросе")
        print("3. Фильтрация полученных вакансий по ключевому слову")
        print("4. Сохранение текущих вакансий в отдельное хранилище")
        print("5. Удалить вакансию по ID")
        print("6. Очистить все вакансии")
        print("7. Статистика вакансий по зарплате в полученном запросе")
        print("0. Выход")
        print("-" * 60)

        choice = input("Выберите действие (0-7): ").strip()

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            current_vacancies, current_source = search_vacancies(hh_api, storage)

        elif choice == "2":
            current_vacancies, current_source = show_top_salaries(storage)

        elif choice == "3":
            current_vacancies, current_source = filter_by_keyword(storage)

        elif choice == "4":
            save_current_vacancies(current_vacancies, storage_filter)

        elif choice == "5":
            delete_vacancy(storage, storage_filter)

        elif choice == "6":
            clear_all_vacancies(storage, storage_filter)
            current_vacancies.clear()

        elif choice == "7":
            show_statistics(storage)

        else:
            print("Неверный выбор! Попробуйте снова.")


def search_vacancies(hh_api: HeadHunterAPI, storage: JSONVacancyStorage) -> tuple[list, str]:
    """Поиск вакансий по запросу"""
    query = input("\nВведите название вакансии для поискового запроса: ").strip().lower()

    if not query:
        print("Запрос не может быть пустым!\n")
        return [], "Запрос пустой"

    print("\nПолучение вакансий...")
    vacancies_data = hh_api.get_vacancies(query)

    if not vacancies_data:
        print("Вакансии не найдены!\n")
        return [], "Вакансии не найдены"

    vacancies = Vacancy.cast_to_object_list(vacancies_data)
    message = f"Сохранено {len(vacancies)} вакансий"
    print(f"Все {len(vacancies)} вакансий сохранены в основное хранилище\n")

    for vacancy in vacancies:
        storage.add_vacancy(vacancy)

    show_vacancies_preview(vacancies[:5])

    return vacancies, message


def show_top_salaries(storage: JSONVacancyStorage) -> tuple[list, str]:
    """Показать топ N вакансий по зарплате"""
    vacancies_data = storage.get_vacancies()

    if not vacancies_data:
        print("\nНет сохраненных вакансий! Сначала выполните поиск вакансий для вывода в топ.\n")
        return [], "Нет вакансий"

    try:
        n = int(input(f"Bвeдитe количество вакансий для вывода в топ от 1 до {len(vacancies_data)}: "))

    except ValueError:
        print("Введите корректное число!")
        return [], "Введите корректное число"

    vacancies = Vacancy.cast_to_object_list(vacancies_data)
    valid_vacancies = [v for v in vacancies if v.avg_salary is not None]
    sorted_vacancies = sorted(valid_vacancies, key=lambda v: v.avg_salary, reverse=True)

    print(f"\n ТОП {n} ВАКАНСИЙ ПО ЗАРПЛАТЕ:")
    print("-" * 60)

    show_vacancies_preview(sorted_vacancies[:n])
    return sorted_vacancies[:n], f"Топ-{n} по зарплате показан"


def filter_by_keyword(storage: JSONVacancyStorage) -> tuple[list, str]:
    """Фильтр вакансий по ключевому слову"""

    vacancies_data = storage.get_vacancies()

    if not vacancies_data:
        print("\nНет сохраненных вакансий! Сначала выполните поиск вакансий.\n")
        return [], "нет вакансий"

    keyword = input("\nВведите ключевое слово для фильтрации вакансий: ").strip().lower()

    if not keyword:
        print("\nКлючевое слово не может быть пустым!\n")
        return [], "пустое поле"

    print(f"\nВсего вакансий в хранилище: {len(vacancies_data)}")

    filtered = []

    for vacancy_dict in vacancies_data:
        text_for_search = ""

        name = vacancy_dict.get("name")
        if name and isinstance(name, str):
            text_for_search += name.lower() + " "

        description = vacancy_dict.get("description")
        if description and isinstance(description, str):
            text_for_search += description.lower() + " "

        requirements = vacancy_dict.get("requirements")
        if requirements and isinstance(requirements, str):
            text_for_search += requirements.lower() + " "

        if keyword in text_for_search:
            filtered.append(vacancy_dict)

    if not filtered:
        print(f"\nНайдено {len(filtered)} вакансий с ключом '{keyword}'\n")
        return [], f"фильтрации по ключевому слову '{keyword}'"
    else:
        print(f"\nНайдено {len(filtered)} вакансий с ключом '{keyword}'\n")

        for i, v in enumerate(filtered[:10], 1):
            print(f"{i}. {v.get('name', 'Без названия')}")

        filtered_objects = Vacancy.cast_to_object_list(filtered)
        return filtered_objects, f"фильтрации по ключевому слову '{keyword}'"


def save_current_vacancies(vacancies: list, storage_filter: JSONVacancyStorage) -> None:
    """Сохранить текущие вакансии"""

    if not vacancies:
        print("\nНет вакансий для сохранения! Сначала выполните поиск, фильтрацию или выведите топ вакансий.")
        return

    print("\n--- Сохранение вакансий ---")
    print("1. Сохранить все")
    print("2. Сохранить выборочно")
    print("3. Не сохранять")

    choice = input("Выберите действие (1-3): ").strip()

    if choice == "1":
        added = 0
        for vacancy in vacancies:
            if storage_filter.add_vacancy(vacancy):
                added += 1
        print(f"Сохранено {added} новых вакансий")
        return

    elif choice == "2":
        saved = 0
        for i, vacancy in enumerate(vacancies[:10], 1):
            name = vacancy.name if hasattr(vacancy, "name") else vacancy.get("name", "Без названия")
            print(f"\n{i}. {name}")

            if input("Сохранить? (д/н): ").lower() in ["д", "да", "y", "yes"]:
                if storage_filter.add_vacancy(vacancy):
                    saved += 1
                    print("Сохранено")
                else:
                    print("Уже существует")
        print(f"\nИтого сохранено: {saved}")
        return

    elif choice == "3":
        print("Сохранение отменено")
        return
    else:
        print("Некорректный выбор! Введите 1, 2 или 3.")


def delete_vacancy(storage: JSONVacancyStorage, storage_filter: JSONVacancyStorage) -> None:
    """Удалить вакансию по ID"""

    vacancy_id = input("Введите ID вакансии для удаления: ").strip()
    if not vacancy_id:
        print("\nID не может быть пустым!")
        return

    if input("Удалить вакансию в основном хранилище? (д/н): ").lower() in ["д", "да", "y", "yes"]:
        storage.delete_vacancy(vacancy_id)
        print("в основном хранилище")
    elif input("Удалить вакансию в отдельном хранилище? (д/н): ").lower() in ["д", "да", "y", "yes"]:
        storage_filter.delete_vacancy(vacancy_id)
        print("в отдельном хранилище")
        return


def clear_all_vacancies(storage: JSONVacancyStorage, storage_filter: JSONVacancyStorage) -> None:
    """Очистить все вакансии"""

    if input("Удалить все вакансии в основном хранилище? (д/н): ").lower() in ["д", "да", "y", "yes"]:
        storage.clear_all()
        print("в основном хранилище")
    elif input("Удалить все вакансии в отдельном хранилище? (д/н): ").lower() in ["д", "да", "y", "yes"]:
        storage_filter.clear_all()
        print("в отдельном хранилище")
        return


def show_statistics(storage: JSONVacancyStorage) -> None:
    """Показать статистику"""
    vacancies_data = storage.get_vacancies()
    if not vacancies_data:
        print("\nНет данных для статистики!")
        return

    vacancies = Vacancy.cast_to_object_list(vacancies_data)
    salaries = [v.avg_salary for v in vacancies if v.avg_salary > 0]

    if salaries:
        avg_salary = sum(salaries) / len(salaries)
        max_salary = max(salaries)
        min_salary = min(salaries)
        with_salary = len([v for v in vacancies if v.avg_salary > 0])

        print("\nСТАТИСТИКА ВАКАНСИЙ ПО ЗАРПЛАТЕ:")
        print("-" * 40)
        print(f"Всего вакансий: {len(vacancies)}")
        print(f"С зарплатой: {with_salary} вакансий")
        print(f"Средняя з/п: {round(avg_salary, 2)} руб.")
        print(f"Макс з/п: {round(max_salary, 2)} руб.")
        print(f"Мин з/п: {round(min_salary, 2)} руб.")
    else:
        print("Нет вакансий с указанной зарплатой")
