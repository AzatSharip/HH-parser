# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import pickle
import pandas as pd


def links_collector(url, links_base):
    time.sleep(1)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    r = requests.get(url, headers=headers)
    status_code = r.status_code
    if status_code != 200:
        return False
    soup = BeautifulSoup(r.text, features="html.parser")
    links = soup.find_all("a", {"class": "bloko-link HH-LinkModifier"})
    for l in links:
        l = l['href']
        links_base.append(l)


def start_links_col():
    links_base = []
    for page in range(100):
        url = 'https://ufa.hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=Frontend+разработчик&page=' + str(
            page)
        if links_collector(url, links_base) == False:
            print(len(links_base))
            print('404!!!')
            with open(f'links.data', 'wb') as file:
                pickle.dump(links_base, file)
            return links_base

        print(len(links_base))



def data_collector(links_base):
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    for url in links_base:
        print(url)
        time.sleep(1)
        r = requests.get(url, headers=headers)
        status_code = r.status_code
        soup = BeautifulSoup(r.text, features="html.parser")

        bs_data = soup.find_all("span", {"class": "bloko-tag__section bloko-tag__section_text"})
        for d in bs_data:
            print(d.get_text())
            data.append(d.get_text())

    df = pd.DataFrame({'link': links_base, 'skills': data})

    with open(f'df.data', 'wb') as file:
        pickle.dump(data, file)





if __name__ == '__main__':
    #start_links_col()
    with open(f'links.data', 'rb') as file_data:
        data = pickle.load(file_data)

    data_collector(data)










