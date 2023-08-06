import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_ethic(admin_client, ethic):
    response = update_ethic(admin_client, ethic)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_update_ethic(client, user, ethic):
    change_project_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(change_project_permission)

    response = update_ethic(client, ethic)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_update_ethic(client, ethic):
    response = update_ethic(client, ethic)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_update_ethic(anonymous_client, ethic):
    response = update_ethic(anonymous_client, ethic)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission,expected_status_code', [
    (True, False, HTTP_200_OK),          # project coordinator
    (False, True, HTTP_200_OK),          # member with write permission
    (False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_updates_ethic(client, user, ethic, is_coordinator, has_write_permission,
                                      expected_status_code):
    add_member(ethic.project, user, is_coordinator, has_write_permission)

    response = update_ethic(client, ethic)

    assert response.status_code == expected_status_code


def update_ethic(client, ethic):
    return client.put(
        reverse('ethic-detail', kwargs=dict(project_pk=ethic.project.pk, pk=ethic.pk)),
        data=dict(code='foobar')
    )
