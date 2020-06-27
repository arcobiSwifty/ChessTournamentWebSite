from django.db import models
from django.contrib.auth.models import AbstractUser

class Player(AbstractUser):
    following = models.ManyToManyField("Player")
    birth_date = models.DateField(null=True, blank=True)
    confirmed_email = models.BooleanField(default=False)

    online = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Notification(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(Player, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    redirect_url = models.CharField(max_length=100)

    def __str__(self):
        return "%s (%s)" % (self.text, self.user)


