from django.db import models

# Create your models here.
from django.db import models
from truc.models import User


# Create your models here.

class conference(models.Model):
    nomc= models.CharField(max_length=100)
    domaine=models.CharField(max_length=100)
    desc= models.TextField()
    DateD=models.DateField(blank=True, null=True)
    DateF=models.DateField(blank=True, null=True)
    delai_final=models.DateField(blank=True, null=True)
    lieu=models.CharField(max_length=100 ,blank=True, null=True)
    pays=models.CharField(max_length=100)
    langue=models.CharField(max_length=200 ,blank=True, null=True)
    prs=models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    reviewers = models.ManyToManyField('truc.User', related_name='conference_reviewers', blank=True,null=True)

    def __str__(self):
        return self.nomc

class participer(models.Model):
    id_abstract=models.AutoField(primary_key=True)
    conf=models.ForeignKey(conference,on_delete=models.CASCADE)
    auteur_principal=models.ForeignKey(User,on_delete=models.CASCADE)
    co_auteur1=models.ForeignKey(User,related_name='core_co1',on_delete=models.CASCADE,blank=True, null=True)
    co_auteur2=models.ForeignKey(User,related_name='core_co2',on_delete=models.CASCADE,blank=True, null=True)
    co_auteur3=models.ForeignKey(User,related_name='core_co3',on_delete=models.CASCADE,blank=True, null=True)
    abstract=models.TextField()
    acc=models.BooleanField(default=False)# edit chef
    v=models.BooleanField(default=False)# edit chef
    affecter=models.BooleanField(default=False)#test si affecter 
    status=models.BooleanField(default=False)# status du traitement 
    decisionrev=models.BooleanField(default=False)
    titre=models.CharField(max_length=200 ,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) # ajouter lui pour garder temps et faire un ordre LIFO 

    class Meta:
        ordering = ['-created_at'] 
    def __str__(self):
        return str(self.titre)
    