from django.contrib.auth.models import Permission

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN


def test_admin_user_can_create_ethic_board(admin_client):
    response = create_ethic_board(admin_client)

    assert response.status_code == HTTP_201_CREATED


def test_user_with_permission_can_create_ethic_board(client, user):
    create_permission = Permission.objects.get(codename='add_ethicboard')
    user.user_permissions.add(create_permission)

    response = create_ethic_board(client)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_cannot_create_ethic_board(client):
    response = create_ethic_board(client)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_ethic_board(anonymous_client):
    response = create_ethic_board(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_ethic_board(client):
    return client.post(reverse('ethicboard-list'), data=dict(name='foo Bar'))
