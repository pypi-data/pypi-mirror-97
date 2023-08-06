import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.project_ethics.models import EthicFile

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_ethic_files(admin_client, ethic, tmp_file):
    response = upload_ethic_file(admin_client, ethic, tmp_file)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_create_ethic_files(client, user, ethic, tmp_file):
    change_project_permission = Permission.objects.get(codename='change_project')
    user.user_permissions.add(change_project_permission)

    response = upload_ethic_file(client, ethic, tmp_file)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_create_ethic_files(client, ethic, tmp_file):
    response = upload_ethic_file(client, ethic, tmp_file)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_ethic_files(anonymous_client, ethic, tmp_file):
    response = upload_ethic_file(anonymous_client, ethic, tmp_file)

    assert response.status_code == HTTP_403_FORBIDDEN


def upload_ethic_file(client, ethic, tmp_file):
    with open(tmp_file, 'r') as f:
        data = dict(
            ethic=ethic.id,
            filehandle=f,
            filetype=EthicFile.TYPE.get_value('proposal'),
        )
        return client.post(
            reverse('ethicfile-list', kwargs=dict(project_pk=ethic.project.pk, ethic_pk=ethic.pk)),
            data=data
        )
