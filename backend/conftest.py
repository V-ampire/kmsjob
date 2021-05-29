from django.utils import timezone

import pytest


pytest_plugins = [
    "vacancies.tests.test_jobparser.fixtures.pytest_fixtures",
]


@pytest.fixture
def now():
    return timezone.now()