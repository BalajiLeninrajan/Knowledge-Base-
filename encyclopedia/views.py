from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from random import choice

from markdown2 import markdown
from . import util


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "search",
            "placeholder": "Search Encyclopedia"
        }),
        label=""
    )


class EditForm(forms.Form):
    text = forms.CharField(
        label="",
        widget=forms.Textarea()
    )


class NewEntryForm(forms.Form):
    title = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            "placeholder": "Title",
        })
    )
    text = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            "placeholder": "Text",
        })
    )


def index(request):
    return render(request, "encyclopedia/index.html", {
        "search": SearchForm(),
        "entries": util.list_entries()
    })


def entry_page(request, title):
    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "search": SearchForm(),
            "title": title,
            "entry": markdown(entry)
        })

    return render(request, "encyclopedia/error.html", {
        "search": SearchForm(),
        "error": "Page not found",
    })


def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        form = SearchForm(request.POST)

        if form.is_valid():
            query = form.cleaned_data["query"]

            if query in entries:
                return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[query]))

            results = [entry for entry in entries if query in entry]
            return render(request, "encyclopedia/search.html", {
                "search": SearchForm(),
                "entries": results
            })

        else:
            return render(request, "encyclopedia/error.html", {
                "search": SearchForm(),
                "error": "Invalid Search",
            })


def random(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[entry]))


def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
        return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[title]))

    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/edit.html", {
            "search": SearchForm(),
            "title": title,
            "form": EditForm(initial={
                "text": entry
            })
        })

    return render(request, "encyclopedia/error.html", {
        "search": SearchForm(),
        "error": "Page not found",
    })


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "search": SearchForm(),
                    "error": "Entry already exists",
                })

            text = form.cleaned_data["text"]
            util.save_entry(title, text)
        return HttpResponseRedirect(reverse("encyclopedia:entry_page", args=[title]))

    return render(request, "encyclopedia/new.html", {
        "search": SearchForm(),
        "form": NewEntryForm()
    })
