from enum import Enum

from django.db import models

from huscy.projects.models import Project


class EthicBoard(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Ethic(models.Model):
    code = models.CharField(max_length=255, blank=True, default='')
    ethic_board = models.ForeignKey(EthicBoard, on_delete=models.PROTECT, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class EthicFile(models.Model):
    class TYPE(Enum):
        proposal = (0, 'Proposal')
        votum = (1, 'Votum')
        amendment = (2, 'Amendment')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    def get_upload_path(self, filename):
        return f'ethics/{filename}'

    ethic = models.ForeignKey(Ethic, on_delete=models.CASCADE, related_name='ethic_files')

    filetype = models.PositiveSmallIntegerField(choices=[x.value for x in TYPE])

    filehandle = models.FileField(upload_to=get_upload_path)
    filename = models.CharField(max_length=255)

    uploaded_at = models.DateTimeField(auto_now_add=True, editable=False)
    uploaded_by = models.CharField(max_length=126, editable=False)
