import requests
import os
import logging
import dotenv
from statistics import mean, median
from salary_utils import predict_rub_salary

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
    try:
        response = requests.get(
            BASE_SJ_API_URL + sj_api_command,
            headers=SJ_HEADERS,
            params=payload
        )
        response.raise_for_status()
        if response.ok:
            vacancies = response.json()['total']
        return vacancies
    except (requests.exceptions.HTTPError, NameError):
        logging.exception("HTTPError")


def get_data(language):
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
        try:
            response = requests.get(
                BASE_SJ_API_URL + sj_api_command,
                headers=SJ_HEADERS,
                params=payload
            )
            response.raise_for_status()
            if response.ok:
                page_data = response.json()
                more = page_data["more"]
                page += 1
                whole_data["items"] += page_data["objects"]
            logging.debug(f"Language: {language} Page: {page}")
        except (requests.exceptions.HTTPError, NameError):
            logging.exception("HTTPError")
            break
    return whole_data


def get_average_salary(data):
    salaries = []
    tax = 1
    for item in data['items']:
        if item["currency"] == "rub":
            salaries_range = item["payment_from"], item["payment_to"], tax
            salary = predict_rub_salary(salaries_range)
            if salary is not None:
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
        data = get_data(language)
        average_salary, median_salary, vacancies_processed = get_average_salary(data)
        top_languages[language] = {}
        top_languages[language]["vacancies_found"] = get_vacancies_num(language)
        top_languages[language]["average_salary"] = average_salary
        top_languages[language]["median_salary"] = median_salary
        top_languages[language]["vacancies_processed"] = vacancies_processed
    return top_languages


if __name__ == '__main__':
    languages = [
        "Python",
        "Java",
        "PHP",
        "JavaScript",
        "Ruby",
        "C++",
        "C#",
        "Go",
        "Objective-C",
        "Scala",
        "Swift",
    ]
    sj_data = get_top_languages(languages)
    print(sj_data)
    pass
