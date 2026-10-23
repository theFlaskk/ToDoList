from django.shortcuts import get_object_or_404
from .models import Task

def get_user_task(*, user, task_id):
    """Return a task only if it belongs to the current user."""
    return get_object_or_404(Task, pk=task_id, owner=user)

def create_task(*, user, form):
    """Persist a valid task for its owner."""
    task = form.save(commit=False)
    task.owner = user
    task.full_clean()
    task.save()
    return task
