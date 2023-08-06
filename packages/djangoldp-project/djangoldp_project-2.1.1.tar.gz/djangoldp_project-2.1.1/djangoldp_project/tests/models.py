from django.contrib.auth.models import AbstractUser

from djangoldp.models import Model


class User(AbstractUser, Model):

    class Meta(AbstractUser.Meta, Model.Meta):
        serializer_fields = ['@id', 'username', 'first_name', 'last_name', 'email']
        anonymous_perms = ['view', 'add']
        authenticated_perms = ['inherit', 'change']
        owner_perms = ['inherit']
