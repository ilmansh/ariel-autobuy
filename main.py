import requests as r
from fake_useragent import UserAgent

ua = UserAgent(browsers="Chrome", os="Windows",platforms="desktop")
session = r.Session()

# дохуярить логин
login_payload = {"username": "test", "password": "1234"}
session.post("", json=login_payload)




# дохуярить парсер товаров
products = r.get("https://order.f-ariel.ru/api/v1/product")
print(products.json())




buy_payload = {
    "first_name": "Маркарян",
    "middle_name": "Алексей",
    "phone": "71119998833",
    "email": "acaz@gmail.com",
    "items": [
        {
            "product_id": 1,
            "quantity": 1
        }
    ],
    "comment": "Самовывоз" # адрес куда
}
headers = {
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Content-Type": "text/plain;charset=UTF-8",
    "Origin": "https://order.f-ariel.ru",
    "Referer": "https://order.f-ariel.ru/",
    "User-Agent": ua,
}


buy_request = session.post("https://example.com/api/order", json=buy_payload)