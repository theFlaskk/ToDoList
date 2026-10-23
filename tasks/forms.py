from django import forms
from .models import Category, Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "category", "status", "priority", "due_date"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(owner=user)
        self.fields["title"].widget.attrs.update({"placeholder": "Например, подготовить презентацию"})

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Введите название задачи.")
        if len(title) > 200:
            raise forms.ValidationError("Максимум 200 символов.")
        return title
