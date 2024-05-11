from django.db import models

class Code(models.Model):
    code = models.IntegerField(max_length=6)
    user = models.OneToOneField('auth.User',
        on_delete=models.CASCADE,
        related_name='user')