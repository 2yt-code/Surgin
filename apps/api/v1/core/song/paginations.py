from rest_framework.pagination import CursorPagination


class ExploreSearchPagination(CursorPagination):
    ordering = ['-id']