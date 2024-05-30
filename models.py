from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    reviewer = models.BooleanField(default=False)
    #r_conf=models.ForeignKey(to='conf.conference',on_delete=models.CASCADE,blank=True, null=True)
    conferences = models.ManyToManyField('conf.conference', related_name='user_reviewers', blank=True)    
    editc = models.BooleanField(default=False)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    spe = models.CharField(max_length=100)

    desc = models.CharField(max_length=255)
    nba=models.IntegerField(default=0)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.nom + " " + self.prenom

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, appl_label):
        return True



class demande_rev(models.Model):
    conf=models.ForeignKey(to='conf.conference',on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    desctext=models.TextField()
    deci=models.BooleanField(default=False)
    vu=models.BooleanField(default=False)
