import json
import os

VACANCY_FILE = "data/vacancies.json"


def load_vacancies():
    if not os.path.exists(VACANCY_FILE) or os.stat(VACANCY_FILE).st_size == 0:
        return {}
    with open(VACANCY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_vacancies(data):
    os.makedirs(os.path.dirname(VACANCY_FILE), exist_ok=True)
    with open(VACANCY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_vacancy(region, branch, vacancy):
    data = load_vacancies()
    branch_key = branch["title"]["en"]
    data.setdefault(region, {}).setdefault(branch_key, []).append(vacancy)
    save_vacancies(data)

def get_vacancies(region, branch_title):
    data = load_vacancies()
    return data.get(region, {}).get(branch_title, [])


def delete_vacancy(region, branch, index):
    data = load_vacancies()
    branch_key = branch["title"]["en"]
    if region in data and branch_key in data[region] and index < len(data[region][branch_key]):
        del data[region][branch_key][index]
        save_vacancies(data)
        return True
    return False

