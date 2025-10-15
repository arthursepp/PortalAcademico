from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('portal/', views.portal, name='portal'),
    path('logout/', views.logout_view, name='logout'),
    path('__reload__/', include('django_browser_reload.urls')),
]