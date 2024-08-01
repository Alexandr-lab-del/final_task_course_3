import json
import logging
import pandas as pd
from datetime import datetime

logger = logging.getLogger(__name__)


def load_user_settings(file_path='C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/user_settings.json'):
    """Функция загрузки пользовательских настроек"""
    try:
        with open(file_path, 'r') as file:
            settings = json.load(file)
            logger.info(f'Настройки загружены из {file_path}')
            return settings
    except Exception as e:
        logger.error(f'Ошибка при загрузке настроек из {file_path}: {e}')
        return {}


def convert_timestamps(obj):
    """Функция для конвертации даты"""
    if isinstance(obj, dict):
        return {k: convert_timestamps(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_timestamps(i) for i in obj]
    elif isinstance(obj, (datetime, pd.Timestamp)):
        return obj.isoformat()
    return obj


def load_transactions(file_path):
    """Функция чтения транзакций"""
    try:
        transactions = pd.read_excel(file_path)
        return transactions
    except Exception as e:
        logger.error(f"Ошибка чтения транзакций из {file_path}: {e}")
        return pd.DataFrame()
