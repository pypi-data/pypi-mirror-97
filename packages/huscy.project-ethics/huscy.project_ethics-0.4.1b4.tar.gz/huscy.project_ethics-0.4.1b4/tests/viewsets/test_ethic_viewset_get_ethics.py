import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_retrieve_ethics_is_not_provided(client, ethic):
    response = client.get(
        reverse('ethic-detail', kwargs=dict(project_pk=ethic.project.pk, pk=ethic.pk))
    )

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_admin_user_can_list_ethics(admin_client, project):
    response = list_ethics(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_user_with_permission_can_list_ethics(client, user, project):
    view_project_permission = Permission.objects.get(codename='view_project')
    user.user_permissions.add(view_project_permission)

    response = list_ethics(client, project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_cannot_list_ethics(client, project):
    response = list_ethics(client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_list_ethics(anonymous_client, project):
    response = list_ethics(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize('is_coordinator,has_write_permission', [
    (True, False),   # project coordinator
    (False, True),   # member with write permission
    (False, False),  # member with read permission
])
def test_all_project_members_can_list_ethics(client, user, project, is_coordinator,
                                             has_write_permission):
    add_member(project, user, is_coordinator, has_write_permission)

    response = list_ethics(client, project)

    assert response.status_code == HTTP_200_OK


def list_ethics(client, project):
    return client.get(reverse('ethic-list', kwargs=dict(project_pk=project.pk)))
