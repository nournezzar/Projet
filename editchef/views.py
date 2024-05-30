from django.shortcuts import render , redirect
from .models import EditChef
from django.core.mail import send_mail
from conf.models import *
from django.conf import settings
from truc.models import *
from reviewer.models import*
from projet.models import *
from django.db.models import Min, Max
from numpy import random
from django.contrib.auth.decorators import login_required
from editchef.model import ArticleClassifier
# Create your views here.

# toutes les participations
@login_required
def displayEDC1(request):
    user=request.user
    ed=EditChef.objects.get(user=user)
    conf=ed.conf
    par=participer.objects.filter(conf=conf ,v=False)
    return render(request,'RedC1.html',{'par':par})
@login_required
def accepterC1(request,id):
    par=participer.objects.get(id_abstract=id)
    par.acc=True
    par.v=True
    par.save()
    return redirect('R1')


@login_required
def refuserC1(request, id):
    par = participer.objects.get(id_abstract=id)
    par.v=True
    par.save()
    ap = par.auteur_principal

    send_mail(
        'Résultat de participation',
        'Bonjour,\n\n Nous espérons que cette note vous trouve bien. Nous tenons à vous informer des résultats de la première sélection des propositions pour notre conférence ' + par.conf.nomc + '. Après un examen attentif de toutes les soumissions, nous sommes désolés de vous informer que votre proposition n a pas été retenue pour la prochaine étape du processus de sélection. Veuillez noter que ce rejet ne signifie pas nécessairement que votre proposition n était pas de qualité. Nous avons reçu un grand nombre de soumissions, et malheureusement, nous ne pouvons pas inclure toutes les propositions dans le programme final. Nous vous remercions de votre intérêt pour notre conférence et de votre contribution à notre processus de sélection. Nous vous encourageons à continuer à vous engager dans votre domaine et à participer à d autres événements à l avenir ',
        'settings.EMAIL_HOST_USER',
        [ap.email],
        fail_silently=False,
    )
    return redirect('R1')

#display des article qui ont ete selection:
@login_required
def displayEDC2(request):
    user = request.user
    ed = EditChef.objects.get(user=user)
    conf = ed.conf
    par = participer.objects.filter(conf=conf,acc=True,affecter=False)
    return render(request,'RedC2.html' ,{'par':par})


@login_required
def attribuer_rev(request , id):
    user = request.user
    ed = EditChef.objects.get(user=user)
    par = participer.objects.get(id_abstract=id)
    auteur=[par.auteur_principal,par.co_auteur1,par.co_auteur2,par.co_auteur3]
    conf = ed.conf
    nbrev = User.objects.filter(conferences=conf).count()# j'ai changer 
    nbabst = participer.objects.filter(conf=conf).count()
    x = (nbabst / nbrev) + 2
    nbrev = User.objects.filter(conferences=conf, reviewer=True).order_by('id')# ca change !!!! j'ai changer!!!!!
    reviewer_id= list(nbrev.values_list('id', flat=True))
    nombre_rev=len(reviewer_id)
    print("nombre des reviewers ")
    print(nombre_rev)
    classifier = ArticleClassifier()  
    reviewers = classifier.classify(par.abstract,nombre_rev)
    cpt=0
    for index in reviewers:
        X= reviewer_id[index]
        try:
            review = User.objects.get(id=X)
            if review not in auteur:
                if  review.nba < x:
                    review.nba += 1
                    review.save()
                    par.affecter = True
                    par.save()
                    rr = revoir.objects.create(abstract=par, rev=review)
                    rr.save()
                    cpt+=1
                    if cpt==2:
                        break 

        except User.DoesNotExist:
            pass

    return redirect('R2')

@login_required
def displayEDC3(request):
    user=request.user
    chef=EditChef.objects.get(user=user)
    conf=chef.conf
    pr= participer.objects.filter(conf=conf)
    revoirs=revoir.objects.filter(abstract__conf=conf)

    return render(request,'RedC3.html',{'pr':pr ,'revoirs':revoirs})

@login_required
def demrev(request):
    user = request.user
    chef = EditChef.objects.get(user=user)
    conf = chef.conf
    dem=demande_rev.objects.filter(conf=conf,vu=False)
    dem_rev=[]
    for dem in dem : 
        prj=projet.objects.filter(auteur_pr=dem.user)
        dem_rev.append(
            
            {'dem':dem,'prj':prj}
            )
    print("dem rev")
    print(dem_rev)
    return render(request,'demrev.html',{'dem_rev':dem_rev})


# gestion des demandes des reviewers :
@login_required
def accepterRev(request , id):
    demande= demande_rev.objects.get(id=id)
    demande.deci=True
    print(demande.user)
    print(demande.user.reviewer)
    demande.user.reviewer=True
    print(demande.user.reviewer)
    demande.user.desc= demande.desctext
    chef = EditChef.objects.get(user=request.user)
    demande.user.conferences.add(chef.conf) ## change !! j'ai changer
    demande.vu=True
    demande.save()
    demande.user.save()
    object_email = 'resultat de la demande'
    corps_email = 'corps accepter demande'
    send_mail(object_email,
              corps_email,
              'settings.EMAIL_HOST_USER',
              [request.user],
              fail_silently=True)
    return redirect('demrev')


