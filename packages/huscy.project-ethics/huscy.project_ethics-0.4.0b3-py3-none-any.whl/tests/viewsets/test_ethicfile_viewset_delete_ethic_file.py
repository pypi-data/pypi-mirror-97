import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

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
