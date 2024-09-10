from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission


class NeedLogin(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = {'message': 'Authentication credentials were not provided.'}


class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            raise NeedLogin
        return True
