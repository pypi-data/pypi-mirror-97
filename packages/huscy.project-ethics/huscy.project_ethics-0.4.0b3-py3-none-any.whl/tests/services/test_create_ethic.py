import pytest

from huscy.project_ethics.services import create_ethic

pytestmark = pytest.mark.django_db


def test_create_ethic(project):
    result = create_ethic(project)

    assert result.project == project
    assert result.ethic_board is None
    assert result.code == ''


def test_create_with_ethic_board(project, ethic_board):
    result = create_ethic(project, ethic_board)

    assert result.project == project
    assert result.ethic_board is ethic_board
    assert result.code == ''


def test_create_with_code(project):
    result = create_ethic(project, code='1234567890')

    assert result.project == project
    assert result.ethic_board is None
    assert result.code == '1234567890'


def test_create_with_ethic_board_and_code(project, ethic_board):
    result = create_ethic(project, ethic_board, '1234567890')

    assert result.project == project
    assert result.ethic_board is ethic_board
    assert result.code == '1234567890'
