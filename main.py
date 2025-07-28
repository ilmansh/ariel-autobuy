import requests as r
from fake_useragent import UserAgent


ua = UserAgent().random #UserAgent(browsers="Chrome", os="Windows",platforms="desktop")
session = r.Session()

login_headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": ua,
    "Referer": "https://f-ariel.ru/auth/",
    "Origin": "https://f-ariel.ru"
}

login_data = {
    "AUTH_FORM": "Y",
    "TYPE": "AUTH",
    "backurl": "/auth/",
    "USER_LOGIN": "dmsch",
    "USER_PASSWORD": "dmsch1",
    "Login": "Войти"
}

session.post("https://f-ariel.ru/auth/?login=yes", data=login_data, headers=login_headers)
login_check = session.get("https://f-ariel.ru/auth/?register=yes")

if "Вы зарегистрированы и успешно авторизовались." in login_check.text:
    print("Успешная авторизация!")
    # допилить прочек новых лотов через бесконечный цикл
    headers = {
        "Accept": "*/*",
        "Referer": "https://order.f-ariel.ru/",
        "Origin": "https://order.f-ariel.ru",
        "User-Agent": ua
    }

    products = session.get("https://order.f-ariel.ru/api/v1/product")
    print(products.json())
else:
    print("Проблемы с логином...")






# Покупка
# buy_payload = {
#     "first_name": "Маркарян",
#     "middle_name": "Алексей",
#     "phone": "71119998833",
#     "email": "acaz@gmail.com",
#     "items": [
#         {
#             "product_id": 1,
#             "quantity": 1
#         }
#     ],
#     "comment": "Самовывоз" # адрес куда
# }
# headers = {
#     "Accept": "*/*",
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     "Content-Type": "text/plain;charset=UTF-8",
#     "Origin": "https://order.f-ariel.ru",
#     "Referer": "https://order.f-ariel.ru/",
#     "User-Agent": ua,
# }
#
#
# buy_request = session.post("https://example.com/api/order", json=buy_payload)