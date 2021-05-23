from rest_framework import permissions


class ShareAppIsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.(自定義對所有的訪問進行認證)
    """

    def has_permission(self, request, view):

        # print(request.META['HTTP_AUTH'])
        # print('111')
        print(request.user)
        # print('222')

        return False if request.user != 'sample user' else True



