# -*- coding: utf-8 -*-

__author__ = 'Adler'

from django.contrib.auth.models import User


class ClientNameAuthBackend(object):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)

            if user.check_password(password):
                return user
        except User.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

        return None