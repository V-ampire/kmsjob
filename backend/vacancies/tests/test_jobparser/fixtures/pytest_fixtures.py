from django.conf import settings

import json
import pytest
import os


AVITO_JSON_PATH = os.path.join(
    settings.BASE_DIR, 
    'vacancies/tests/test_jobparser/fixtures/avito.json'
)
FARPOST_JSON_PATH = os.path.join(
    settings.BASE_DIR, 
    'vacancies/tests/test_jobparser/fixtures/farpost.json'
)
HH_JSON_PATH = os.path.join(
    settings.BASE_DIR, 
    'vacancies/tests/test_jobparser/fixtures/hh.json'
)
SUPERJOB_JSON_PATH = os.path.join(
    settings.BASE_DIR, 
    'vacancies/tests/test_jobparser/fixtures/superjob.json'
)
VK_JSON_PATH = os.path.join(
    settings.BASE_DIR, 
    'vacancies/tests/test_jobparser/fixtures/vk.json'
)


@pytest.fixture
def avito_vacancies():
    with open(AVITO_JSON_PATH, 'r') as fp:
        return json.load(fp)


@pytest.fixture
def farpost_vacancies():
    with open(FARPOST_JSON_PATH, 'r') as fp:
        return json.load(fp)


@pytest.fixture
def hh_vacancies():
    with open(HH_JSON_PATH, 'r') as fp:
        return json.load(fp)


@pytest.fixture
def superjob_vacancies():
    with open(SUPERJOB_JSON_PATH, 'r') as fp:
        return json.load(fp)


@pytest.fixture
def vk_vacancies():
    with open(VK_JSON_PATH, 'r') as fp:
        return json.load(fp)