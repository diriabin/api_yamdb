from rest_framework import serializers

from reviews.validators import validate_username, username_is_not_me
from reviews.constans import MAX_LENGTH_USERNAME


class UsernameMixin:
        def validate_username(self, username):
            validate_username(username)
            username_is_not_me(username)
            return username
