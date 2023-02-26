from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef

from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination

from recipes.models import Subscriptions

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.action == 'list':
            user_obj = self.request.user
            subquery = Subscriptions.objects.filter(
                user=user_obj,
                author=OuterRef('pk')
            )
            return User.objects.annotate(is_subscribed=Exists(subquery))
        return super().get_queryset()
