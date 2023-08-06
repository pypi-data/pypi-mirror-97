from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.projects.models import Project
from huscy.project_ethics import serializer, services
from huscy.project_ethics.models import Ethic
from huscy.project_ethics.permissions import (
    DeleteEthicFilePermission,
    EthicPermissions,
    EthicFilePermissions,
)
from huscy.project_ethics.services import get_ethic_files


class EthicBoardViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_ethic_boards()
    serializer_class = serializer.EthicBoardSerializer


class EthicViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, EthicPermissions)
    serializer_class = serializer.EthicSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_or_create_ethics(self.project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        return context


class EthicFileViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, EthicFilePermissions, DeleteEthicFilePermission)
    serializer_class = serializer.EthicFileSerializer

    def initial(self, request, *args, **kwargs):
        self.ethic = get_object_or_404(
            Ethic, pk=self.kwargs['ethic_pk'], project=self.kwargs['project_pk']
        )
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return get_ethic_files(self.ethic)
