from django.shortcuts import render , redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import projet
from truc.models import User

def form_nvprj(request):
    referrer = request.GET.get('referrer', None)
    if request.method == 'POST':
        print('formulaire projet')
        user = request.user
        titre = request.POST['titre']
        abs = request.POST['abs']
        annee = request.POST['annee']
        file = request.FILES['doc']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        co_list = request.POST.getlist('co_auteurs[]')
        nb_co = len(co_list)
        print(nb_co)

        prj = projet.objects.create(auteur_pr=user, titre=titre, annee=annee, resum=abs)

    
        if nb_co > 0:
            if nb_co >= 1 and co_list[0] != '':
            
                
                prj.coaut1 = co_list[0]

            if nb_co >= 2 and co_list[1] != '':
                prj.coaut2 = co_list[1]

            if nb_co >= 3 and co_list[2] != '':

                prj.coaut3 = co_list[2]

        

        
        if file:
            prj.file = file
            prj.save()

    return render(request, 'projform.html', {'referrer': referrer})


def detaiprj(request , id ):
    prj=projet.objects.get(pk=id)
    return render(request,'detaiprj.html', {'prj':prj})



def edit_prj(request,id):
    prj=projet.objects.get(pk=id)
    if request.method == 'POST':
        prj.titre = request.POST.get('titre', prj.titre)
        prj.annee = request.POST.get('annee', prj.annee)
        prj.coaut1 = request.POST.get('co1', prj.coaut1)
        prj.coaut2 = request.POST.get('co2', prj.coaut2)
        prj.coaut3 = request.POST.get('co3', prj.coaut3)
        prj.resum = request.POST.get('abs', prj.resum)
        prj.save()
        return redirect('profil')
    return render(request,'editprjpro.html',{'prj':prj})