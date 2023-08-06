import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.project_ethics.models import EthicFile
from huscy.projects.services import add_member

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


@pytest.mark.parametrize('is_coordinator,has_write_permission,expected_status_code', [
    (True, False, HTTP_201_CREATED),     # project coordinator
    (False, True, HTTP_201_CREATED),     # member with write permission
    (False, False, HTTP_403_FORBIDDEN),  # member with read permission
])
def test_project_member_creates_ethic_file(client, user, ethic, tmp_file, is_coordinator,
                                           has_write_permission, expected_status_code):
    add_member(ethic.project, user, is_coordinator, has_write_permission)

    response = upload_ethic_file(client, ethic, tmp_file)

    assert response.status_code == expected_status_code


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
