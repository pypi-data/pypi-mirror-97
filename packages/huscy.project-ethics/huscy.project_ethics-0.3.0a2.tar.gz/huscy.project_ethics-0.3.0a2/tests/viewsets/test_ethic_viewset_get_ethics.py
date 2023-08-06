from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_ethics_is_not_provided(client, ethic):
    response = client.get(
        reverse('ethic-detail', kwargs=dict(project_pk=ethic.project.pk, pk=ethic.pk))
    )

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_list_ethics_is_not_provided(client, project):
    response = client.get(reverse('ethic-list', kwargs=dict(project_pk=project.pk)))

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
