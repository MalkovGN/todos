from django.forms import ModelForm

from todo_app.models import ToDo


class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'content', 'important']
