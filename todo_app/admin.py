from django.contrib import admin

from todo_app.models import ToDo


class ToDoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(ToDo, ToDoAdmin)
