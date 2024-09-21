import requests


def convert(height: str) -> float:
    if 'cm' in height:
        return float(height.replace(' cm', ''))
    elif 'meters' in height:
        return float(height.replace(' meters', '')) * 100
    else:
        return 0пше


def check_height_hero(api_url: str, gender: str, has_job: bool) -> dict:
    """Находит самого высокого героя с заданными параметрами."""
    response = requests.get(api_url)
    file = response.json()
    heroes = []
    for i in file:
        if i['appearance']['gender'] == gender and bool(i.get('work', {}).get('occupation', '')) == has_job: # Исправлено на явную проверку наличия ключа 'work'(совет AI)
            height = convert(i['appearance']['height'][1])
            heroes.append({'height': height, 'gender': gender, 'status_work': has_job, 'name': i['name']})
    if heroes:
        # Используем lambda функцию для сравнения по ключу 'height'
        max_height_hero = max(heroes, key=lambda hero: hero['height'])
        return max_height_hero
    else:
        return None

# Параметризация для API, пола героя и наличие работы.
if __name__ == '__main__':
    api_url = "https://akabab.github.io/superhero-api/api/all.json"
    gender = 'Male'  # Пол героя
    work = True  # Наличие работы
    hero = check_height_hero(api_url, gender, work)

    if hero:
        print(f"Самый высокий герой: {hero['name']}, Рост: {hero['height']} см")
    else:
        print("Герой не найден")