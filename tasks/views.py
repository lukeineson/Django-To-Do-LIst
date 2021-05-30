from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.contrib import messages

# Create your views here.


class NewTask(forms.Form):
    task = forms.CharField(label="task", widget=forms.TextInput(
        attrs={'class': 'form-control'}))


class RemoveTask(forms.Form):
    remove_task = forms.CharField(label="remove_task", widget=forms.TextInput(
        attrs={'class': 'form-control'}))


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        form = NewTask(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            if task not in request.session["tasks"]:
                request.session["tasks"] += [task]
                return HttpResponseRedirect(reverse('task:index'))
            else:
                messages.add_message(request, messages.INFO,
                                     'Task is already in to do list.')
                return HttpResponseRedirect(reverse('task:index'))

        else:
            return NewTask(request.POST)

    return render(request, "tasks/add.html", {
        "form": NewTask()
    })


def remove(request):
    if request.method == 'POST':
        form = RemoveTask(request.POST)
        if form.is_valid():
            task = form.cleaned_data["remove_task"]
            try:
                request.session["tasks"].remove(task)
                request.session.modified = True
                return HttpResponseRedirect(reverse('task:index'))
            except ValueError:
                messages.add_message(
                    request, messages.ERROR, 'Task not in list')
                return HttpResponseRedirect(reverse('task:index'))
        else:
            return RemoveTask(request.POST)

    return render(request, "tasks/remove.html", {
        "form": RemoveTask()
    })
