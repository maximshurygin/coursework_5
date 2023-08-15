import requests


class HHApi:
    def __init__(self):
        self.api_url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, keyword):
        """Получение вакансий от работодателей с помощью API HeadHunter"""
        vacancies = []
        params = {
            'area': '113',
            'text': keyword,
            'search_field': 'company_name',
            'per_page': 100,
            'page': 0,
            'only_with_vacancies': True
        }
        response = requests.get(self.api_url, params=params)
        for row in response.json()['items']:
            if row['salary'] is not None:
                vacancies.append({
                    'employer_name': row['employer']['name'],
                    'employer_url': row['employer']['url'],
                    'vacancy_name': row['name'],
                    'salary_from': row['salary']['from'],
                    'salary_to': row['salary']['to'],
                    'vacancy_url': row['alternate_url'],
                    'area': row['area']['name']
                })

        return vacancies
