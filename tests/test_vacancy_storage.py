import pytest
import os
from typing import Dict, Any, List
from pathlib import Path
from src.vacancy_storage import JSONVacancyStorage
from src.vacancy import Vacancy


class TestJSONVacancyStorage:

    @pytest.fixture
    def storage(self, tmp_path: Path) -> JSONVacancyStorage:
        filename: Path = tmp_path / "test_vacancies.json"
        return JSONVacancyStorage(str(filename))

    @pytest.fixture
    def test_vacancy_dict(self) -> Dict[str, Any]:
        return {
            "id": "12345",
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/12345",
            "salary": {"from": 150000, "to": 250000, "currency": "RUR"},
            "description": "Работа с Python"
        }

    @pytest.fixture
    def test_vacancy_object(self) -> Vacancy:
        return Vacancy(
            name="Python Developer",
            url="https://hh.ru/vacancy/12345",
            salary={"from": 150000, "to": 250000},
            id="12345"
        )

    def test_file_created(self, storage: JSONVacancyStorage) -> None:
        assert os.path.exists(storage.filename)
        assert os.path.getsize(storage.filename) > 0

    def test_read_empty_file(self, storage: JSONVacancyStorage) -> None:
        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert isinstance(vacancies, list)
        assert len(vacancies) == 0

    def test_add_vacancy_dict(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        result: bool = storage.add_vacancy(test_vacancy_dict)
        assert result is True

        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0]["id"] == "12345"
        assert vacancies[0]["name"] == "Python Developer"

    def test_add_vacancy_object(self, storage: JSONVacancyStorage, test_vacancy_object: Vacancy) -> None:
        result: bool = storage.add_vacancy(test_vacancy_object)
        assert result is True

        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0]["id"] == "12345"

    def test_no_duplicates(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        storage.add_vacancy(test_vacancy_dict)
        result: bool = storage.add_vacancy(test_vacancy_dict)
        assert result is False
        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert len(vacancies) == 1

    def test_get_vacancies_no_criteria(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        storage.add_vacancy(test_vacancy_dict)
        vacancies: List[Dict[str, Any]] = storage.get_vacancies()
        assert len(vacancies) == 1
        assert vacancies[0]["id"] == "12345"

    def test_get_vacancies_filter_id(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        storage.add_vacancy(test_vacancy_dict)
        vacancies: List[Dict[str, Any]] = storage.get_vacancies(id="12345")
        assert len(vacancies) == 1

    def test_delete_vacancy_exists(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        storage.add_vacancy(test_vacancy_dict)
        result: bool = storage.delete_vacancy("12345")
        assert result is True
        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert len(vacancies) == 0

    def test_clear_all(self, storage: JSONVacancyStorage, test_vacancy_dict: Dict[str, Any]) -> None:
        storage.add_vacancy(test_vacancy_dict)
        storage.clear_all()
        vacancies: List[Dict[str, Any]] = storage._read_vacancies()
        assert len(vacancies) == 0