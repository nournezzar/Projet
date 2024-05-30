from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import revoir
from django.core.mail import send_mail
from django.conf import settings
from truc.models import User
# Create your views here.


# le display des participant 
@login_required
def reviewer(request):
    user=request.user
    conf=user.conferences.all()
    art=revoir.objects.filter(rev=user ,feedback__isnull=True)
    return render(request,'reviewer.html',{'art':art , 'conf':conf})


@login_required
def detail_article(request, id):
    rev=revoir.objects.get(id=id)
    print(rev.abstract.auteur_principal)
    return render(request,'rev_abs.html', {'rev':rev})


@login_required
def accepterR(request,id):
    print("dans accepter")
    print(id)
    rev=revoir.objects.get(id=id)
    fdbk=''
    if request.method== 'POST':
        fdbk=request.POST['feedback']
        print("apres post et le feed back est : ")
        print(fdbk)
        rev.feedback=fdbk 
    rev.acc=True
    rev.save()
    recevoir=User.objects.get(id=rev.abstract.auteur_principal.id)
    send_mail(
        'Résultat de participation',
        f'Bonjour,\n\nCe que je veux dire: {fdbk}',
        'settings.EMAIL_HOST_USER',
        [recevoir.email],
        fail_silently=True,
    )
    return redirect('rev_p')

    

@login_required
def refuserR(request,id): 
    print("dans refuser")
    rev=revoir.objects.get(id=id)
    if request.method=='POST':
        fdbk=request.POST['feedback']
    rev.feedback=fdbk 
    rev.acc=False
    rev.save()
    send_mail(
        'Résultat de participation',
        f'Bonjour,\n\nCe que je veux dire: {fdbk}',
        'settings.EMAIL_HOST_USER',
        [rev.abstract.auteur_principal],
        fail_silently=True,
    )
    return redirect('rev_p')


def test(par): 
    print("dans le teste")
    revs = revoir.objects.filter(abstract=par)
    fdbk = []
    for rev in revs:
        fdbk.append(rev.feedback)
    tr=all(feedback is not None for feedback in fdbk)
    if tr == True :
        print("les deux sont la ")
        dess = []
        for rev in revs:
            dess.append(rev.decision)
        par.status=True
        par.decisionrev=any(dess)
        par.save()



 


@login_required
def decision(request , id):
    rev=revoir.objects.get(id=id)
    if request.method=='POST':
        action = request.POST.get('action')
        fdbk=request.POST['feedback']
        rev.feedback=fdbk
        recevoir=User.objects.get(id=rev.abstract.auteur_principal.id)
        if action=='accept':
            rev.decision=True
            rev.save()
            test(rev.abstract)
            send_mail(
        'Résultat de participation',
        f'Bonjour,\n\n feedback {fdbk}',
        'settings.EMAIL_HOST_USER',
        [rev.abstract.auteur_principal.email],
        fail_silently=True,
            )

        elif action=='refuse':
            rev.decision=False
            rev.save()
            test(rev.abstract)
            rev.save()
            send_mail(
        'Résultat de participation',
        f'Bonjour,\n\n nous somme navré : {fdbk}',
        'settings.EMAIL_HOST_USER',
        [rev.abstract.auteur_principal.email],
        fail_silently=True,
            )   
        

    return render(request,'rev_abs.html', {'rev':rev})



