import requests
import logging
from statistics import mean, median
from salary_utils import predict_rub_salary


BASE_API_HH_URL = "https://api.hh.ru/"
HH_HEADERS = {
    "User-Agent": "HH-User-Agent"
}
hh_api_command = "vacancies"


def get_vacancies_num(language):
    payload = {
        "text": f"программист {language}",
        "area": 1,
        "period": 30
    }
    response = requests.get(
        BASE_API_HH_URL + hh_api_command,
        headers=HH_HEADERS,
        params=payload
    )
    if response.ok:
        vacancies = response.json()['found']
    return vacancies


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


def get_data(language):
    page = 0
    pages_number = 1
    whole_data = {"items": []}
    while page < pages_number:

        payload = {
            "text": f"программист {language}",
            "area": 1,
            "period": 30,
            "only_with_salary": True,
            "currency": "RUR",
            "page": page,
            "per_page": 100
        }
        response = requests.get(
            BASE_API_HH_URL + hh_api_command,
            headers=HH_HEADERS,
            params=payload
        )
        if response.ok:
            page_data = response.json()
            pages_number = page_data["pages"]
            page += 1
            whole_data["items"] += page_data["items"]
        logging.debug(f"Language: {language} Page: {page} from {pages_number}")
    return whole_data


def get_average_salary(data):
    salaries = []
    for item in data['items']:
        if item["salary"]["currency"] == "RUR":
            tax = 1
            if item["salary"]["gross"]:
                tax = 0.87
            salaries_range = item["salary"]["from"], item["salary"]["to"], tax
            salary = predict_rub_salary(salaries_range)
            if salary is not None:
                salaries.append(salary)
    avg_salary = int(mean(salaries))
    median_salary = int(median(salaries))
    return avg_salary, median_salary, len(salaries)


if __name__ == '__main__':
    pass
