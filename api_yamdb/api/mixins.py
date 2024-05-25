from reviews.validators import validate_username, username_is_not_forbidden


class UsernameMixin:
    def validate_username(self, username):
        return validate_username(username_is_not_forbidden(username))
