from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.SerializerMethodField()
    days_since_joined = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('url', 'pk', 'username', 'first_name', 'last_name',
                  'full_name', 'email', 'days_since_joined')

    def get_days_since_joined(self, obj):
        return (timezone.now() - obj.date_joined).days

    def get_full_name(self, obj):
        if not (obj.first_name and obj.last_name):
            return ""
        return f"{obj.first_name} {obj.last_name}"
