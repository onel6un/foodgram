from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    def get_page_size(self, request):
        page_size = 10
        if request.query_params.get('limit') is not None:
            page_size = int(request.query_params.get('limit'))
        return page_size
