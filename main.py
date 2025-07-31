import time
import json
import yaml
import requests as r
from fake_useragent import UserAgent


def load_config(path="config.yaml"):
    with open(path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def login(session, ua, cfg):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": ua,
        "Referer": "https://f-ariel.ru/auth/",
        "Origin": "https://f-ariel.ru"
    }
    data = {
        "AUTH_FORM": "Y",
        "TYPE": "AUTH",
        "backurl": "/auth/",
        "USER_LOGIN": cfg["auth"]["login"],
        "USER_PASSWORD": cfg["auth"]["password"],
        "Login": "Войти"
    }

    session.post("https://f-ariel.ru/auth/?login=yes", data=data, headers=headers)
    check = session.get("https://f-ariel.ru/auth/?register=yes")
    return "Вы зарегистрированы и успешно авторизовались." in check.text


def check_products(session, ua, cfg):
    headers = {
        "Accept": "*/*",
        "Referer": "https://order.f-ariel.ru/",
        "Origin": "https://order.f-ariel.ru",
        "User-Agent": ua
    }

    while True:
        time.sleep(cfg["product_check"]["check_interval"])
        products = session.get("https://order.f-ariel.ru/api/v1/product", headers=headers).json()

        for product in products:
            if product["name"] != cfg["product_check"]["name_to_avoid"]:
                print("Найден другой товар:")
                print("ID:", product["id"])
                print("Название:", product["name"])
                return product["id"]



def make_order(session, ua, cfg, product_id):
    payload = {
        "first_name": cfg["order"]["first_name"],
        "middle_name": cfg["order"]["middle_name"],
        "phone": cfg["order"]["phone"],
        "email": cfg["order"]["email"],
        "items": [{
            "product_id": product_id,
            "quantity": cfg["order"]["quantity"]
        }],
        "comment": cfg["order"]["comment"]
    }

    headers = {
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "Content-Type": "text/plain;charset=UTF-8",
        "Origin": "https://order.f-ariel.ru",
        "Referer": "https://order.f-ariel.ru/",
        "User-Agent": ua
    }

    while True:
        response = session.post("https://order.f-ariel.ru/api/v1/buy", data=json.dumps(payload), headers=headers)
        print(response.text)
        print(response.status_code)
        if response.ok:
            print("Заявка успешно создана!")
            break
        else:
            print("Не удалось оформить заказ, повтор через 3 сек...")
            time.sleep(3)


def main():
    cfg = load_config()
    ua = UserAgent().random
    session = r.Session()

    if login(session, ua, cfg):
        print("Авторизация прошла успешно.")
        product_id = check_products(session, ua, cfg)
        if product_id:
            make_order(session, ua, cfg, product_id)
    else:
        print("Проблемы с логином.")


if __name__ == "__main__":
    main()
