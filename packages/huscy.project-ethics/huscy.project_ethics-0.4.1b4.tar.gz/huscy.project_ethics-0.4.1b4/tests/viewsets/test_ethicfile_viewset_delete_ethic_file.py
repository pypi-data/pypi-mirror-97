import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

from huscy.projects.services import add_member

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_ethic_files(admin_client, ethic, ethic_file):
    response = delete_ethic_file(admin_client, ethic, ethic_file)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_with_permission_can_delete_ethic_files(client, user, ethic, ethic_file):
    change_project_permission = Permission.objects.get(codename='change_project')
    delete_ethicfile_permission = Permission.objects.get(codename='delete_ethicfile')
    user.user_permissions.add(change_project_permission, delete_ethicfile_permission)

    response = delete_ethic_file(client, ethic, ethic_file)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_cannot_delete_ethic_files(client, ethic, ethic_file):
    response = delete_ethic_file(client, ethic, ethic_file)

    assert response.status_code == HTTP_403_FORBIDDEN


@pytest.mark.parametrize(('can_delete_ethicfiles,is_coordinator,has_write_permission,'
                          'expected_status_code'), [
    (True, True, False, HTTP_204_NO_CONTENT),   # project coordinator
    (True, False, True, HTTP_204_NO_CONTENT),   # member with write permission
    (True, False, False, HTTP_403_FORBIDDEN),   # member with read permission

    (False, True, False, HTTP_403_FORBIDDEN),   # project coordinator
    (False, False, True, HTTP_403_FORBIDDEN),   # member with write permission
    (False, False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_deletes_ethic_file(client, user, ethic, ethic_file, can_delete_ethicfiles,
                                           is_coordinator, has_write_permission,
                                           expected_status_code):
    if can_delete_ethicfiles:
        delete_permission = Permission.objects.get(codename='delete_ethicfile')
        user.user_permissions.add(delete_permission)
    add_member(ethic.project, user, is_coordinator, has_write_permission)

    response = delete_ethic_file(client, ethic, ethic_file)

    assert response.status_code == expected_status_code


def test_anonymous_user_cannot_delete_ethic_files(anonymous_client, ethic, ethic_file):
    response = delete_ethic_file(anonymous_client, ethic, ethic_file)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_ethic_file(client, ethic, ethic_file):
    return client.delete(
        reverse(
            'ethicfile-detail',
            kwargs=dict(project_pk=ethic.project.pk, ethic_pk=ethic.pk, pk=ethic_file.pk)
        )
    )
