from rest_framework.pagination import PageNumberPagination

from api.constants import Limit


class LimitPagination(PageNumberPagination):
    """Пагинация по парамерту"""
    page_size_query_param = "limit"
    page_size = Limit.PAGINATION_PAGE_SIZE
