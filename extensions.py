import requests
import json
from config import CURRENCY_DICT


class APIException(Exception):
    """Неверный ввод одного из аргументов"""


class Exchange:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base.lower()
        quote.lower()

        # Проверка на ошибки при вводе пользователя
        if amount == "0":
            raise APIException(f"Сюрприз, {amount} {base} равно нулю в любой валюте")
        if base == quote:
            raise APIException("Вы ввели одинаковые валюты")
        if base not in CURRENCY_DICT.keys():
            raise APIException(f"Я не знаком с такой валютой как {base}")
        if quote not in CURRENCY_DICT.keys():
            raise APIException(f"Я не знаком с такой валютой как {quote}")
        try:
            amount_num = float(amount)
        except ValueError:
            raise APIException(f"Третье значение должно быть цифрой, а не {amount}")

        # Формирование запроса через api.apilayer.com
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=" \
              f"{CURRENCY_DICT[quote]}&from={CURRENCY_DICT[base]}&amount={amount_num}"

        headers = {
          "apikey": "2OQ9dEWeIfhHhx8PP2KV07argHYIKjGd"
        }

        response = requests.request("GET", url, headers=headers)
        result = json.loads(response.text)

        if result["success"]:
            return result["result"]
        else:
            raise APIException("Странно, не могу подсоединится к денежным серверам")
