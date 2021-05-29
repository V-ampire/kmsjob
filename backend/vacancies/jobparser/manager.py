import concurrent.futures as cf
import logging
import threading
from typing import Callable, Dict

from vacancies.jobparser.parsers import BaseVacancyParser


logger = logging.getLogger(__name__)


class ThreadedManager(object):
    """
    Управляющий класс для запуска парсеров в несколько потоков.
    """

    def __init__(self) -> None:
        """
        Инициализация.
        Создаем списки парсеров и хендлеров.
        """
        self._parsers = []
    
    def add_parser(self, parser: BaseVacancyParser) -> None:
        """
        Добавить парсер.
        :param parser: Экземпляр парсера, парсеры должны быть унаследованы от 
        base.BaseVacancyParser
        :param config: Конфиг парсера.
        """
        self._parsers.append(parser)

    def run_parser(self, parser: BaseVacancyParser) -> None:
        """
        Запускает парсер и логгирует ошибки.
        :param parser: Экземпляр парсера.
        """
        try:
            return parser.run()
        except Exception as exc:
            # Логгируем все исключения чтобы не потерять их при запуске в отдельном потоке
            logger.exception(exc, exc_info=True)
            raise exc

    def parse(self) -> None:
        """
        Запуск парсеров и обработка результатов в отдельном потоке для каждого парсера.
        """
        if len(self._parsers) > 0:
            with cf.ThreadPoolExecutor(max_workers=len(self._parsers)) as executor:
                for parser in self._parsers:
                    executor.submit(self.run_parser, parser)