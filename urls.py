"""
URL configuration for prj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from truc import views as core_v
from conf import views as conf_v
from reviewer import views as rev_v
from editchef import views as ed_v
from projet import  views as pr_v
from contact import views as cont_v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls,name="admin" ),
    path("login/", core_v.log_in, name="login"),
    path("inscription/", core_v.inscription, name="inscription"),
    path("profil/", core_v.profil, name="profil"),
    path("",conf_v.conf,name="conf"),
    path('info/<int:id>/',conf_v.info_conf,name="inf-conf"),
    path('postuler/<int:id>/', conf_v.postuler, name='postuler'),
    path('rev/', rev_v.reviewer, name='rev_p'),# display des condidature rev
    path('absrev/<int:id>/', rev_v.detail_article, name='absr'), # reviewer ou accep refuser l'abs
    path('acc/<int:id>/', rev_v.accepterR, name='accepterR'), # reviewer ou accep refuser l'abs
    path('ref/<int:id>/', rev_v.refuserR, name='refuserR'), # reviewer ou accep refuser l'abs
    path('dec/<int:id>/', rev_v.decision, name='deci'), # reviewer ou accep refuser l'abs
    path('edit/', core_v.edit_profil, name='editpro'),
    path('uprev', core_v.up_reviewer, name='uprev'),
    path('logout', core_v.decc, name='decc'),
    path('r1', ed_v.displayEDC1, name='R1'), # edc selection primaire
    path('r2', ed_v.displayEDC2, name='R2'), # distribution
    path('r3', ed_v.displayEDC3, name='R3'),# liste des reviewer
    path('demrev', ed_v.demrev, name='demrev'),# liste des dem reviewer
    path('np', pr_v.form_nvprj, name='prjform'),
    path('accepterC1/<int:id>/', ed_v.accepterC1, name='accepterC1'),# accepter selection
    path('refuserC1/<int:id>/', ed_v.refuserC1, name='refuserC1'),# refuser selection
    path('att/<int:id>', ed_v.attribuer_rev, name='attribuer'),# attribution de reviewer
    path('accrev<int:id>', ed_v.accepterRev, name='accepterRev'),  # attribution de reviewer
    path('refuserev<int:id>', ed_v.refuserRev, name='refuserRev'),  # attribution de reviewer
    path('comconf/<int:id>',conf_v.comconf, name='comconf'),#display co;;
    path('contact/',cont_v.contact, name='about'),#contact de about us 
    path('cnconf/',cont_v.form_conf, name='cnconf'),#contact de about us 
    path('supp/<int:id>',core_v.supp_prj, name='suppP'),#supprimer projet 
    path('detpr/<int:id>',pr_v.detaiprj, name='detpr'),# detail prj (pas encore coller )
    path('editsd',core_v.edit_desc_spe, name='edit_sp_ds'),# modifier spe et description 
    path('modmdp',core_v.mod_mdp, name='mod_mdp'),# modifier mot de passe 
    path('dt/<int:id>',ed_v.detailprj, name='detprjrev'),# detail prj pour reviewer dans edit chef 
    path('arc',conf_v.archive, name='archiveconf'),# archive conf principal 
    path('arc/<int:id>',pr_v.edit_prj, name='changprj'),# modifier prj du detail 
    path('download/<int:prj_id>/', ed_v.download_file, name='download_file'),
    path('addr', ed_v.ajouter_rev, name='addr'),
    path('etat/', core_v.etat_participation, name='etatpar'),
    path('pass/<int:id>',conf_v.articlesp,name='passer'),
    path('supprev/',ed_v.supp_rev,name='supprev'),
    path('supprimer/<int:id>',ed_v.supprimer,name='suprev'),
    path('tester',ed_v.tester,name='tester'),

]
