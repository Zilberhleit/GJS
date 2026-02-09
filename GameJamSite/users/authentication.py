from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend, BaseBackend


class EmailAuthBackend(BaseBackend):
    """ Аутентификация по email """

    def authenticate(self, request, email=None, password=None):
        """  Получение пользователя по email и проверка пароля """
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return
        else:
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        """ Получение пользователя по id """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


class EmailOrUsernameAuthBackend(BaseBackend): 
    """ Аутентификация по email или username """

    def authenticate(self, request, username = None, password = None):
        """ Получение пользователя по email или по nickname"""
        User = get_user_model()
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else: 
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return
        else:
            if user.check_password(password):
                return user
            
    def get_user(self, user_id):
        """ Получение пользователя по id """
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None