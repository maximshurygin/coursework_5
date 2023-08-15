from config import config
import psycopg2


class DBManager:
    """
    Класс для взаимодействия с базой данных и таблицами
    """

    def __init__(self):
        self.params = config()

    def create_database(self, database_name):
        """
        Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях
        """
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        # Удаление базы данных, если она существует
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")

        # Создание базы данных
        cur.execute(f"CREATE DATABASE {database_name}")

        # Закрытие текущего соединения и переподключение
        conn.close()
        conn = psycopg2.connect(dbname=database_name, **self.params)

        query_1 = '''
            CREATE TABLE IF NOT EXISTS employers (
            employer_id SERIAL PRIMARY KEY,
            employer_name VARCHAR(100)
            )
        '''
        query_2 = '''
            CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            vacancy_name VARCHAR(100),
            salary_from INTEGER,
            vacancy_url VARCHAR(200),
            employer_id SERIAL REFERENCES employers (employer_id)
            )
        '''

        for query in [query_1, query_2]:
            with conn.cursor() as cur:
                cur.execute(query)
                conn.commit()

        conn.close()

    def save_data_to_database(self, data):
        """
        Сохранение данных о работодателях и вакансиях в базу данных
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)
        with conn.cursor() as cur:
            for line in data:
                cur.execute(
                    '''
                    INSERT INTO employers (employer_name)
                    VALUES (%s)
                    ''',
                    (line['employer_name'],)
                )

            for line in data:
                cur.execute(
                    '''
                    INSERT INTO vacancies (vacancy_name, salary_from, vacancy_url)
                    VALUES (%s, %s, %s)
                    ''',
                    (line['vacancy_name'], line['salary_from'], line['vacancy_url'])
                )

        conn.commit()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)

        with conn.cursor() as cur:
            cur.execute('''
                SELECT employers.employer_name, COUNT(vacancies.vacancy_id) AS vacancy_count
                FROM employers
                LEFT JOIN vacancies ON (employers.employer_id=vacancies.employer_id)
                GROUP BY employers.employer_name
                ORDER BY employers.employer_name
            ''')
            result = cur.fetchall()
        return result

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию.
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)

        with conn.cursor() as cur:
            cur.execute('''
                SELECT employers.employer_name, vacancies.vacancy_name, vacancies.salary_from, vacancies.vacancy_url
                FROM employers
                INNER JOIN vacancies ON (employers.employer_id=vacancies.employer_id)
                ORDER BY employers.employer_name, vacancies.vacancy_name
            ''')
            result = cur.fetchall()
        return result

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)
        with conn.cursor() as cur:
            cur.execute('''
                SELECT AVG(salary_from)
                FROM vacancies
            ''')
            average_salary = cur.fetchone()[0]
        return average_salary

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)
        average_salary = self.get_avg_salary()
        with conn.cursor() as cur:
            cur.execute(f'''
                SELECT vacancy_name, salary_from, vacancy_url
                FROM vacancies
                WHERE salary_from > {average_salary}
            ''')
            result = cur.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """
        получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
        """
        conn = psycopg2.connect(dbname='headhunter', **self.params)
        with conn.cursor() as cur:
            query = '''
                SELECT vacancy_name, salary_from, vacancy_url FROM vacancies
                WHERE vacancy_name LIKE %s
            '''
            cur.execute(query, (f"%{keyword}%",))
            result = cur.fetchall()
        conn.close()
        return result
