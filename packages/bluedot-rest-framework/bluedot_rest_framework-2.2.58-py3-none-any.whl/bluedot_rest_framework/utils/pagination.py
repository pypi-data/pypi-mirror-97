from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_query_param = 'current'
    page_size_query_param = 'pageSize'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'pageSize': self.get_page_size(self.request),
            'current': self.page.number,
            'data': data
        })
