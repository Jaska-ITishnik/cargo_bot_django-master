from django.contrib.auth.models import UserManager


class NotRegisteredUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(user__isnull=True)
