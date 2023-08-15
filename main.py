from src.hh_api import HHApi
from src.db_manager import DBManager


def main():
    """
    Взаимодействие с пользователем
    """
    selected_employers = ['рсхб', 'сбер', 'мтс', 'мгтс', 'ростелеком', 'softline', 'айтек', 'озон', 'тинькофф']
    hh = HHApi()
    res = []
    for employer in selected_employers:
        hh_data = hh.get_vacancies(employer)
        res.extend(hh_data)
    db_manager = DBManager()
    db_manager.create_database('headhunter')
    db_manager.save_data_to_database(res)

    print('\nПредоставляю подсчет вакансий у работодателей:')
    for vacancy in db_manager.get_companies_and_vacancies_count():
        print(*vacancy)

    print('\nПредоставляю информацию по найденным вакансиям:')

    for vacancy in db_manager.get_all_vacancies():
        print(*vacancy)

    user_choice_1 = int(input('\nХотите посмотреть вакансии с з/п выше средней? 1-Да, 2-Нет\n'))
    if user_choice_1 == 1:
        for vacancy in db_manager.get_vacancies_with_higher_salary():
            print(*vacancy)
    else:
        print('Хорошо. Продолжаю работу')

    user_choice_2 = int(input('\nХотите осуществить поиск вакансий по ключевому слову? 1-Да, 2-Нет\n'))
    if user_choice_2 == 1:
        key_word = input('Введите ключевое слово для поиска:\n')
        for vacancy in db_manager.get_vacancies_with_keyword(key_word):
            print(*vacancy)
        print('\nРабота завершена')
    else:
        print('Работа завершена')


if __name__ == '__main__':
    main()
