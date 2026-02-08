from rest_framework.serializers import ModelSerializer
from DB.models import User

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'created_at']