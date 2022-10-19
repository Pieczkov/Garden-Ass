"""garden URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from garden_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index_view'),
    path('home/', views.HomeView.as_view(), name='base_view'),
    path('add_unit/', views.AddUnitView.as_view(), name='add_unit'),
    path('add_type/', views.AddPlantTypeView.as_view(), name='add_type'),
    path('plant_list', views.PlantListView.as_view(), name='plant_list'),
    path('add_plant', views.AddPlantView.as_view(), name='add_plant'),
    path('add_task', views.AddTaskView.as_view(), name='add_task'),
    path('task_list', views.TaskListView.as_view(), name='task_list'),
    path('add_plan', views.AddPlanOfWorkView.as_view(), name='add_plan'),
    path('plan_list', views.PlanOfWorkListView.as_view(), name='plan_list'),
    path('task_view/<int:task_id>/', views.TaskView.as_view(), name='task_view'),
    path('plan_view/<int:plan_id>/', views.PlanView.as_view(), name='plan_view'),
    path('task_view/delete/<int:task_id>/', views.TaskDelete.as_view(), name='delete_task'),
    path('plan_view/delete/<int:plan_id>/', views.PlanDelete.as_view(), name='delete_plan'),
    path('plant_list/delete/<int:plant_id>/', views.PlantDelete.as_view(), name='delete_plant'),
    path('plant_list/update/<int:pk>/', views.EditPlantView.as_view(), name='edit_plant'),



    path('register_user/', views.CreateUserView.as_view(), name='register_user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('main/', views.MainPageView.as_view(), name='main_page')
]
