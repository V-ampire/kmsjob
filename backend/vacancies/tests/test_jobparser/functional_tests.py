from django.conf import settings

from vacancies.jobparser import parsers
from vacancies.jobparser.tasks import parse

import pytest


@pytest.mark.django_db
def test_hh_parser():
    config = settings.PARSERS_CONFIG.get('hh')
    parser = parsers.HHParser(config, json_output=True)
    parser.run()


@pytest.mark.django_db
def test_superjob_parser():
    config = settings.PARSERS_CONFIG.get('superjob')
    parser = parsers.SuperjobParser(config, json_output=True)
    parser.run()


@pytest.mark.django_db
def test_vk_parser():
    config = settings.PARSERS_CONFIG.get('vk')
    parser = parsers.VkParser(config, json_output=True)
    parser.run()


@pytest.mark.django_db
def test_farpost_parser():
    config = settings.PARSERS_CONFIG.get('farpost')
    parser = parsers.FarpostParser(config, json_output=True)
    parser.run()


@pytest.mark.django_db
def test_avito_parser():
    config = settings.PARSERS_CONFIG.get('avito')
    parser = parsers.AvitoParser(config, json_output=True)
    parser.run()


@pytest.mark.django_db
def test_parse_in_threads():
    parse(json_output=True)