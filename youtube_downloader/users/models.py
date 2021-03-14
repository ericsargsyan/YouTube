from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.ForeignKey(User.email, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images', default='default.png')

    def __str__(self):
        return f"{self.user.username}"
