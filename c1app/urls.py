#c1app.urls.py

from django.conf.urls import url
#from django.urls import path
from django.contrib.auth.views import login, logout
from core import views as core_views
from c1app import views as c1app_views
from c1app.views import ListClientView, MultiRedirectMixin, ClientListView, ClientCreateView, ClientDetailView
#from django.urls import path
from django.views.generic import TemplateView



#from django.contrib import admin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    #url(r'^$', c1app_views.client, name='cuprofile'),
    url(r'^$', core_views.login_redirect, name='login_redirect'),
    url(r'^login/$', login, {'template_name': 'c1app/login.html'}),

    url(r'^logout/$', logout, {'template_name': 'c1app/logout.html'}),
    url(r'^register/$', c1app_views.register, name='register'),
    url(r'^uprofile/$',c1app_views.view_uprofile, name='uprofile'),
    url(r'^uprofile/edit$', c1app_views.edit_uprofile, name='edit_uprofile'),
    url(r'^uprofile/changepassword$', c1app_views.change_password, name='change_password'),
    #url(r'^caseadmin/$', TemplateView.as_view( template_name= 'c1app/clientmanagement.html')),
    ###url(r'^caseadmin/searchclient/$', c1app_views.MultiRedirectMixin.as_view()),
    url(r'^caseadmin/$', c1app_views.clientafterlogin, name='clientafterlogin'),
    #url(r'^caseadmin/$', c1app_views.display_meta, name='clientafterlogin'),
    url(r'^caseadmin/clientprofile/$', c1app_views.edit_cprofile, name='cprofile'),

    url(r'^caseadmin/client_list/', ClientListView.as_view(), name='client_list'),

    url(r'^caseadmin/clientprofile/', ListClientView.as_view(template_name ="searchclient1.html")),

]
