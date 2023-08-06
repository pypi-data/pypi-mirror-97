from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_is_not_allowed(client, project, ethic, ethic_file):
    response = client.get(
        reverse(
            'ethicfile-detail',
            kwargs=dict(project_pk=project.pk, ethic_pk=ethic.pk, pk=ethic_file.id)
        )
    )

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_list_is_not_allowed(client, project, ethic):
    response = client.get(
        reverse('ethicfile-list', kwargs=dict(project_pk=project.pk, ethic_pk=ethic.pk))
    )

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
