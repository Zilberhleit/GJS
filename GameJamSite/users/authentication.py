from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, BaseBackend


class EmailAuthBackend(BaseBackend):
    """ Аутентификация по email """

    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
