from django.contrib import admin
from django.urls import include, path
from tasks import views as task_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", task_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("tasks.urls")),
]
