from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User


class SpyDomeTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['id'] = user.id
        token['email'] = user.email
        return token


class SpyDomeTokenObtainPairView(TokenObtainPairView):
    serializer_class = SpyDomeTokenObtainPairSerializer
