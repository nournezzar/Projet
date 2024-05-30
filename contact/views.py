from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import *
from conf.models import conference 

# Create your views here.

def contact(request): 
    mess=None
    if request.method=='POST':
        nom=request.POST['nom']
        prnom=request.POST['prnom']
        email=request.POST['email']
        cont=request.POST['message']
        sujet=request.POST['sujet']
        q=contacter.objects.create(email_contact=email,object=sujet,nomE=nom,prnom=prnom,contenu=cont)
        q.save()
        mess="votre message a été envoyer! "

    return render(request,'aboutus.html',{'mess':mess})

def form_conf(request):
    print("dans la fonction")
    subject=None
    message=None
    email=None
    if request.method=='POST':
        print("dans le post ")
        nomc=request.POST['nomc']
        dom=request.POST['dom']
        long=request.POST['long']
        lieu=request.POST['lieu']
        pays=request.POST['pays']
        desc=request.POST['description']
        dateD=request.POST['dateD']
        dateF=request.POST['dateF']
        conf=conference.objects.create(nomc=nomc,domaine=dom,desc=desc,DateD=dateD,DateF=dateF,lieu=lieu,pays=pays,langue=long)
        conf.save()
        #editchef
        nomedit=request.POST['nomchef']
        prenom=request.POST['prechef']
        email=request.POST['email']
        ## email:
        subject = "Notification de soumission de conférence"
        print("on envoie a lui ")
        print(email)
        message = (
                f"Madame/Monsieur {nomedit} {prenom},\n\n"
                f"Nous avons le plaisir de vous informer que la conférence intitulée '{nomc}' a été soumise avec succès sur notre plateforme.\n\n"
                f"En tant qu'éditeur en chef, nous vous invitons à compléter votre inscription sur notre plateforme à l'aide de cette adresse email : {email}. "
                f"Ceci est une étape essentielle pour la validation et la gestion de votre conférence.\n\n"
                "Veuillez suivre les étapes suivantes pour finaliser votre inscription et procéder à l'examen des abstracts soumis par les participants :\n"
                "1. Connectez-vous à notre plateforme via le lien suivant :lien.\n"
                "2. Utilisez cette adresse email pour créer votre compte éditeur en chef.\n"
                "3. Une fois inscrit, on poursuivera la validation\n\n"
                "En tant qu'éditeur en chef, vous aurez également la responsabilité de désigner des reviewers pour l'examen des abstracts. "
                "Nous vous fournirons toute l'assistance nécessaire pour garantir une gestion fluide et efficace de la conférence.\n\n"
                "Nous vous remercions pour la confiance que vous accordez à notre plateforme. "
                "N'hésitez pas à nous contacter pour toute question ou assistance supplémentaire.\n\n"
                "Bien a vous ,\n"
                "Passez une bonne journée\n"
                "L'équipe ICONF\n"
        )

    send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )



    return render(request,'form_conf.html')

