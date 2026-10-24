from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    ordering = ['-id'] # TODO
    page_size = 20