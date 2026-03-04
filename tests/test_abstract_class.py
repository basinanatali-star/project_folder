import pytest
from typing import List
from src.abstract_class import HeadHunterAPI


class TestHeadHunterAPI:

    @pytest.fixture
    def api(self) -> HeadHunterAPI:
        return HeadHunterAPI()

    def test_connect_success(self, api: HeadHunterAPI) -> None:
        result = api.connect()
        assert result is True

    def test_connect_failure(self) -> None:
        api: HeadHunterAPI = HeadHunterAPI()
        assert api.connect()

    def test_get_vacancies_empty_query(self, api: HeadHunterAPI) -> None:
        vacancies: List[dict] = api.get_vacancies("")
        assert isinstance(vacancies, list)

    def test_get_vacancies_python_jobs(self, api: HeadHunterAPI) -> None:
        vacancies: List[dict] = api.get_vacancies("python разработчик")
        assert isinstance(vacancies, list)
        assert len(vacancies) > 0
        if vacancies:
            first: dict = vacancies[0]
            assert "name" in first
            assert "id" in first
