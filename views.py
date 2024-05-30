from django.shortcuts import render , redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .bck import CaseInsensitiveModelBackend
from .models import *
from projet.models import *
from conf.models import conference , participer
from reviewer.models import revoir
from django.http import JsonResponse
backend='django.contrib.auth.backends.AllowAllUsersModelBackend'

def inscription(request):
    if request.user.is_authenticated:
        return redirect('profil')
    if request.method =='POST':
        if request.method == 'POST':
            nom = request.POST['nom']
            prenom = request.POST['prenom']
            spe = request.POST['spe']
            email = request.POST['email']
            mdp = request.POST['mdp']
            mdp1 = request.POST['mdp1']

            if mdp != mdp1:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return redirect('inscription')
            mdp = make_password(mdp)
            user = User.objects.create(nom=nom, prenom=prenom, spe=spe, email=email, password=mdp)
            user.save()
            return redirect('login')

    return render(request,'insctription.html')


def log_in(request):
    if request.user.is_authenticated:
        return redirect('profil')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('mdp')
        b = CaseInsensitiveModelBackend()

        user =  b.authenticate(request, email=email, password=password, backend='truc.bck.CaseInsensitiveModelBackend')
        print(user)
        if user is not None:
            login(request, user ,backend='django.contrib.auth.backends.AllowAllUsersModelBackend')
            next_url = request.GET.get('next')
            if user.reviewer== True:
                return redirect('rev_p')
            if user.editc== True :
                return redirect('R1')
            
            

            if next_url:
                return redirect(next_url)

            else:
                return redirect('profil')
        else:
            messages.error(request, 'email ou mot de passe invalid')

    return render(request, 'connecter.html')


def decc(request):
    logout(request)
    return redirect('conf')


@login_required
def profil(request):
        referrer = request.GET.get('referrer', None)
        user=request.user
        prj=projet.objects.filter(auteur_pr=user)
        return render(request, 'profil.html', {'user': user , 'prj':prj ,'referrer': referrer})


@login_required
def edit_profil(request):
    return render(request,'edit profil.html')

@login_required
def up_reviewer(request):
    conflist = conference.objects.all()
    user=request.user
    conf0=user.conferences.all()
    X=demande_rev.objects.filter(user=user,vu=False)
    conf= [demande.conf for demande in X]
    conff = list(conf0) + conf
    conff = list(set(conff))
    msg = None
    errP=None

    if request.method == 'POST':
        
        nomc = request.POST['confc']
        confc = conference.objects.get(nomc=nomc)
        try:
            pr = demande_rev.objects.get(user=user, conf=confc)
            #if pr.vu == True :
            msg = "Votre demande est en cours de traitement. Un e-mail de réponse vous sera envoyé dès que la décision sera prise."
        except demande_rev.DoesNotExist:
            prr=projet.objects.filter(auteur_pr=user).count()
            if prr<5:
                errP=f"Pour postuler il faut presenter au moins vos 5 projets les plus recent \n vous en avez {prr} \n rajoutez en {5-prr}  "
            else :
                desc = request.POST.get('desc')
                demande = demande_rev.objects.create(user=user, conf=confc, desctext=desc)
                demande.save()
                return redirect('profil')
    return render(request, 'reviewer-form.html', {'conflist': conflist, 'msg': msg,'errP':errP,'conff':conff})

# projects/views.py


# action de suppression du prj 
def supp_prj(request, id):
    
    project = projet.objects.get(pk=id)
    project.delete()
    return redirect('profil')


def edit_desc_spe(request): 
    user=request.user
    
    if request.method =='POST':
        user.spe=request.POST['speciality']
        description = request.POST.get('description', '')
        print("desc : ")
        print(description)
        print("apres le strip")
        print(description.strip())

        if description.strip():
            user.desc = description
        user.save()
        return redirect('profil')

    return render(request,'editpr_sp_ds.html' , {'user':user})

def mod_mdp(request):
    return render(request,'modif_mdp.html')

@login_required
def etat_participation(request):
    user=request.user
    part=participer.objects.filter(auteur_principal=user)
    #revue = revoir.objects.all()
    part_revue=[]
    for part in part : 
        revue=revoir.objects.filter(abstract=part)
        part_revue.append({'part':part,'revue':revue})
    return render(request,'etatdemande.html',{'part_revue':part_revue})