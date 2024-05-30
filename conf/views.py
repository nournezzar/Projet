
from django.shortcuts import render,redirect
from django.db.models import Q
from .models import  *
from truc.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from editchef.models import EditChef 
# Create your views here.
def conf(request):
    #conf=conference.objects.all()
    current_date = date.today()
    conf = conference.objects.filter((Q(DateF__gte=current_date) | Q(DateF__isnull=True)|Q(delai_final__lte=current_date)) & Q(is_approved=True) ) 
    req=request.GET.get('q')
    if req :
        conf=conference.objects.filter(nomc__icontains=req) | \
        conference.objects.filter(pays__icontains=req) | \
        conference.objects.filter(domaine__icontains=req) | \
        conference.objects.filter(desc__icontains=req)


    return render(request,'conf.html',{'conf':conf})

def info_conf(request,id):
    conf=conference.objects.get(id=id)
    return render(request,'info_conf.html' , {'conf':conf})


@login_required
def postuler(request, id):
    user = request.user
    conf = conference.objects.get(id=id)

    if request.method == 'POST':
        print('dans post')
        ap=request.user
        abstract = request.POST['abstract']
        titre=request.POST['titre']
        co_list = request.POST.getlist('co_auteurs[]')
        nb_co = len(co_list)
        print(nb_co)


        par = participer.objects.create(conf=conf, auteur_principal=user, abstract=abstract,titre=titre)

        if nb_co>0 :
            if nb_co >= 1 and co_list[0] != '':
                try:
                    co1 = User.objects.get(email=co_list[0])
                    par.co_auteur1 = co1
                except User.DoesNotExist:

                    messages.error(request, f"Co-auteur {co_list[0]} n'existe pas.")
                    co1=None
            if nb_co >= 2 and co_list[1] != '':
                try:
                    co2 = User.objects.get(email=co_list[1])
                    par.co_auteur2 = co2
                except User.DoesNotExist:

                    messages.error(request, f"Co-auteur {co_list[1]} n'existe pas.")
                    co2 = None
            if nb_co >= 3 and co_list[2] != '':
                try:
                    co3 = User.objects.get(email=co_list[3])
                    par.co_auteur3 = co3
                except User.DoesNotExist:
                    messages.error(request, f"Co-auteur {co_list[2]} n'existe pas.")

                    co3 = None


            if ap.email == getattr(par.co_auteur1, 'email', None) or ap.email == getattr(par.co_auteur2, 'email', None) or ap.email == getattr(par.co_auteur3, 'email', None):
                messages.error(request, 'auteur principal peut pas etre un co auteur ')

        par.save()


    return render(request, 'postuler.html', {'conf': conf, 'user': user})


def comconf(request,id):
    conf=conference.objects.get(id=id)
    chef=None
    rev=conf.reviewers.all()## ca changer  # jai changer 
    pro=participer.objects.filter(conf=conf,decisionrev=True)

    return render(request, 'comconf.html',{'chef':chef, 'rev':rev, 'conf':conf, 'pro':pro})



def articlesp(request , id ):
    conf=conference.objects.get(pk=id)
    par=participer.objects.filter(conf=conf,decisionrev=True)
    return render(request,'articlesp.html',{'par':par})


def archive(request):
    current_date = date.today()
    conf=conference.objects.filter(DateF__lte=current_date)
    chef=EditChef.objects.all()
    

    return render(request,'archiveconf.html',{'conf':conf , 'editc':chef } )