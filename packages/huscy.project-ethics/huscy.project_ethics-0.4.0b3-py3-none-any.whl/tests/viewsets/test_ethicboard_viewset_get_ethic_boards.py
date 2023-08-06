from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_list_ethic_boards(admin_client):
    response = list_ethic_boards(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_can_list_ethic_boards(client):
    response = list_ethic_boards(client)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_list_ethic_boards(anonymous_client):
    response = list_ethic_boards(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_ethic_boards(client):
    return client.get(reverse('ethicboard-list'))
