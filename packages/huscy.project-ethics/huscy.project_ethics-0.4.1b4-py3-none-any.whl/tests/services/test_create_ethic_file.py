from datetime import datetime

import pytest

from django.core.files import File

from huscy.project_ethics.models import EthicFile
from huscy.project_ethics.services import create_ethic_file


@pytest.mark.freeze_time('2020-01-01 10:00:00')
def test_create_ethic_file(user, ethic, tmp_file):
    filetype = EthicFile.TYPE.get_value('proposal')

    with open(tmp_file, 'r') as fh:
        filehandle = File(fh)
        result = create_ethic_file(ethic, filehandle, filetype, user)

        assert result.ethic == ethic
        assert result.filetype == filetype
        assert result.filename == 'tmp.txt'
        assert result.uploaded_at == datetime(2020, 1, 1, 10)
        assert result.uploaded_by == 'Erik Zion'
