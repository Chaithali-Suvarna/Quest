from django.urls import path
from . import views

urlpatterns = [
    path('', views.adv, name='adv'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('base', views.base, name='base'),
    path('post', views.post, name='post'),
    path('search', views.search, name='search'),
    path('contribution', views.contribution, name='contribution'),
    path('update/<str:pk>/', views.update, name='update'),
    path('delete/<int:id>/', views.delete, name='delete'),
    path('new_search', views.new_search, name='new_search'),

]