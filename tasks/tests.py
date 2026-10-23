from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Task

User = get_user_model()

class TaskAccessTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="alice", password="Test-pass-123!")
        self.other = User.objects.create_user(username="bob", password="Test-pass-123!")
        self.task = Task.objects.create(owner=self.owner, title="Моя задача")

    def test_user_sees_only_own_tasks(self):
        self.client.login(username="bob", password="Test-pass-123!")
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Моя задача")

    def test_user_cannot_edit_another_users_task(self):
        self.client.login(username="bob", password="Test-pass-123!")
        response = self.client.get(reverse("task_edit", args=[self.task.pk]))
        self.assertEqual(response.status_code, 404)

    def test_task_creation_requires_login(self):
        response = self.client.get(reverse("task_create"))
        self.assertEqual(response.status_code, 302)
