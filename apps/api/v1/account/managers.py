from django.contrib.auth.models import UserManager

class ActiveManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted=False
        )