import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_ethic(admin_client, project, ethic_board):
    response = create_ethic(admin_client, project, ethic_board)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_create_ethic(client, user, project, ethic_board):
    change_project_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(change_project_permission)

    response = create_ethic(client, project, ethic_board)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_create_ethic(client, project, ethic_board):
    response = create_ethic(client, project, ethic_board)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_ethic(anonymous_client, project, ethic_board):
    response = create_ethic(anonymous_client, project, ethic_board)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission,expected_status_code', [
    (True, False, HTTP_201_CREATED),     # project coordinator
    (False, True, HTTP_201_CREATED),     # member with write permission
    (False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_creates_ethic(client, user, project, ethic_board, is_coordinator,
                                      has_write_permission, expected_status_code):
    add_member(project, user, is_coordinator, has_write_permission)

    response = create_ethic(client, project, ethic_board)

    assert response.status_code == expected_status_code


def create_ethic(client, project, ethic_board):
    data = dict(
        code='123/12-ek',
        ethic_board=ethic_board.id,
    )
    return client.post(reverse('ethic-list', kwargs=dict(project_pk=project.pk)), data=data)
