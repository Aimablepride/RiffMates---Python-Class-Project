from django.urls import path
from . import views  # This imports the entire views module

urlpatterns = [
    path('comment/', views.comment, name='comment'),
    path('comment/accepted/', views.comment_accepted, name='comment_accepted'),
    path('ads/', views.ads_list, name='ads_list'),
    path('list_ads/', views.list_ads, name='list_ads'), 
]