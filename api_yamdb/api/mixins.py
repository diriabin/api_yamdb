from reviews.validators import validate_username, username_is_not_me


class UsernameMixin:
    def validate_username(self, username):
        validate_username(username)
        username_is_not_me(username)
        return username
