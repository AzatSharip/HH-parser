# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import pickle
import pandas as pd
import random
from Configurations.pw import matvei_pass
from Share_monitoring.main import gemail_sender


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
    with open(f'links.data', 'wb') as file:
        for page in range(100):
            url = 'https://ufa.hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=Frontend+разработчик&page=' + str(
                page)
            if links_collector(url, links_base) == False:
                print(len(links_base))
                print('404!!!')
                pickle.dump(links_base, file)
                return links_base

            #ickle.dump(links_base, file)
            print(len(links_base))
            #return links_base


def skills_collector(links_base):
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    with open(f'skills.data', 'wb') as file:
        for url in links_base:
            print(url)
            time.sleep(random.randrange(1, 3))
            r = requests.get(url, headers=headers)
            status_code = r.status_code
            soup = BeautifulSoup(r.text, features="html.parser")

            bs_data = soup.find_all("span", {"class": "bloko-tag__section bloko-tag__section_text"})
            temp_lst = []
            for d in bs_data:
                print(d.get_text())
                temp_lst.append(d.get_text())


            data.append(temp_lst)
            print(data)
        print(data)
        pickle.dump(data, file)


def make_df():
    with open(f'links.data', 'rb') as file:
        links = pickle.load(file)
    with open(f'skills.data', 'rb') as file:
        skills = pickle.load(file)
    with open(f'salary.data', 'rb') as file:
        salary = pickle.load(file)

    print(len(links))
    print(len(skills))
    print(len(salary))

    df = pd.DataFrame({'link': links, 'skills': skills, 'salary': salary})
    print(df)
    return df


def salary_collector(links_base):
    salary_list = []
    time.sleep(random.randrange(1, 3))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}

    with open(f'salary.data', 'wb') as file:
        for url in links_base:
            print(url)
            time.sleep(random.randrange(1, 3))
            r = requests.get(url, headers=headers)
            status_code = r.status_code
            soup = BeautifulSoup(r.text, features="html.parser")

            bs_salary = soup.find_all("p", {"class": "vacancy-salary"})

            for s in bs_salary:
                s = s.get_text()
                print(s)
                salary_list.append(s)

        pickle.dump(salary_list, file)


def to_excel(df):
    excel_file = df.to_excel(r'D:\Personal\GitHub\HH-parser\HH.xlsx', index=False)
    return excel_file


if __name__ == '__main__':
    #links = start_links_col()
    # with open(f'links.data', 'rb') as file_data:
    #     links = pickle.load(file_data)

    # skills_collector(links)
    # salary_collector(links)
    df = make_df()
    to_excel(df)
    gemail_sender(epass=matvei_pass, email_theme='HI Ozzy')










