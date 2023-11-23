from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import chromedriver_autoinstaller
import json
import re
import os
from datetime import datetime


def get_analyst_info(raw_data):
    # info = {
    #     'order_number': "None",
    #     'name_champion': "None",
    #     'match': "None",
    #     'kda': "None",
    #     'win_rate': "None",
    #     'pick': "None",
    #     'ban': "None",
    #     'cs': "None",
    #     'gold': "None",
    #     'queue': "None",
    #     'rank': "None",
    #     'region': "None",
    #     'period': "None",
    #     'role': "None"
    # }
    info = {}
    mark = 1
    list_info = []
    for i in range(0, len(raw_data)):
        if mark == 1:
            info['order_number'] = raw_data[i]
        elif mark == 2:
            info['name_champion'] = raw_data[i]
        elif mark == 3:
            info['match'], info['kda'] = raw_data[i].split(" ")
        elif mark == 4:
            info['win_rate'] = raw_data[i]
        elif mark == 5:
            info['ban'] = raw_data[i]
        elif mark == 6:
            mark = 0
            info['ban'], info['cs'], info['gold'] = raw_data[i].split(
                " ")
            info['queue'] = 'solo'
            info['rank'] = 'platinum'
            info['region'] = 'vietnam'
            list_info.append(info)
            info = {}
        mark += 1
    return list_info


def main():
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome()
    driver.get(
        "https://www.op.gg/statistics/champions?region=vn&period=day&position=&tier=platinum")
    wait = WebDriverWait(driver, 1)

    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    sleep(3)
    info_elements = driver.find_element(
        By.XPATH, '//*[@id="content-container"]/div[2]/table/tbody')

    list_info = get_analyst_info(info_elements.text.split('\n'))

    now = datetime.now()
    now_format = now.strftime("%Y_%m_%d %H_%M_%S")
    file_name_info = f'info_{now_format}.json'

    # # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    # Create the path to the output file
    file_name_info = os.path.join(parent_dir, 'data', file_name_info)
    with open(file_name_info, 'w', encoding='utf-8') as file:
        json.dump(list_info, file)
    driver.quit()


if __name__ == "__main__":
    main()
