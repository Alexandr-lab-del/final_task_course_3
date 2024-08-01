import logging
import os
import pandas as pd
from src.services import extract_transactions_with_mobile_numbers
from src.reports import spending_by_category, spending_by_category_custom
from src.views import main

if __name__ == "__main__":
    """Настройка логирования"""
    logs_directory = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/logs'
    log_file = os.path.join(logs_directory, 'main.log')

    os.makedirs(logs_directory, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=log_file,
        filemode='w'
    )

    logger = logging.getLogger(__name__)

    logger.info('Запуск основного скрипта')

    file_path = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/data/operations.xlsx'

    """Пример использования функции из services.py"""
    logger.info('Запуск функции extract_transactions_with_mobile_numbers')
    try:
        extract_transactions_with_mobile_numbers(file_path)
        logger.info('Функция extract_transactions_with_mobile_numbers выполнена успешно')
    except Exception as e:
        logger.error(f'Ошибка при выполнении функции extract_transactions_with_mobile_numbers: {e}')

    """Загрузка данных для report функций"""
    logger.info(f'Загрузка данных из файла {file_path}')
    try:
        df = pd.read_excel(file_path)
        logger.info(f'Данные успешно загружены, количество записей: {len(df)}')
    except Exception as e:
        logger.error(f'Ошибка при загрузке данных из файла {file_path}: {e}')
        raise

    """Пример стандарного вызова функции из reports.py"""
    logger.info('Вызов функции spending_by_category')
    try:
        report = spending_by_category(df, 'Супермаркеты', '2021-12-31')
        logger.info('Функция spending_by_category выполнена успешно')
    except Exception as e:
        logger.error(f'Ошибка при вызове функции spending_by_category: {e}')

    """Пример вызова функции с дополнительным параметром из reports.py"""
    logger.info('Вызов функции spending_by_category_custom')
    try:
        report_custom = spending_by_category_custom(df, 'Дом и ремонт', '2020-12-31')
        logger.info('Функция spending_by_category_custom выполнена успешно')
    except Exception as e:
        logger.error(f'Ошибка при вызове функции spending_by_category_custom: {e}')

    datetime_str = "2018-07-20 15:30:45"
    result = main(datetime_str)
    print(result)
