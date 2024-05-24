from reviews.validators import validate_username, username_is_not_forbidden


class UsernameMixin:
    def validate_username(self, username):
        validate_username(username)
        username_is_not_forbidden(username)
        return username