@login_required
def refuserRev(request , id):
    demande= demande_rev.objects.get(id=id)
    demande.deci=False
    chef = EditChef.objects.get(user=request.user)
    print(demande.user)
    print(demande.user.reviewer)
    demande.vu=True
    demande.save()
    demande.user.save()
    object_email='resultat de la demande'
    corps_email='corps refuser demande'
    send_mail(object_email,
              corps_email,
              'settings.EMAIL_HOST_USER',
              [request.user],
              fail_silently=True)
    return redirect('demrev')



# detail prj rev demande 
def detailprj(request ,id ): 
    prj=projet.objects.get(pk=id)
    return render(request,'detailprj_rev.html',{'prj':prj})


from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import smart_str


def download_file(request, prj_id):
    prj = get_object_or_404(projet, pk=prj_id)
    if prj.file:
        file_path = prj.file.path
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename=' + smart_str(prj.file.name)
            return response
    else:
        return HttpResponse("le fichier n'existe pas ")
    

# vue pour ajouter un reviewer 

def ajouter_rev(request):
    mess=None
    obj=None
    conf=request.user.conf
    if request.method=='POST':
        nom=request.POST['nom']
        prnom=request.POST['prnom']
        email=request.POST['email']
        try: 
            rev=User.objects.get(email=email)
            if rev.reviewer==False:
                rev.reviewer=True
                rev.conferences.add(conf)
                rev.save()
            mess=f"{nom} {prnom} a été ajouter comme un reviewer de votre conference "
        except : 
            mess="cette utilisateur n'est pas enregistrer dans le systeme un email d'invitation lui a été envoyé "
            message = (
                f"Madame/Monsieur {nom} {prnom},\n\n"
                f"Nous avons le plaisir de vous annoncer que vous avez ete choisi pour etre reviewer conference {conf} "
                f"Pour le faire veuillez crée un compte dans notre platforme puis contacter l'editeur en chef via son mail{request.user.email}"
                "N'hésitez pas à nous contacter pour toute question ou assistance supplémentaire.\n\n"
                "Bien a vous ,\n"
                "Bonne journée\n"
                "L'équipe ICONF\n"
                )
            obj="Recrutement pour devenir reviewer"
            send_mail(
                obj,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
    
    return render(request,'ajouter_rev_ec.html',{'mess':mess})

def supp_rev(request): 
    ed=EditChef.objects.get(user=request.user)
    Rev=User.objects.filter(reviewer=True,conferences=ed.conf)
    return render(request,'supprev.html',{'rev':Rev})


def supprimer(request,id):
    rev=User.objects.get(pk=id)
    ed=EditChef.objects.get(user=request.user)
    rev.conferences.remove(ed.conf)
    return redirect('supprev')

def ajouter_rev(request):
    mess=None
    messEX=None
    obj=None
    ec=EditChef.objects.get(user=request.user)
    conf=ec.conf
    if request.method=='POST':
        nom=request.POST['nom']
        prnom=request.POST['prnom']
        email=request.POST['email']
        try: 
            rev=User.objects.get(email=email)
            if rev.reviewer==False:
                rev.reviewer=True
            if conf not in rev.conferences.all() :
                rev.conferences.add(conf)
                rev.save()
                messEX=f"{nom} {prnom} a été ajouter comme un reviewer de votre conference ,un mail d'information lui a été envoyer"
            else : 
                mess="Ce reviewer est deja associé a votre conference " 
           
            
        except : 
            mess="cette utilisateur n'est pas enregistrer dans le systeme un email d'invitation lui a été envoyé "
            message = (
                f"Madame/Monsieur {nom} {prnom},\n\n"
                f"Nous avons le plaisir de vous annoncer que vous avez ete choisi pour etre reviewer conference {conf} "
                f"Pour le faire veuillez crée un compte dans notre platforme puis contacter l'editeur en chef via son mail{request.user.email}"
                "N'hésitez pas à nous contacter pour toute question ou assistance supplémentaire.\n\n"
                "Bien a vous ,\n"
                "Bonne journée\n"
                "L'équipe ICONF\n"
                )
            obj="Recrutement pour devenir reviewer"
            send_mail(
                obj,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
  
    return render(request,'ajouter_rev_ec.html',{'mess':mess,'messEX':messEX})




def tester(request):
    user=request.user
    chef=EditChef.objects.get(user=user)
    conf=chef.conf
    pr= participer.objects.filter(conf=conf,affecter=True)
    par_rev=[]
    for par in pr : 
        rev=revoir.objects.filter(abstract=par)
        par_rev.append(
            {'pr':par , 'rev':rev}
        )
    print("par rev")
    print(par_rev)

    return render(request,'attr.html' ,{'par_rev':par_rev})