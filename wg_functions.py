from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
import requests
from bs4 import BeautifulSoup as soup
import time

def get_date(day):
    today = date.today()
    go_to = timedelta(days=day)
    the_date = today + go_to
    return the_date  

def past_weather(location, station):
    historical = {}
    for idx, stn in enumerate(station):  
        url = f'https://www.wunderground.com/dashboard/pws/{stn}/graph/{get_date(-1)}/{get_date(-1)}/daily'
        page = requests.get(url).text
        scoop = soup(page, 'html.parser')
        hi_low = scoop.find_all('span', class_='wu-value wu-value-to')
        ls = [f.get_text() for f in hi_low]
        historical.update({location[idx] : ls[18:20]})
        time.sleep(5)
    return historical

def forecast(area, station, web_driver):
    weather_dict = {}
    driver = webdriver.Firefox(executable_path=web_driver)
    try:
        for idx, stn in enumerate(station):
            record_high = []
            record_low = []
            time.sleep(5)
            driver.get(f'https://www.wunderground.com/forecast/us/ca/{area[idx]}/{stn}')
            page = WebDriverWait(driver, 10).until(                 
            EC.presence_of_element_located((By.CLASS_NAME, "temp-hi"))
            ) 
            page = driver.page_source
            scoop = soup(page, 'html.parser')
            temp_high = scoop.find_all('span', class_='temp-hi')
            temp_low = scoop.find_all('span', class_='temp-lo')
            record_high = [f.get_text().replace("°", "") for f in temp_high] 
            record_low = [f.get_text().replace("°", "") for f in temp_low]
            weather_dict.update({area[idx]: [record_high, record_low]}) 
    finally:
        driver.close()
        driver.quit()
    return weather_dict    