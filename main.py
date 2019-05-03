import logging
import hh_utils
import sj_utils
from terminaltables import AsciiTable


logging.basicConfig(
    format='%(levelname)-8s [%(asctime)s] %(message)s',
    level=logging.DEBUG,
    filename='log.log'
)


def make_table(data, api_name):
    if api_name == "hh":
        table_title = "HeadHunter, Moscow"
    elif api_name == "sj":
        table_title = "SuperJob, Moscow"
    else:
        raise UnboundLocalError("Unknown API")
    table_header = [
        "Язык программирования", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата", "Медианная зарплата"
    ]
    table_data = [
        table_header,
    ]
    for language in data:
        table_row_template = [
            language,
            data[language]["vacancies_found"],
            data[language]["vacancies_processed"],
            data[language]["average_salary"],
            data[language]["median_salary"]
        ]
        table_data.append(table_row_template)
    table = AsciiTable(table_data, table_title)
    return table


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
    hh_data = hh_utils.get_top_languages(languages)
    sj_data = sj_utils.get_top_languages(languages)

    hh_table = make_table(hh_data, "hh")
    sj_table = make_table(sj_data, "sj")
    print(hh_table.table)
    print()
    print(sj_table.table)
