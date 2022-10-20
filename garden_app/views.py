from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView

from garden_app.forms import CreateUserForm, LoginForm, AddPlantForm, AddTaskForm, AddPlanOfWorkForm
from garden_app.models import Unit, PlantType, Plant, Task, PlanOfWork


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


class HomeView(View):
    def get(self, request):
        return render(request, 'base.html')


class AddUnitView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "forms/add_unit.html")

    def post(self, request):
        name = request.POST["name"]
        try:
            if Unit.objects.get(name=name) is not None:
                return render(request, "forms/add_unit.html", {"message": "This unit already exist"})
        except:
            Unit.objects.create(name=name)
        return redirect("plant_list")


class AddPlantTypeView(LoginRequiredMixin, View):
    def get(self, request):

        return render(request, "forms/add_plant_type.html")

    def post(self, request):
        name = request.POST["name"]
        try:
            if PlantType.objects.get(name=name) is not None:
                return render(request, "forms/add_plant_type.html", {"message": "This kind of plant already exists"})
        except:
            PlantType.objects.create(name=name)
            return redirect("plant_list")


class AddPlantView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPlantForm()
        return render(request, "forms/add_plant_form.html", {"form": form})

    def post(self, request):
        form = AddPlantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("add_task")
        return render(
            request,
            "forms/add_plant_form.html",
            {"form": form, "message": "Failed to add please fill in the form again"},
        )


class EditPlantView(LoginRequiredMixin, UpdateView):
    model = Plant
    # fields = ['name', 'species', 'description', 'amount', 'unit', 'type']
    form_class = AddPlantForm
    template_name = "forms/plant_update_form.html"
    # inaczej mamy blad circular import
    success_url = reverse_lazy("plan_list")


class PlantListView(View):
    def get(self, request):
        wiki_base_url = "https://pl.wikipedia.org/w/index.php"
        plant_list = Plant.objects.all().order_by("type__name")
        paginator = Paginator(plant_list, 10)
        page = request.GET.get('page')
        plants = paginator.get_page(page)
        return render(request, "plant_list.html", {"plants": plants, "wiki_base_url": wiki_base_url})


class PlantDelete(LoginRequiredMixin, View):
    def get(self, request, plant_id):
        plant_to_delete = Plant.objects.get(id=plant_id)
        plant_to_delete.delete()
        return redirect("plant_list")


class AddTaskView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddTaskForm()
        return render(request, "forms/add_task_form.html", {"form": form})

    def post(self, request):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("plan_list")
        return render(
            request,
            "forms/add_task_form.html",
            {"form": form, "message": "Failed to register please fill in the form again"},
        )


class TaskListView(View):
    def get(self, request):
        task_list = Task.objects.all().order_by('plant')
        paginator = Paginator(task_list, 10)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
        return render(request, "task_list.html", {"tasks": tasks})


class TaskView(View):
    def get(self, request, task_id):
        task = Task.objects.get(id=task_id)
        return render(request, "task_info.html", {"task": task})


class EditTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = AddTaskForm
    template_name = "forms/task_update_form.html"
    success_url = reverse_lazy("task_list")


class TaskDelete(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task_to_delete = Task.objects.get(id=task_id)
        task_to_delete.delete()
        return redirect("task_list")


class AddPlanOfWorkView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPlanOfWorkForm()
        return render(request, "forms/add_plan_of_work.html", {"form": form})

    def post(self, request):
        form = AddPlanOfWorkForm(request.POST)
        if form.is_valid():
            plan = form.save()
            for i in form.cleaned_data["task"]:
                plan.task_set.add(i)
            plan.save()
            return redirect("plan_list")
        return render(
            request,
            "forms/add_plan_of_work.html",
            {"form": form, "message": "Failed to register please fill in the form again"},
        )


class PlanView(View):
    def get(self, request, plan_id):
        plan = PlanOfWork.objects.get(id=plan_id)
        return render(request, "plan_info.html", {"plan": plan})


class PlanOfWorkListView(View):
    def get(self, request):
        plan_list = PlanOfWork.objects.all().order_by("date")
        paginator = Paginator(plan_list, 10)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        return render(request, "plan_list.html", {"plans": plans})

## do poprawy nie dziła dodawnie do bazy taskow jak sie mozna bylo spodziewc
class EditPlanView(LoginRequiredMixin, UpdateView):
    model = PlanOfWork
    form_class = AddPlanOfWorkForm
    # fields = ["name", "description", "date"]
    template_name = "forms/plan_update_form.html"
    success_url = reverse_lazy("plan_list")

class AddTaskToPlanView(View):
    def post(self, request):
        task_to_add = Task.objects.all()
        return render(request, 'forms/add_plan_of_work.html', {"task_to_add": task_to_add})

class PlanDelete(LoginRequiredMixin, View):
    def get(self, request, plan_id):
        plan_to_delete = PlanOfWork.objects.get(id=plan_id)
        plan_to_delete.delete()
        return redirect("plan_list")


class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, "forms/register_user_form.html", {"form": form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password1"]
            user.username = form.cleaned_data["username"]
            user.set_password(password)
            user.save()
            return redirect("login")
        return render(request, "forms/register_user_form.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "forms/login_form.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
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
