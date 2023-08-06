from django.contrib.auth import get_user_model

User = get_user_model()


class UsernameAsEmailBackend:
    """Login with a username that may be an email.

    Mostly based on django.contrib.auth.backends.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        # Only consider usernames-as-emails that have '@'
        if not username or "@" not in username:
            return None

        try:
            user = User._default_manager.get(email=username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None

    @staticmethod
    def user_can_authenticate(user):
        """Reject users with is_active=False."""
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None
