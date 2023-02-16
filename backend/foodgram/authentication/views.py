
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import GetTokenSerializer


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer
