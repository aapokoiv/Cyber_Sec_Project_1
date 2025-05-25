from django.urls import path

from .views import homePageView, transferView, viewAccount

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('balance/<str:username>/', viewAccount, name='balance')
]
