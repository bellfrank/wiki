from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django import forms

from markdown2 import Markdown

markdowner = Markdown()

from . import util

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))


class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')


def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    
                    context = {
                        'page': page_converted,
                        'title': item,
                        'form': Search()
                    }

                    return render(request, "encyclopedia/entry.html", context)
                if item.lower() in i.lower(): 
                    searched.append(i)
                    context = {
                        'searched': searched, 
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", context)

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })
def webpages(request, title):
    page = util.get_entry(title)
    return render(request, "encyclopedia/webpages.html", {
        "title":markdowner.convert(page)
    })

def create(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"message": "Page already exists"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)

                context = {
                    'form': Search(),
                    'page': page_converted,
                    'title': title
                }

                return render(request, "encyclopedia/entry.html", context)
    else:
        return render(request, "encyclopedia/create.html", {"form": Search(), "post": Post()})

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)
        
        context = {
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", context)
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)

            context = {
                'form': Search(),
                'page': page_converted,
                'title': title
            }

            return render(request, "encyclopedia/entry.html", context)


