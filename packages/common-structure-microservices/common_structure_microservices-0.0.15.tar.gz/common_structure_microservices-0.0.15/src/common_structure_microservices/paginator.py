from common_structure_microservices.messages import Messages
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            'paginator': {
                'count': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'status': True,
            'message': Messages.SUCCESSFUL_MESSAGE,
            'data': data
        })