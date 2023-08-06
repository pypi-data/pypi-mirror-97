from huscy.project_ethics.models import Ethic, EthicBoard, EthicFile


def create_ethic(project, ethic_board=None, code=''):
    return Ethic.objects.create(project=project, ethic_board=ethic_board, code=code)


def create_ethic_file(ethic, filehandle, filetype, creator):
    filename = filehandle.name.split('/')[-1]

    return EthicFile.objects.create(
        ethic=ethic,
        filehandle=filehandle,
        filename=filename,
        filetype=filetype,
        uploaded_by=creator.get_full_name(),
    )


def get_ethic_files(ethic):
    return EthicFile.objects.filter(ethic=ethic)


def get_or_create_ethics(project=None):
    queryset = Ethic.objects.order_by('pk')
    if project is not None:
        filtered_queryset = queryset.filter(project=project)
        if not filtered_queryset.exists():
            Ethic.objects.create(project=project)
        return filtered_queryset
    return queryset


def get_ethic_boards():
    return EthicBoard.objects.order_by('name')
