
class Vacancy:
    """Класс для работы с вакансиями"""
    name_vacancy: str
    link_url: str
    salary: dict | None
    description: str


    def __init__(self, name_vacancy: str, link_url: str, salary: dict | None, description: str):

        self.name_vacancy = name_vacancy
        self.link_url = link_url
        self.salary = self._validate_salary(salary)
        self.description = description

    @staticmethod
    def _validate_salary(salary_data: dict | None) -> dict:
        """Валидация данных о зарплате"""
        if not salary_data:
            return {
                "from": 0,
                "to": 0,
                "currency": "не указана",
                "display": "Зарплата не указана"
            }

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

        return {
            "from": salary_from,
            "to": salary_to,
            "currency": currency,
            "display": display_text
        }

    @property
    def avg_salary(self) -> float:
        """ Вычисляет среднюю зарплату для сравнения"""

        if self.salary["from"] == 0 and self.salary["to"] == 0:
            return 0.0
        elif self.salary["from"] == 0:
            return float(self.salary["to"])
        elif self.salary["to"] == 0:
            return float(self.salary["from"])
        else:
            return (self.salary["from"] + self.salary["to"]) / 2

    def __eq__(self, other) -> bool:
        """Проверка на равенство по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary == other.avg_salary

    def __lt__(self, other) -> bool:
        """Проверка на меньше по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary < other.avg_salary

    def __le__(self, other) -> bool:
        """Проверка на меньше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other) -> bool:
        """Проверка на больше по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary > other.avg_salary

    def __ge__(self, other) -> bool:
        """Проверка на больше или равно по средней зарплате"""
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.avg_salary >= other.avg_salary

    @classmethod
    def from_dict(cls, data: dict) -> 'Vacancy':
        """Создание вакансии из словаря"""
        return cls(
            name_vacancy=data.get('title', ''),
            link_url=data.get('url', ''),
            salary=data.get('salary'),
            description=data.get('description', '')
        )


if __name__ == "__main__":
    # Создаем тестовые вакансии
    vacancy1 = Vacancy(
        name_vacancy="Python разработчик",
        link_url="https://hh.ru/vacancy/123",
        salary={"from": 100000, "to": 150000, "currency": "RUR"},
        description="Требуется опыт работы с Django, Flask, знание SQL."
    )

    vacancy2 = Vacancy(
        name_vacancy="Data Scientist",
        link_url="https://hh.ru/vacancy/456",
        salary={"from": 150000, "to": 200000, "currency": "RUR"},
        description="Анализ данных, машинное обучение, Python."
    )

    vacancy3 = Vacancy(
        name_vacancy="Стажер программист",
        link_url="https://hh.ru/vacancy/789",
        salary=None,  # Зарплата не указана
        description="Обучение программированию на Python."
    )

    # Выводим информацию о вакансиях
    print("Вакансия 1:")
    print(vacancy1)

    print("Вакансия 2:")
    print(vacancy2)

    print("Вакансия 3:")
    print(vacancy3)

    # Сравниваем вакансии по зарплате
    print(f"vacancy1 > vacancy2: {vacancy1 > vacancy2}")
    print(f"vacancy1 < vacancy2: {vacancy1 < vacancy2}")
    print(f"vacancy3 == 0: {vacancy3.avg_salary == 0}")

    # Создание из словаря (имитация данных с API)
    api_data = {
        "name": "Backend разработчик",
        "alternate_url": "https://hh.ru/vacancy/999",
        "salary": {"from": 120000, "to": None, "currency": "RUR"},
        "snippet": {"requirement": "Опыт работы от 2 лет"}
    }

    vacancy4 = Vacancy.from_dict(api_data)
    print("\nВакансия из API данных:")
    print(vacancy4)

    # Сортировка списка вакансий
    vacancies = [vacancy1, vacancy2, vacancy3, vacancy4]
    sorted_vacancies = sorted(vacancies, reverse=True)

    print("\nВакансии, отсортированные по зарплате (по убыванию):")
    for vac in sorted_vacancies:
        print(f"{vac.link_url}: {vac.salary['display']}")