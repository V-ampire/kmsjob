from django.conf import settings

from vacancies.jobparser.parsers import parsers_list
from vacancies.jobparser.manager import ThreadedManager


configs = settings.PARSERS_CONFIG


def parse(json_output=False):
    """
    Запускает парсинг сайтов.
    """
    manager = ThreadedManager()
    for parser_name in configs.keys():
        if configs[parser_name]['is_active']:
            parser_cls = parsers_list.get(parser_name, None)
            if parser_cls is not None:
                manager.add_parser(parser_cls(configs[parser_name], json_output))
    
    manager.parse()
