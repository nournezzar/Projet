from django.db import models
from truc.models import User
# Create your models here.

class projet(models.Model):
    auteur_pr=models.ForeignKey(User,on_delete=models.CASCADE)
    titre=models.CharField(max_length=80)
    annee=models.IntegerField()
    #coaut1 = models.ForeignKey(User,related_name='aut1',  on_delete=models.CASCADE, blank=True, null=True)
    #coaut2 = models.ForeignKey(User, related_name='aut2', on_delete=models.CASCADE, blank=True, null=True)
    #coaut3 = models.ForeignKey(User, related_name='aut3', on_delete=models.CASCADE, blank=True, null=True)
    coaut1=models.CharField(max_length=200,blank=True,null=True)
    coaut2=models.CharField(max_length=200,blank=True,null=True)
    coaut3=models.CharField(max_length=200,blank=True,null=True)
    resum=models.TextField()
    file=models.FileField(blank=True, null=True)
    


    