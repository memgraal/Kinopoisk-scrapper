from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from typing import Dict, List
import json
from colorama import Fore, Style


# Настройка опций для Chrome
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def GET_info(html: str, url: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, 'html.parser')
    data = {}
    rows = soup.select('div.styles_rowDark__ucbcz, div.styles_rowLight__P8Y_1')

    for row in rows:
        title = row.select_one('div.styles_titleDark___tfMR, div.styles_titleLight__HIbfT')
        value = row.select_one('div.styles_valueDark__BCk93, div.styles_valueLight__nAaO3')

        if title and value:
            title_text = title.get_text(strip=True)
            if value.find_all('span'):
                value_text = ''.join([span.get_text(strip=True) for span in value.find_all('span')])
            else:
                value_text = value.get_text(strip=True)
            data[title_text] = value_text

    # Добавляем поле "url"
    data["url"] = url
    return data


driver = init_driver()

if __name__ == "__main__":
    try:
        all_data: List[Dict[str, str]] = []
        with open("hrefs.txt", mode="r", encoding="utf-8") as file:
            urls = file.readlines()

            for url in urls:
                url = url.strip()  # Удаление лишних пробелов и символов новой строки
                driver.get(url)
                
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_rowDark__ucbcz, div.styles_rowLight__P8Y_1'))
                )
                
                html = driver.page_source
                data = GET_info(html, url)
                all_data.append(data)
                print(Fore.GREEN + f"Данные с {url} извлечены и добавлены в список" + Style.RESET_ALL)

        # Запись всех данных в файл
        with open("json_film.json", mode="w", encoding="utf-8") as json_file:
            json.dump(all_data, json_file, ensure_ascii=False, indent=4)
            print(Fore.GREEN + "Все данные записаны в json_film.json" + Style.RESET_ALL)

    except Exception as e:
        print(Fore.RED + f"Произошла ошибка: {e}" + Style.RESET_ALL)

    finally:
        driver.quit()
