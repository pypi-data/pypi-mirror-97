from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission


class EthicPermissions(BasePermission):
    perms_map = {
        'DELETE': ['projects.change_project'],
        'GET': ['projects.view_project'],
        'HEAD': [],
        'OPTIONS': [],
        'POST': ['projects.change_project'],
        'PUT': ['projects.change_project'],
    }

    def has_permission(self, request, view):
        if request.method not in self.perms_map:
            raise MethodNotAllowed(request.method)

        if request.method == 'GET' and view.detail is True:
            raise MethodNotAllowed(request.method)

        perms = self.perms_map[request.method]

        return request.user.has_perms(perms) or request.user.has_perms(perms, view.project)


class EthicFilePermissions(BasePermission):
    perms_map = {
        'DELETE': ['projects.change_project'],
        'HEAD': [],
        'OPTIONS': [],
        'POST': ['projects.change_project'],
    }

    def has_permission(self, request, view):
        if request.method not in self.perms_map:
            raise MethodNotAllowed(request.method)

        perms = self.perms_map[request.method]

        return request.user.has_perms(perms) or request.user.has_perms(perms, view.ethic.project)


class DeleteEthicFilePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.has_perm('project_ethics.delete_ethicfile')
        return True
