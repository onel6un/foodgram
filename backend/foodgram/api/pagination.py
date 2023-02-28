from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    def get_page_size(self, request):
        if request.query_params.get('limit') is not None:
            return int(request.query_params.get('limit'))
        return 10
