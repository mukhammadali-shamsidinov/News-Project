from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/images', blank=True, null=True)
    data_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.username


