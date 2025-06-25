"""
URL configuration for restful01 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('drone-categories/', views.DroneCategoryList.as_view(), name=views.DroneCategoryList.name),
    path('drone-categories/<int:pk>/', views.DroneCategoryDetail.as_view(), name=views.DroneCategoryDetail.name),
    path('drones/', views.DroneList.as_view(), name=views.DroneList.name),
    path('drones/<int:pk>/', views.DroneDetail.as_view(), name=views.DroneDetail.name),
    path('pilots/', views.PilotList.as_view(), name=views.PilotList.name),
    path('pilots/<int:pk>/', views.PilotDetail.as_view(), name=views.PilotDetail.name),
    path('competitions/', views.CompetitionList.as_view(), name=views.CompetitionList.name),
    path('competitions/<int:pk>/', views.CompetitionDetail.as_view(), name=views.CompetitionDetail.name),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]
