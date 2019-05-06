import requests
import os
import logging
import dotenv
from statistics import mean, median

dotenv.load_dotenv()

SJ_TOKEN = os.getenv("SJ_TOKEN")
SJ_HEADERS = {
    "X-Api-App-Id": SJ_TOKEN
}
BASE_SJ_API_URL = "https://api.superjob.ru/2.0/"

sj_api_command = "vacancies/"


def get_vacancies_num(language):
    payload = {
        "keywords[1][keys]": f"программист {language}",
        "t": 4,
        "no_agreement": 1
    }
    response = requests.get(
        BASE_SJ_API_URL + sj_api_command,
        headers=SJ_HEADERS,
        params=payload
    )
    if response.ok:
        vacancies = response.json()['total']
    return vacancies


def predict_rub_salary(vacancy):
    if vacancy["currency"] == "rub":
        if vacancy["payment_from"] != 0 and vacancy["payment_to"] != 0:
            return (vacancy["payment_from"] + vacancy["payment_to"]) / 2
        elif vacancy["payment_from"] == 0:
            return vacancy["payment_to"] * 0.8
        else:
            return vacancy["payment_from"] * 1.2


def get_avg_salary(language):
    page = 0
    whole_data = {"items": []}
    more = True
    while more:
        payload = {
            "keywords[1][keys]": f"программист {language}",
            "t": 4,
            "no_agreement": 1,
            "page": page,
            "count": 100
        }
        response = requests.get(
            BASE_SJ_API_URL + sj_api_command,
            headers=SJ_HEADERS,
            params=payload
        )
        if response.ok:
            page_data = response.json()
            more = page_data["more"]
            page += 1
            whole_data["items"] += page_data["objects"]
        logging.debug(f"Language: {language} Page: {page}")

    salaries = []
    for item in whole_data['items']:
        salary = predict_rub_salary(item)
        if salary != None:
            salaries.append(salary)
    try:
        avg_salary = int(mean(salaries))
        median_salary = int(median(salaries))
    except Exception:
        avg_salary, median_salary = None, None
    return avg_salary, median_salary, len(salaries)


def get_top_languages(languages):
    top_languages = {}
    for language in languages:
        average_salary, median_salary, vacancies_processed = get_avg_salary(language)
        top_languages[f"{language}"] = {}
        top_languages[f"{language}"]["vacancies_found"] = get_vacancies_num(language)
        top_languages[f"{language}"]["average_salary"] = average_salary
        top_languages[f"{language}"]["median_salary"] = median_salary
        top_languages[f"{language}"]["vacancies_processed"] = vacancies_processed
    return top_languages


if __name__ == '__main__':
    pass
