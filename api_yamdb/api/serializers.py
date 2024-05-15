from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Title


class TitleSerializer(serializers.Serializer):
    author = SlugRelatedField(slug='username', read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
