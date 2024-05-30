from django.db import models

# Create your models here.

class contacter(models.Model):
    email_contact=models.EmailField()
    object=models.CharField(max_length=200)
    nomE=models.CharField(max_length=200)
    prnom=models.CharField(max_length=200)
    contenu=models.TextField()
