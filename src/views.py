import os
import requests
import logging
import pandas as pd
from dateutil.parser import parse
from dotenv import load_dotenv
from src.utils import load_user_settings, convert_timestamps
import json

"""Настройка логирования"""
logs_directory = 'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/logs'
log_file = os.path.join(logs_directory, 'views.log')

os.makedirs(logs_directory, exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=log_file,
    filemode='w'
)

logger = logging.getLogger(__name__)

"""Загрузка переменных окружения"""
load_dotenv()

"""Получение API ключей из .env файла"""
API_KEY = os.getenv("API_KEY")
API_KEY_STOCK = os.getenv("API_KEY_STOCK")

"""Дефолтные значения цен на акции"""
default_stock_prices = {
    "AAPL": 150.12,
    "AMZN": 3173.18,
    "GOOGL": 2742.39,
    "MSFT": 296.71,
    "TSLA": 1007.08
}


def fetch_stock_price(stock_symbol):
    """Функция для записи логов при получении цены акции"""
    try:
        price = default_stock_prices.get(stock_symbol, None)
        if price is not None:
            logger.info(f'Цена акций для {stock_symbol}: {price}')
        else:
            logger.warning(f'Цена для {stock_symbol} не найдена.')
        return price
    except Exception as e:
        logger.error(f'Ошибка при получении цены акции для {stock_symbol}: {e}')
        return None


def get_greeting(dt):
    """Функция получения приветствия в зависимости от времени суток"""
    hour = dt.hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_currency_rates(currencies):
    """Функция получения курсов валют"""
    if not API_KEY:
        logger.warning("API_KEY не установлен. Проверьте файл .env.")
        return [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08}
        ]

    symbols = ",".join(currencies)
    url = f"https://api.apilayer.com/currency_data/live?symbols={symbols}"
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info("Курсы валют получены успешно.")
    except requests.RequestException as e:
        logger.error(f"Ошибка в обращении к сайту: {e}")
        return [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08}
        ]

    try:
        data = response.json()
        logger.debug(f'Полученные данные о курсах валют: {data}')
    except ValueError as e:
        logger.error(f"Ошибка в преобразовании ответа в JSON: {e}")
        return [
            {"currency": "USD", "rate": 73.21},
            {"currency": "EUR", "rate": 87.08}
        ]

    quotes = data.get("quotes", {})
    rates = [{"currency": currency, "rate": round(quotes.get(f"USD{currency}", 0), 2)} for currency in currencies]
    logger.info("Курсы валют успешно обработаны.")
    return rates


def get_stock_price(stocks):
    """Функция получения цен на акции"""
    if not API_KEY_STOCK:
        logger.warning("API_KEY_STOCK не установлен. Проверьте файл .env.")
        return [
            {"stock": "AAPL", "price": 150.12},
            {"stock": "AMZN", "price": 3173.18},
            {"stock": "GOOGL", "price": 2742.39},
            {"stock": "MSFT", "price": 296.71},
            {"stock": "TSLA", "price": 1007.08}
        ]

    stock_prices = []

    for s in stocks:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={s}&apikey={API_KEY_STOCK}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Цены на акции для {s} получены успешно.")
        except requests.RequestException as e:
            logger.error(f"Запрос не был успешным для {s}: {e}")
            stock_prices.append({"stock": s, "price": default_stock_prices.get(s, 0.0)})
            continue

        try:
            data = response.json()
            logger.debug(f'Полученные данные о цене акций для {s}: {data}')
        except ValueError as e:
            logger.error(f"Ошибка в преобразовании ответа в JSON для {s}: {e}")
            stock_prices.append({"stock": s, "price": default_stock_prices.get(s, 0.0)})
            continue

        stock_data = data.get("Global Quote", {})
        price = round(float(stock_data.get("05. price", 0)), 2)

        if price == 0.0:
            price = default_stock_prices.get(s, 0.0)

        stock_prices.append({"stock": s, "price": price})

    if not stock_prices:
        logger.warning("Получен пустой список акций. Возвращаем дефолтные значения.")
        stock_prices = default_stock_prices

    logger.info("Цены на акции успешно обработаны.")
    return stock_prices


def analyze_cards(file_path, start_date, end_date):
    """Функция для анализа данных карт из operations.xlsx"""
    try:
        df = pd.read_excel(file_path)
        logger.info(f'Файл {file_path} успешно прочитан.')
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return [], []
    except Exception as e:
        logger.error(f"Ошибка чтения файла {file_path}: {e}")
        return [], []

    try:
        """Обновление формата даты и времени"""
        df['Дата операции'] = pd.to_datetime(df['Дата операции'], format='%d.%m.%Y %H:%M:%S')
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        filtered_df = df[(df['Дата операции'] >= start_date) & (df['Дата операции'] <= end_date)]
    except Exception as e:
        logger.error(f"Ошибка обработки данных из {file_path}: {e}")
        return [], []

    card_summary = filtered_df.groupby('Номер карты')['Сумма операции'].sum().reset_index()
    card_summary['Кэшбэк'] = round(card_summary['Сумма операции'] * 0.01, 2)
    card_summary['Последние цифры'] = card_summary['Номер карты'].apply(lambda x: str(x)[-4:] if pd.notna(x) else '')

    transactions = filtered_df.nlargest(5, 'Сумма операции')[['Дата операции', 'Сумма операции', 'Категория',
                                                              'Описание']].to_dict(orient='records')

    card_info = [{"Последние цифры": str(row['Последние цифры']),
                  "Всего потрачено": round(row['Сумма операции'], 2),
                  "Кэшбэк": round(row['Кэшбэк'], 2)} for index, row in card_summary.iterrows()]

    logger.info("Транзакции успешно проанализированы.")
    return card_info, transactions


def main(datetime_str):
    """Главная функция"""
    dt = parse(datetime_str)
    start_date = dt.replace(day=1)
    end_date = dt

    logger.info(f"Программа запущена с datetime_str: {datetime_str}")

    settings = load_user_settings()
    greeting = get_greeting(dt)
    card_info, top_transactions = analyze_cards(
        'C:/Users/Александр Побережный/Desktop/питон/final_task_course_3/data/operations.xlsx', start_date, end_date)
    currency_rates = get_currency_rates(settings.get('user_currencies', []))
    stock_prices = get_stock_price(settings.get('user_stocks', []))

    result = {
        "greeting": greeting,
        "cards": card_info,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
        "start_date": start_date,
        "end_date": end_date
    }

    result = convert_timestamps(result)

    logger.info("Результаты успешно сформированы.")
    logger.debug(f'Результаты: {result}')

    return json.dumps(result, ensure_ascii=False, indent=4)


"""Пример как вызывать функцию"""
if __name__ == "__main__":
    datetime_str = "2018-07-20 15:30:45"
    result = main(datetime_str)
    logger.info("Программа успешно завершена.")
    print(result)
