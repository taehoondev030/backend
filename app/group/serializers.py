"""
serializers for Group APIs
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Group
from django.conf import settings

class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many = True, # 필드가 여러 개의 값을 가질 수 있음
        queryset = get_user_model().objects.all()
    )

    class Meta:
        model = Group
        fields = ['id', 'members', 'created_at']
        read_only_fields = ['id']

class GroupDetailSerializer(GroupSerializer):
    """Serializer for Group detail view"""

    class meta(GroupSerializer.Meta):
        fields = GroupSerializer.Meta.fields