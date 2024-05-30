from django.db import models
from truc.models import User
from conf.models import conference
# Create your models here.
class EditChef(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    conf= models.OneToOneField(conference, on_delete=models.CASCADE)