from django.utils import timezone
from django.conf import settings

import os
import json
import time
from random import random
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

from vacancies.models import Vacancy


class BaseVacancyParser:
    """
    Базовый класс для парсеров
    """

    name = 'vacancy_parser_class'
    
    def __init__(self, config: Dict, json_output=False):
        self.config = config
        self.json_output = json_output
        self.parse_url = self.config.get('parse_url')
        self.base_url = self.config.get('base_url')

    def get_html(self, url: str) -> str:
        response = requests.get(url)
        if response.status_code < 400:
            return response.text

    def get_vacancies(self):
        """
        Получить данные по parse_url
        """
        raise NotImplementedError('Необходимо определить метод, получающий данные по parse_url.')

    def parse_data(self, vacancy_data) -> List[Dict[str, str]]:
        """
        Распарсить полученные данные и вернуть список словарей формата:
        {'name': '...', 'employer': '...', 'source': '...', ...},
        где name - обязательное поле
        """
        raise NotImplementedError('Необходимо определить метод, чтобы распарсить полученные данные.')

    def save_vacancies_in_db(self, vacancies: List[Dict[str, str]]):
        if vacancies:
            for vacancy_data in vacancies:
                vacancy, created = Vacancy.objects.get_or_create(**vacancy_data)
                if not created:
                    # Если вакансия уже сущ. то обновить ее
                    Vacancy.objects.filter(pk=vacancy.pk).update(**vacancy_data, modified=timezone.now())

    def save_vacancies_as_json(self, vacancies: List[Dict[str, str]]):
        """
        Вывести результаты в json файл.
        """
        filepath = os.path.join(settings.BASE_DIR, 'parser_results', f'{self.name}.json')
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as fp:
            json.dump(vacancies, fp, ensure_ascii=False, indent=4)

    def run(self):
        vacancy_data = self.get_vacancies()
        vacancies = self.parse_data(vacancy_data)
        # Вывод в json
        if self.json_output:
            self.save_vacancies_as_json(vacancies)
        else:
            self.save_vacancies_in_db(vacancies)


class HHParser(BaseVacancyParser):

    name = 'hh'

    def get_vacancies(self):
        params = {
            "area": 1979,
            "period": 1,
            "text": "Комсомольск-на-Амуре",
        }
        response = requests.get(self.parse_url, params)
        if response.status_code < 400:
            return response.json()

    def parse_data(self, data):
        vacancies = []
        if data:
            for item in data['items']:
                vacancy = {
                    'name': item['name'],
                    'employer': item['employer']['name'].lower(),
                    'source': item['alternate_url'],
                    'source_name': self.name,
                }
                vacancies.append(vacancy)
        return vacancies


class AvitoParser(BaseVacancyParser):

    name = 'avito'

    def get_vacancies(self):
        return self.get_html(self.parse_url)

    def parse_data(self, data):
        vacancies = []
        if data:
            soup = BeautifulSoup(data, 'html.parser')
            items = soup.find_all('div', {'data-marker': 'item'})
            for item in items:
                if self.is_today_vacancy(item):
                    vacancy = {
                        'name': item.find('a', {'data-marker': 'item-title'}).get_text(),
                        'source': self.base_url + item.find('a', {'data-marker': 'item-title'}).get('href'),
                        'source_name': self.name,
                    }
                    vacancies.append(vacancy)
        return vacancies

    def is_today_vacancy(self, item):
        """
        Вернуть True если вакансия сегодняшняя, иначе False
        """
        data_str = item.find('div', {'data-marker': 'item-date'}).get_text()
        return data_str.lower().find('час') >= 0 or data_str.lower().find('минут') >= 0


class FarpostParser(BaseVacancyParser):

    name = 'farpost'

    def get_vacancies(self):
        return self.get_html(self.parse_url) # FIXME get with pagination

    def parse_data(self, data):
        vacancies = []
        if data:
            soup = BeautifulSoup(data, 'html.parser')
            items = soup.find_all('tr', class_='bull-item')
            for item in items:
                if self.is_today_vacancy(item):
                    vacancy = {
                        'name': item.find('a', class_='bulletinLink').get_text(),
                        'employer': self.get_employer(item),
                        'source': self.base_url + item.find('a', class_='bulletinLink').get('href'),
                        'source_name': self.name,
                    }
                    vacancies.append(vacancy)
        return vacancies

    def get_employer(self, item):
        """
        Распарсить работадотеля или вернуть пустую строку.
        """
        employer_div = item.find('div', class_='bull-item__annotation-row')
        return employer_div.get_text() if employer_div is not None else ''

    def is_today_vacancy(self, item):
        """
        Определяет имеет ли вакансия сегодняшнюю дату.
        Вакансии на сегодня либо не имеют даты либо включают слово сегодня.
        """
        date_div = item.find('div', class_='date')
        return date_div is None or date_div.get_text().find('сегодня') >= 0


class VkParser(BaseVacancyParser):

    name = 'vk'  
    
    def get_vacancies(self):
        params = {
            'q': r'#РаботаКомсомольск',
            'access_token': self.config.get('access_token'),
            'v': self.config.get('v'),
            'start_time': int(time.time()) - 86400,
        }
        response = requests.get(self.parse_url, params)
        return response.json()

    def parse_data(self, data):
        vacancies = []
        if data:
            for post in data['response']['items']:
                name_end_index = post.get('text').find('\n')
                vacancy = {
                    'name': post.get('text')[:name_end_index],
                    'description': post.get('text'),
                    'source': '{}/wall{}_{}'.format(self.base_url,
                                                    str(post.get('owner_id')), 
                                                    post.get('id')),
                    'source_name': self.name,
                }
                vacancies.append(vacancy)
        return vacancies

    
class SuperjobParser(BaseVacancyParser):

    name = 'superjob'

    def get_vacancies(self):
        params = {
            'period': 1,
            'town': 731
        }
        headers = {
            'X-Api-App-Id': self.config.get('secret_key')
        }
        url = '{}/{}/vacancies'.format(self.parse_url, self.config.get('v'))
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def parse_data(self, data):
        vacancies = []
        if data:
            for item in data['objects']:
                vacancy = {
                    'name': item['profession'],
                    'employer': item['client']['title'],
                    'source': item['link'],
                    'source_name': self.name
                }
                vacancies.append(vacancy)
        return vacancies
 

parsers_list = {
    'avito': AvitoParser,
    'farpost': FarpostParser,
    'vk': VkParser,
    'superjob': SuperjobParser,
    'hh': HHParser,
}