from pprint import pprint
import requests
import os
from dotenv import load_dotenv
from itertools import count
from terminaltables import AsciiTable


def get_vacancies_statistics_hh(language):
    url = "https://api.hh.ru/vacancies"
    page = 0
    pages_number = 1
    salaries = []
    area_id = 1
    while page < pages_number and page < 101:
        payload = {"text": language, "area": area_id, "page": page}
        response = requests.get(url, params=payload)
        response.raise_for_status()
        response_content = response.json()
        pages_number = response_content["pages"]
        vacancies_found = response_content["found"]
        page += 1
        for vacancy in response_content["items"]:
            if vacancy["salary"]:
                salary_from = vacancy["salary"]["from"]
                salary_to = vacancy["salary"]["to"]
                currency = vacancy["salary"]["currency"]
                exp_salary = predict_rub_salary(salary_from, salary_to, currency)
                if not exp_salary:
                    continue
                salaries.append(exp_salary)
    processed_salaries = len(salaries)
    if processed_salaries:
        average_salary = sum(salaries) / len(salaries)
    else:
        processed_salaries, average_salary = (0, 0)
    return {
        "vacancies_found": vacancies_found,
        "processed_salaries": processed_salaries,
        "average_salary": average_salary
    }


def predict_rub_salary(salary_from, salary_to, currency):
    if currency != "RUR" and currency != "rub":
        return
    if salary_from and salary_to:
        expected_salary = (salary_from + salary_to) / 2
    elif salary_from and not salary_to:
        expected_salary = 1.2 * salary_from
    else:
        expected_salary = 0.8 * salary_to
    return expected_salary


def get_vacancies_statistics_sj(sj_key, language):
    salaries = []
    page_count = count(start=0, step=1)
    headers = {"X-Api-App-Id": sj_key}
    url = "https://api.superjob.ru/2.0/vacancies"
    for page in page_count:
        params = {
            "town": "Москва",
            "keyword": language,
            "page": page
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        response_content = response.json()
        vacancies_found = response_content["total"]
        page += 1
        vacancies = response_content["objects"]
        for item in vacancies:
            salary_from = item["payment_from"]
            salary_to = item["payment_to"]
            currency = item["currency"]
            exp_salary = predict_salary_statistics(salary_from, salary_to, currency)
            if exp_salary:
                salaries.append(exp_salary)
        if not response_content["more"]:
            break
    processed_salaries = len(salaries)
    if processed_salaries:
        average_salary = sum(salaries) // len(salaries)
    else:
        average_salary = 0
    return {
        "vacancies_found": vacancies_found,
        "processed_salaries": processed_salaries,
        "average_salary": average_salary
    }


def print_table(popular_langs, title):
    table_data = [
        (
            "Язык программирования",
            "Вакансий найдено",
            "Ваканский обработано",
            "Средняя зарплата"
        )
    ]
    for lang in popular_langs:
        lang_list = (
            lang,
            popular_langs[lang]["vacancies_found"],
            popular_langs[lang]["processed_salaries"],
            popular_langs[lang]["average_salary"]
        )
        table_data.append(lang_list)
    table = AsciiTable(table_data, title)
    print(table.table)


if __name__ == "__main__":

    load_dotenv()
    language_params_hh = {}
    language_params_sj = {}
    sj_key = os.getenv("SJ_KEY")


    languages = ["python", "javascript", "java"]
    for language in languages:
        language_params_hh[language] = get_vacancies_statistics_hh(language)
        language_params_sj[language] = get_vacancies_statistics_sj(sj_key, language)
    print_table(language_params_hh, "HH MOSCOW")
    print_table(language_params_sj, "SJ MOSCOW")
