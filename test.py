import pytest
from check_height_hero import check_height_hero, convert


def test_convert():
    assert convert('180 cm') == 180.0
    assert convert('240 meters') == 24000.0


def test_check_height_hero(requests_mock):
    # Мокаем ответ от API
    api_url = "https://akabab.github.io/superhero-api/api/all.json"
    mock_response = [
        {
            "name": "Hero1",
            "appearance": {
                "gender": "Male",
                "height": ["5 ft", "180 cm"]
            },
            "work": {"occupation": "Job1"}
        },
        {
            "name": "Hero2",
            "appearance": {
                "gender": "Male",
                "height": ["6 ft", "190 cm"]
            },
            "work": {"occupation": "Job2"}
        }
    ]
    requests_mock.get(api_url, json=mock_response)

    # Проверяем самого высокого героя
    tallest_hero = check_height_hero(api_url, "Male", True)  # Передаем api_url, gender и has_job
    assert tallest_hero['name'] == "Hero2"
    assert tallest_hero['height'] == 190.0


def test_check_height_hero_no_hero_found(requests_mock):
    api_url = "https://akabab.github.io/superhero-api/api/all.json"
    mock_response = []  # Пустой список, если героев нет
    requests_mock.get(api_url, json=mock_response)

    # Проверка, что героев не найдено
    tallest_hero = check_height_hero(api_url, "Unknown", True)  # Передаем api_url, gender и has_job
    assert tallest_hero is None
