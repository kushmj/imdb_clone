from rest_framework.pagination import PageNumberPagination, BasePagination,CursorPagination,LimitOffsetPagination

class MovieListPagination(PageNumberPagination):
    page_size = 5
    