import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_update_ethic(admin_client, ethic):
    response = update_ethic(admin_client, ethic)

    assert response.status_code == HTTP_200_OK


def test_user_can_update_ethic(client, ethic):
    response = update_ethic(client, ethic)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_update_ethic(anonymous_client, ethic):
    response = update_ethic(anonymous_client, ethic)

    assert response.status_code == HTTP_403_FORBIDDEN


def update_ethic(client, ethic):
    return client.patch(
        reverse('ethic-detail', kwargs=dict(project_pk=ethic.project.pk, pk=ethic.pk)),
        data=dict(code='foobar')
    )
