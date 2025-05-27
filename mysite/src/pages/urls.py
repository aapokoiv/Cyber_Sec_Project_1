from django.urls import path

from .views import homePageView, transferView, viewAccount, userSearchView, addCard

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('balance/<str:username>/', viewAccount, name='balance'),
    path('search/', userSearchView, name='search'),
    path('addCard/', addCard, name='add_card')

]
