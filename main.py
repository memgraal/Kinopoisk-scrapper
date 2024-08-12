from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium_stealth import stealth
import time
from typing import List
from bs4 import BeautifulSoup

class Setting:
    def __init__(self) -> None:
        super().__init__()

        self.options = Options()
        self.options.add_argument("user-data-dir=C:\\Temp\\Chrome")  # Временная директория для кэша
        self.options.add_argument("--headless")  # Включить headless-режим для отладки
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-software-rasterizer")
        self.chrome_options.add_argument("--blink-settings=imagesEnabled=false")

        self.service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        
        stealth(self.driver, platform="Win32")

    def wait_for_element(self, by: By, value: str, timeout: int = 30):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def scroll_and_wait(self, delay: int = 2):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)





class Main(Setting):
    def __init__(self, PAGEcounter: int = 2672 ) -> None: # PAGEcounter - переменная, которая говорит нам о том, какую странице сейчас обрабатывает код
        super().__init__()
        self.PAGEcounter = PAGEcounter  # Make PAGEcounter an instance variable

    def GetPageCode(self) -> str:
        url = f"https://www.kinopoisk.ru/lists/movies/?page={self.PAGEcounter}"
        self.driver.get(url)

        # Ожидание загрузки страницы и скролл
        self.wait_for_element(By.CSS_SELECTOR, 'body')
        self.scroll_and_wait()
        
        self.PAGEcounter += 1  # Increment the PAGEcounter after processing the current page
        return self.driver.page_source

    def GetLinkToFilm(self, PAGEsource: str) -> List[str]:
        soup = BeautifulSoup(PAGEsource, 'html.parser')
        films_mini_info = soup.select('div.styles_root__ti07r a.styles_root__wgbNq')
        hrefs = []
        for info in films_mini_info:
            href_to_film_page = info['href']
            hrefs.append("https://www.kinopoisk.ru" + href_to_film_page)
        
        # Запись в файл после завершения сбора ссылок
        with open("hrefs.txt", "a") as file:  # Use "a" to append to the file
            for href in hrefs:
                file.write(href + "\n")
        
        return hrefs

# Create a single instance of Main and use it throughout the loop
# mn = Main()

# for _ in range(2672 , 19009):  # or range(1, 19010) to include the last page | ПОМЕНЯТЬ
#     page_code = mn.GetPageCode()
#     links = mn.GetLinkToFilm(page_code)
#     print(links)  # Печать собранных ссылок

    # НЕ ЗАПУСКАТЬ КОД, НЕ ПОМЕНЯВ, ТАК КАК ПОСЛЕДНЯЯ ССЫЛКА, КОТОРАЯ БЫЛА ОТКРЫТА - | НОМЕР СТРАНЦЫ -  