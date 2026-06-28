#!/data/data/com.termux/files/usr/bin/env python


import requests
import time
import random
from datetime import datetime

# URL ИЗМЕНЁН!
URL = "https://speedtest.ru/api/exam_result"

# Заголовки (обязательны)
HEADERS = {
    "x-api-key": "b8a4ecb62a2cc6bb375e01c9482c996d",
    "origin": "https://epd.qms.ru",
    "referer": "https://epd.qms.ru/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "connection": "keep-alive"
}

# Доступные тарифы
TARIFFS = [40, 60, 100, 130, 200, 300, 400, 500]

# Шаблон данных - УДАЛЕН attr_2, ИЗМЕНЕН attr_4
TEMPLATE_DATA = {
    "download": None,
    "upload": None,
    "ping": None,
    "jitter": None,
    "ping_download": None,
    "ping_upload": None,
    "finger_hash": "5bcf1c243042e72317f2b58a919bd299",
    "server_id": 47,
    "city": "Улан-Удэ",
    "requester": "user",
    "lat": 51.8334492,
    "lng": 107.584068,
    "region_id": 24,
    "exam_type": 1,
    "vpn_flag": 0,
    "ya_user": "1775491083143397116",
    "rtk_nls": None,
    # "attr_2": "cookie_accept",  # <-- УДАЛЕНО
    "attr_3": "multi",
    "attr_4": "2.7.4",          # <-- ИЗМЕНЕНО
    "country": "Россия",
    "timezone": "Asia/Irkutsk",
    "network_type": "wi-fi",
    "device_type": "n/a",
    "trait": "service"
}

def randomize_speed(tariff_speed: float, down_percent: float = 8, up_percent: float = 15) -> float:
    """
    Рандомизирует скорость в пределах от -down_percent% до +up_percent% от тарифа
    """
    min_speed = tariff_speed * (1 - down_percent / 100)
    max_speed = tariff_speed * (1 + up_percent / 100)

    randomized = round(random.uniform(min_speed, max_speed), 2)

    # Страховка от слишком низких значений
    if randomized < tariff_speed * 0.85:
        randomized = round(tariff_speed * random.uniform(0.85, 0.88), 2)

    return randomized

def manual_input():
    """Ручной ввод всех параметров"""
    print("\n✏️ РУЧНОЙ РЕЖИМ:")
    print("-" * 40)

    download = float(input("📥 Download (Мбит/с): ").strip())
    upload = float(input("📤 Upload (Мбит/с): ").strip())
    ping = int(input("📡 Ping (мс): ").strip())
    jitter = int(input("⚡ Jitter (мс): ").strip())
    ping_download = int(input("📥 Ping Download (мс): ").strip())
    ping_upload = int(input("📤 Ping Upload (мс): ").strip())

    return {
        "download": download,
        "upload": upload,
        "ping": ping,
        "jitter": jitter,
        "ping_download": ping_download,
        "ping_upload": ping_upload
    }

def calculate_upload(download_speed: float) -> float:
    """Реалистичный расчёт скорости отдачи"""
    return round(download_speed * random.uniform(0.85, 0.95), 2)

def generate_realistic_values(download_speed: float, mode: str = "auto"):
    """Генерирует реалистичные значения для ping, jitter и т.д."""
    if mode == "auto":
        if download_speed >= 500:
            ping = 2
            jitter = 1
            ping_download = 2
            ping_upload = random.randint(18, 25)
        elif download_speed >= 400:
            ping = 3
            jitter = 1
            ping_download = 2
            ping_upload = random.randint(20, 28)
        elif download_speed >= 300:
            ping = 4
            jitter = 1
            ping_download = 2
            ping_upload = random.randint(22, 30)
        elif download_speed >= 200:
            ping = 5
            jitter = 2
            ping_download = 3
            ping_upload = random.randint(25, 35)
        elif download_speed >= 130:
            ping = 6
            jitter = 2
            ping_download = 3
            ping_upload = random.randint(28, 38)
        elif download_speed >= 100:
            ping = 8
            jitter = 2
            ping_download = 4
            ping_upload = random.randint(30, 40)
        elif download_speed >= 60:
            ping = 10
            jitter = 3
            ping_download = 5
            ping_upload = random.randint(35, 45)
        else:
            ping = 12
            jitter = 3
            ping_download = 5
            ping_upload = random.randint(40, 50)
        return ping, jitter, ping_download, ping_upload

    elif mode == "random":
        ping = random.randint(2, 15)
        jitter = random.randint(1, 5)
        ping_download = random.randint(2, 10)
        ping_upload = random.randint(18, 50)
        return ping, jitter, ping_download, ping_upload

    elif mode == "static":
        return 4, 1, 2, 21

    else:
        return 4, 1, 2, 21

def select_tariff():
    """Интерактивный выбор тарифа с отображением нового диапазона"""
    print("\n📡 Доступные тарифы (диапазон -8% / +15%):")
    print("-" * 50)

    row1 = TARIFFS[:4]
    row2 = TARIFFS[4:]

    for tariff in row1:
        min_speed = tariff * 0.92  # -8%
        max_speed = tariff * 1.15  # +15%
        print(f"   {tariff} Мбит/с  →  {min_speed:.1f} - {max_speed:.1f} Мбит/с")

    for tariff in row2:
        min_speed = tariff * 0.92
        max_speed = tariff * 1.15
        print(f"   {tariff} Мбит/с  →  {min_speed:.1f} - {max_speed:.1f} Мбит/с")

    print("-" * 50)

    while True:
        try:
            choice = int(input("\n🔢 Выберите тариф: ").strip())
            if choice in TARIFFS:
                return choice
            else:
                print(f"❌ Доступны: {', '.join(map(str, TARIFFS))}")
        except ValueError:
            print("❌ Введите число!")

