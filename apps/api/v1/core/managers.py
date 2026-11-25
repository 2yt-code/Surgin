from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            deleted=False
        )
    
    def get_by_natural_key(self, *args):
        return self.get_queryset().get_by_natural_key(*args)