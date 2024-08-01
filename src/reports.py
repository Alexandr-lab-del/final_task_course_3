import pandas as pd
import datetime
import os
import logging
from typing import Optional, Callable
from functools import wraps

"""Настройка логирования"""
logs_directory = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/logs'
log_file = os.path.join(logs_directory, 'reports.log')

os.makedirs(logs_directory, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='w'
)

logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None) -> Callable:
    """Функция декоратора для сохранения отчета в файле"""
    default_filename = 'reports'

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            logger.debug(f'Вызвана функция {func.__name__} с аргументами {args} и {kwargs}')
            try:
                result = func(*args, **kwargs)
                output_filename = filename if filename else default_filename
                output_file = os.path.join(logs_directory, output_filename)

                if not os.path.exists(logs_directory):
                    os.makedirs(logs_directory)

                result.to_csv(output_file, index=False)
                logger.info(f'Результаты сохранены в файл {output_file}')
                return result
            except Exception as e:
                logger.error(f'Ошибка при выполнении функции {func.__name__}: {e}')
                raise

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция для вывода транзакций по категориям"""
    logger.info(f'Обработка транзакций по категории {category} и дате {date}')
    if date is None:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = pd.to_datetime(date, format='%Y-%m-%d')
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    filtered_transactions = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category)
    ]

    logger.debug(f'Найдено {len(filtered_transactions)} транзакций по категории {category}')
    return filtered_transactions


@save_report('custom_report')
def spending_by_category_custom(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция для вывода транзакций по категориям"""
    logger.info(f'Обработка транзакций по категории {category} и дате {date} с кастомным отчетом')
    if date is None:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
    end_date = pd.to_datetime(date, format='%Y-%m-%d')
    start_date = end_date - pd.DateOffset(months=3)

    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    filtered_transactions = transactions[
        (transactions['Дата операции'] >= start_date) &
        (transactions['Дата операции'] <= end_date) &
        (transactions['Категория'] == category)
    ]

    logger.debug(f'Найдено {len(filtered_transactions)} транзакций по категории {category}')
    return filtered_transactions


# file_path = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/data/operations.xlsx'
#
#
# def main():
#     # Загрузка данных для report функций
#     logger.info(f'Загрузка данных из файла {file_path}')
#     try:
#         df = pd.read_excel(file_path)
#         logger.info(f'Данные успешно загружены, количество записей: {len(df)}')
#     except Exception as e:
#         logger.error(f'Ошибка при загрузке данных из файла {file_path}: {e}')
#         raise
#
#     # Пример стандартного вызова функции из reports.py
#     logger.info('Вызов функции spending_by_category')
#     try:
#         report = spending_by_category(df, 'Супермаркеты', '2021-12-31')
#         logger.info('Функция spending_by_category выполнена успешно')
#     except Exception as e:
#         logger.error(f'Ошибка при вызове функции spending_by_category: {e}')
#
#     # Пример вызова функции с дополнительным параметром из reports.py (если такая функция существует)
#     logger.info('Вызов функции spending_by_category_custom')
#     try:
#         report_custom = spending_by_category(df, 'Дом и ремонт', '2020-12-31')
#         logger.info('Функция spending_by_category выполнена успешно')
#     except Exception as e:
#         logger.error(f'Ошибка при вызове функции spending_by_category: {e}')
#
#
# if __name__ == "__main__":
#     main()
