import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_ethic(admin_client, ethic):
    response = delete_ethic(admin_client, ethic)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_can_delete_ethic(client, ethic):
    response = delete_ethic(client, ethic)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_anonymous_user_cannot_delete_ethic(anonymous_client, ethic):
    response = delete_ethic(anonymous_client, ethic)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_ethic(client, ethic):
    return client.delete(
        reverse('ethic-detail', kwargs=dict(project_pk=ethic.project.pk, pk=ethic.pk))
    )
