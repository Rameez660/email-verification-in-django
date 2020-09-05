from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path,re_path
urlpatterns = [
    # path('', views.signup),
    path('signup/', views.signup, name='signup'),
    path('login/',views.handlelogin,name="handlelogin"),
    path('student/', views.student, name='student'),

    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate,name='activate'),]
