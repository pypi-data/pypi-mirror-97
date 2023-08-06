import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_ethic(admin_client, project, ethic_board):
    response = create_ethic(admin_client, project, ethic_board)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_can_create_ethic(client, project, ethic_board):
    response = create_ethic(client, project, ethic_board)

    assert response.status_code == HTTP_201_CREATED


def test_anonymous_user_cannot_create_ethic(anonymous_client, project, ethic_board):
    response = create_ethic(anonymous_client, project, ethic_board)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_ethic(client, project, ethic_board):
    data = dict(
        code='123/12-ek',
        ethic_board=ethic_board.id,
    )
    return client.post(reverse('ethic-list', kwargs=dict(project_pk=project.pk)), data=data)
