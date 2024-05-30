from django.db import models
from conf.models import participer
# Create your models here.


class revoir(models.Model):
    abstract=models.ForeignKey(participer,on_delete=models.CASCADE )
    rev=models.ForeignKey(to='truc.User' ,related_name='rev1_c',on_delete=models.CASCADE,blank=True, null=True)
    decision=models.BooleanField(default=False)
    feedback=models.TextField(blank=True,null=True)
    st=models.IntegerField(default=0)
    def __str__(self):
        return str(self.abstract)
    