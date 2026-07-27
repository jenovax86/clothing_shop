from django.http import HttpResponse
from rest_framework.views import APIView

from core.exceptions import NotFoundException, ConflictException


class TestView(APIView):
    def get(self, request):
        raise ConflictException()
