import random
import time
import requests
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Инициализация colorama
init(autoreset=True)

headers = {
    'Content-Type': 'application/json',
    'Referer': 'https://bot.dragonz.land/',
}

def log(message, color=Fore.WHITE):
    """Функция для вывода логов с текущей датой и временем и цветом"""
    print(f"{color}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")

def load_credentials():
    try:
        with open('query_id.txt', 'r') as f:
            queries = [line.strip() for line in f.readlines()]
        log(f"Загружено учетных записей: {len(queries)}", Fore.CYAN)
        return queries
    except FileNotFoundError:
        log("Файл query_id.txt не найден.", Fore.RED)
        return []
    except Exception as e:
        log(f"Ошибка при загрузке учетных данных: {str(e)}", Fore.RED)
        return []

def getuseragent(index):
    try:
        with open('useragent.txt', 'r') as f:
            useragent = [line.strip() for line in f.readlines()]
        if index < len(useragent):
            return useragent[index]
        else:
            return "Index out of range"
    except FileNotFoundError:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'
    except Exception as e:
        return 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36'

def getme(query):
    url = 'https://bot.dragonz.land/api/me'
    headers['X-Init-Data'] = query

    try:
        response = requests.get(url, headers=headers)
        if response.status_code in range(200, 211):
            return response.json()
        elif response.status_code in range(500, 530):
            log(response.text, Fore.RED)
            return None
        elif response.status_code in range(400, 410):
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        log(f'Ошибка при запросе: {e}', Fore.RED)
        return None

def feed(query, feed):
    url = 'https://bot.dragonz.land/api/me/feed'
    headers['X-Init-Data'] = query
    payload = {'feedCount': feed}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in range(200, 211):
            return "DONE"
        elif response.status_code in range(500, 530):
            log(response.text, Fore.RED)
            return None
        elif response.status_code in range(400, 410):
            return None
        else:
            raise Exception(f'Unexpected status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        log(f'Ошибка при запросе: {e}', Fore.RED)
        return None

def main():
    log("Бот стартовал", Fore.GREEN)
    while True:
        queries = load_credentials()
        for index, query in enumerate(queries):
            useragent = getuseragent(index)
            headers['User-Agent'] = useragent
            log(f"========= Обработка учетной записи {index+1} =========", Fore.YELLOW)

            pause = random.uniform(5, 15)
            log(f"Пауза перед следующим запросом: {pause:.2f} секунд", Fore.BLUE)
            time.sleep(pause)

            data_getme = getme(query)
            if data_getme is not None:
                first_name = data_getme.get('firstName')
                last_name = data_getme.get('lastName')
                energy = data_getme.get('energy')
                log(f"Имя: {first_name} {last_name} | Энергия: {energy}", Fore.CYAN)

                while energy > 10:
                    pause = random.uniform(5, 10)
                    log(f"Пауза перед кормлением: {pause:.2f} секунд", Fore.BLUE)
                    time.sleep(pause)

                    feeds = random.randint(50, 150)
                    if energy < feeds:
                        feeds = energy

                    data_feed = feed(query, feeds)
                    if data_feed is not None:
                        energy -= feeds
                        log(f"Кормление: {feeds} кликов отправлено, осталось энергии: {energy}", Fore.GREEN)
                    else:
                        log('Ошибка при кормлении', Fore.RED)
                        break
            else:
                log('Ошибка получения данных', Fore.RED)

        next_cycle_time = datetime.now() + timedelta(minutes=30)
        log(f"Все аккаунты обработаны. Следующий цикл начнется в {next_cycle_time.strftime('%Y-%m-%d %H:%M:%S')}", Fore.MAGENTA)
        time.sleep(30 * 60)  # Ожидание 30 минут перед повторным запуском

main()
