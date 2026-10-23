from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task
from .services import get_user_task, create_task


def signup(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Аккаунт создан. Добро пожаловать!")
        return redirect("task_list")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).select_related("category")
    status = request.GET.get("status", "")
    query = request.GET.get("q", "").strip()
    if status in Task.Status.values:
        tasks = tasks.filter(status=status)
    if query:
        tasks = tasks.filter(title__icontains=query)
    return render(request, "tasks/task_list.html", {
        "tasks": tasks, "selected_status": status, "query": query,
        "statuses": Task.Status.choices,
    })


@login_required
def task_create(request):
    form = TaskForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        create_task(user=request.user, form=form)
        messages.success(request, "Задача создана.")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Новая задача"})


@login_required
def task_edit(request, task_id):
    task = get_user_task(user=request.user, task_id=task_id)
    form = TaskForm(request.POST or None, instance=task, user=request.user)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        updated.full_clean()
        updated.save()
        messages.success(request, "Изменения сохранены.")
        return redirect("task_list")
    return render(request, "tasks/task_form.html", {"form": form, "page_title": "Редактировать задачу"})


@login_required
@require_POST
def task_delete(request, task_id):
    task = get_user_task(user=request.user, task_id=task_id)
    task.delete()
    messages.success(request, "Задача удалена.")
    return redirect("task_list")


@login_required
@require_POST
def task_toggle_done(request, task_id):
    task = get_user_task(user=request.user, task_id=task_id)
    task.status = Task.Status.TODO if task.status == Task.Status.DONE else Task.Status.DONE
    task.save(update_fields=["status", "updated_at"])
    return redirect("task_list")
