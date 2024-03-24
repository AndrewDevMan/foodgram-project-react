from rest_framework.pagination import PageNumberPagination

from api import constants


class LimitPagination(PageNumberPagination):
    """Пагинация по парамерту"""
    page_size_query_param = "limit"
    page_size = constants.PAGINATION_PAGE_SIZE
