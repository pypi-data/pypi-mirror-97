from itertools import cycle

import pytest
from model_bakery import baker

from huscy.project_ethics.services import get_ethic_boards

pytestmark = pytest.mark.django_db


def test_ordering():
    baker.make('project_ethics.EthicBoard', name=cycle('A C D B'.split()), _quantity=4)

    result = get_ethic_boards()

    assert ['A', 'B', 'C', 'D'] == [ethic_board.name for ethic_board in result]
