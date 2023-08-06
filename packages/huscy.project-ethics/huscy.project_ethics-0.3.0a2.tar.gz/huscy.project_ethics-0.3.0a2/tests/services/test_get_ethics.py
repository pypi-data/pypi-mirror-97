from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_ethics.services import get_or_create_ethics

pytestmark = pytest.mark.django_db


def test_get_ethics_without_project():
    ethics = create_ethics()
    result = get_or_create_ethics()

    assert list(result) == ethics


def test_get_ethics_filtered_by_project():
    ethics = create_ethics()

    result = get_or_create_ethics(ethics[0].project)

    assert len(result) == 2
    assert list(result) == [ethics[0], ethics[3]]


def test_create_ethics_for_project(project):
    assert len(get_or_create_ethics()) == 0  # no ethics present

    result = get_or_create_ethics(project)  # create ethic

    assert len(get_or_create_ethics()) == 1

    assert list(result) == list(get_or_create_ethics(project))  # get but no create


def create_ethics():
    projects = baker.make('projects.Project', _quantity=3)
    return baker.make('project_ethics.Ethic', project=cycle(projects), _quantity=6)
