from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone

from todo_app.forms import ToDoForm
from todo_app.models import ToDo


def home(request):
    return render(request, 'todo_app/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo_app/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                    )
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(
                    request,
                    'todo_app/signupuser.html',
                    {'form': UserCreationForm(), 'error': 'This name is already taken, please enter a new!'}
                )
        else:
            return render(
                request,
                'todo_app/signupuser.html',
                {'form': UserCreationForm(), 'error': 'Passwords doesnt match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo_app/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(
                request,
                'todo_app/loginuser.html',
                {'form': AuthenticationForm(), 'error': 'Username and password didnt match'})
        else:
            login(request, user)
            return redirect('currentuser')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo_app/createtodo.html', {'form': ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST)
            new_todo = form.save(commit=False) # Уточнить!
            new_todo.user = request.user
            new_todo.save()
            return redirect('currentuser')
        except ValueError:
            return render(
                request,
                'todo_app/createtodo.html',
                {'form': ToDoForm(), 'error': 'Invalid input. Try again.'}
            )


@login_required
def currentuser(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo_app/currentuser.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo_app/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = ToDoForm(instance=todo) # Уточнить!
        return render(request, 'todo_app/viewtodo.html', {'todo': todo, 'form': form})
    else:
        try:
            form = ToDoForm(request.POST, instance=todo)
            form.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'todo_app/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Bad data'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currentuser')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currentuser')
