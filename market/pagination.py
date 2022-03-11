from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class DefaultPagination(PageNumberPagination):
    page_size = 30
    
    def get_paginated_response(self, data):
        return Response(data)