def send_fake_result(account: str, data_params: dict, tariff_speed: float = None):
    """Отправляет результат на сервер"""

    data = TEMPLATE_DATA.copy()
    data["rtk_nls"] = account
    data["download"] = data_params["download"]
    data["upload"] = data_params["upload"]
    data["ping"] = data_params["ping"]
    data["jitter"] = data_params["jitter"]
    data["ping_download"] = data_params["ping_download"]
    data["ping_upload"] = data_params["ping_upload"]

    print(f"\n📤 Отправка результата:")
    print(f"   Счёт: {account}")
    if tariff_speed:
        print(f"   Тариф: {tariff_speed} Мбит/с")
    print(f"   Download: {data['download']} Мбит/с")
    print(f"   Upload: {data['upload']} Мбит/с")
    print(f"   Ping: {data['ping']} мс")
    print(f"   Jitter: {data['jitter']} мс")
    print(f"   Ping Download: {data['ping_download']} мс")
    print(f"   Ping Upload: {data['ping_upload']} мс")

    try:
        response = requests.post(URL, headers=HEADERS, data=data, timeout=30)

        print(f"\n📡 Ответ сервера:")
        print(f"   Статус: {response.status_code}")
        print(f"   Тело: {response.text[:200] if response.text else 'пусто'}")

        if response.status_code == 201:
            print("\n✅ УСПЕХ! Результат принят сервером.")
            return True
        else:
            print(f"\n❌ ОШИБКА: Статус {response.status_code}")
            return False

    except Exception as e:
        print(f"\n❌ ИСКЛЮЧЕНИЕ: {e}")
        return False


# ============================================================
# ИСПОЛЬЗОВАНИЕ
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 ПОДМЕНА РЕЗУЛЬТАТОВ EPD.QMS")
    print("=" * 50)

    account = input("\n🔢 Введите лицевой счёт: ").strip()

    print("\n🎮 Выберите режим:")
    print("   1. Авто (выбор тарифа, рандом -8%/+15%)")
    print("   2. Ручной (сам выбираю скорость и параметры)")
    print("   3. Комбинированный (тариф + ручной ввод параметров)")

    mode_choice = input("\nВаш выбор (1-3): ").strip()

    if mode_choice == "1":
        tariff = select_tariff()
        randomized_speed = randomize_speed(tariff, down_percent=8, up_percent=15)

        print(f"\n🎲 Рандомизация (-8% / +15%):")
        print(f"   Тариф: {tariff} Мбит/с → {randomized_speed} Мбит/с")
        print(f"   Диапазон: {tariff*0.92:.1f} - {tariff*1.15:.1f} Мбит/с")

        print("\n🎮 Режим генерации ping/jitter:")
        print("   1. Авто (под скорость)")
        print("   2. Случайные")
        print("   3. Статические (4,1,2,21)")

        sub_choice = input("Выбор (1-3, умолч. 1): ").strip() or "1"
        sub_modes = {"1": "auto", "2": "random", "3": "static"}
        sub_mode = sub_modes.get(sub_choice, "auto")

        ping, jitter, ping_download, ping_upload = generate_realistic_values(randomized_speed, sub_mode)
        upload = calculate_upload(randomized_speed)

        data_params = {
            "download": randomized_speed,
            "upload": upload,
            "ping": ping,
            "jitter": jitter,
            "ping_download": ping_download,
            "ping_upload": ping_upload
        }

        send_fake_result(account, data_params, tariff)

    elif mode_choice == "2":
        data_params = manual_input()
        send_fake_result(account, data_params)

    elif mode_choice == "3":
        tariff = select_tariff()
        randomized_speed = randomize_speed(tariff, down_percent=8, up_percent=15)

        print(f"\n🎲 Рандомизация (-8% / +15%):")
        print(f"   Тариф: {tariff} Мбит/с → {randomized_speed} Мбит/с")
        print(f"   Диапазон: {tariff*0.92:.1f} - {tariff*1.15:.1f} Мбит/с")

        print("\n✏️ РУЧНОЙ ВВОД ОСТАЛЬНЫХ ПАРАМЕТРОВ:")
        print("-" * 40)
        upload = float(input("📤 Upload (Мбит/с): ").strip())
        ping = int(input("📡 Ping (мс): ").strip())
        jitter = int(input("⚡ Jitter (мс): ").strip())
        ping_download = int(input("📥 Ping Download (мс): ").strip())
        ping_upload = int(input("📤 Ping Upload (мс): ").strip())

        data_params = {
            "download": randomized_speed,
            "upload": upload,
            "ping": ping,
            "jitter": jitter,
            "ping_download": ping_download,
            "ping_upload": ping_upload
        }

        send_fake_result(account, data_params, tariff)

    else:
        print("❌ Неверный выбор!")

    print("\n" + "=" * 50)
    input("\nНажмите Enter для выхода...")
