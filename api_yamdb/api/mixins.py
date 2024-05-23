from rest_framework import serializers

from reviews.validators import UsernameRegexValidator, username_is_not_me
from reviews.constans import MAX_LENGTH_USERNAME


class UsernameMixin(metaclass=serializers.SerializerMetaclass):
    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME,
        validators=(UsernameRegexValidator(), username_is_not_me),
    )
