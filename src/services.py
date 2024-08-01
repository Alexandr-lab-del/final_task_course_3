import os
import logging
import pandas as pd
import re
import json

"""Настройка логирования"""
logs_directory = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/logs'
log_file = os.path.join(logs_directory, 'services.log')

os.makedirs(logs_directory, exist_ok=True)

"""Настройка логгера"""
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='w'
)

logger = logging.getLogger(__name__)


def extract_transactions_with_mobile_numbers(file_path):
    """Чтение данных из Excel файла"""
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Файл {file_path} успешно прочитан.")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла {file_path}: {e}")
        return

    """Выражение для поиска мобильных номеров"""
    phone_pattern = re.compile(r'\+7\s?\(?\d{3}\)?\s?\d{3}-?\d{2}-?\d{2}')
    logger.debug("Регулярное выражение для мобильных номеров создано.")

    def contains_mobile_number(description):
        """Функция для проверки описания на наличие мобильного номера"""
        if pd.isnull(description):
            return False
        return bool(phone_pattern.search(description))

    """Фильтрация строк, где в описании есть мобильные номера"""
    try:
        df_with_numbers = df[df['Описание'].apply(contains_mobile_number)]
        logger.info("Успешно отфильтрованы строки с мобильными номерами.")
    except Exception as e:
        logger.error(f"Ошибка при фильтрации строк: {e}")
        return

    """Преобразование отфильтрованных данных в JSON"""
    try:
        transactions_list = df_with_numbers.to_dict(orient='records')
        logger.info("Успешно преобразовано в список транзакций в формате JSON.")
    except Exception as e:
        logger.error(f"Ошибка при преобразовании данных в JSON: {e}")
        return

    """Вывод каждого объекта JSON в столбец"""
    try:
        for transaction in transactions_list:
            transaction_json = json.dumps(transaction, ensure_ascii=False, indent=2)
            print(transaction_json)
            print()
        logger.info("Успешно выведены транзакции содержащие мобильные номера.")
    except Exception as e:
        logger.error(f"Ошибка при выводе транзакций: {e}")
        return


"""Пример использования функции"""
# file_path = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/data/operations.xlsx'
# extract_transactions_with_mobile_numbers(file_path)
