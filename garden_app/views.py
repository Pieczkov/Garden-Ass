from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from garden_app.forms import CreateUserForm, LoginForm, AddPlantForm, AddTaskForm, AddPlanOfWorkForm
from garden_app.models import Unit, PlantType, Plant, Task, PlanOfWork


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class HomeView(View):
    def get(self, request):
        # odowlo=anie api
        # wrzucic kontekstu
        return render(request, 'base.html')


class AddUnitView(View):
    def get(self, request):
        return render(request, 'forms/add_unit.html')

    def post(self, request):
        name = request.POST['name']
        try:
            if Unit.objects.get(name=name) is not None:
                return render(request, 'forms/add_unit.html', {'message': 'This unit already exist'})
        except:
            Unit.objects.create(name=name)
        return redirect('plant_list')


class AddPlantTypeView(View):
    def get(self, request):

        return render(request, 'forms/add_plant_type.html')

    def post(self, request):
        name = request.POST['name']
        try:
            if PlantType.objects.get(name=name) is not None:
                return render(request, 'forms/add_plant_type.html', {'message': 'This kind of plant already exists'})
        except:
            PlantType.objects.create(name=name)
            return redirect('plant_list')


class AddPlantView(View):
    def get(self, request):
        form = AddPlantForm()
        return render(request, 'forms/add_plant_form.html', {'form': form})

    def post(self, request):
        form = AddPlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_task')
        return render(request, 'forms/add_plant_form.html', {
            'form': form, 'message': "Failed to add please fill in the form again"})


class PlantListView(View):
    def get(self, request):
        wiki_base_url = "https://pl.wikipedia.org/w/index.php"
        plants = Plant.objects.all().order_by('type__name')
        return render(request, 'plant_list.html', {'plants': plants, "wiki_base_url": wiki_base_url})


class PlantDelete(View):
    def get(self, request, plant_id):
        plant_to_delete = Plant.objects.get(id=plant_id)
        plant_to_delete.delete()
        return redirect('plant_list')


class AddTaskView(View):
    def get(self, request):
        form = AddTaskForm()
        return render(request, 'forms/add_task_form.html', {'form': form})

    def post(self, request):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
        return render(request, 'forms/add_task_form.html', {
            'form': form, 'message': "Failed to register please fill in the form again"})


class TaskListView(View):
    def get(self, request):
        task_list = Task.objects.all()
        return render(request, 'task_list.html', {'tasks': task_list})


class TaskView(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, 'task_info.html', {'task': task})


class TaskDelete(View):
    def get(self, request, task_id):
        task_to_delete = Task.objects.get(id=task_id)
        task_to_delete.delete()
        return redirect('task_list')


class AddPlanOfWorkView(View):
    def get(self, request):
        form = AddPlanOfWorkForm()
        return render(request, 'forms/add_plan_of_work.html', {'form': form})

    def post(self, request):
        form = AddPlanOfWorkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('plan_list')
        return render(request, 'forms/add_plan_of_work.html', {
            'form': form, 'message': "Failed to register please fill in the form again"})


class PlanView(View):
    def get(self, request, plan_id):
        plan = PlanOfWork.objects.get(id=plan_id)
        return render(request, 'plan_info.html', {'plan': plan})


class PlanOfWorkListView(View):
    def get(self, request):
        plans = PlanOfWork.objects.all().order_by('date')
        return render(request, 'plan_list.html', {'plans': plans})


class AddTaskToPlanView(View):
    def post(self, request):
        task_to_add = Task.objects.all()
        return render(request, 'forms/add_plan_of_work.html', {"task_to_add": task_to_add})

    def get(self, request, plan_id):
        task_name = request.POST.get('task_name')




class PlanDelete(View):
    def get(self, request, plan_id):
        plan_to_delete = PlanOfWork.objects.get(id=plan_id)
        plan_to_delete.delete()
        return redirect('plan_list')









class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'forms/register_user_form.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.username = form.cleaned_data['username']
            user.set_password(password)
            user.save()
            return redirect('login')
        return render(request, 'forms/register_user_form.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'forms/login_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("base_view")
            else:
                return HttpResponse("Login error")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")
