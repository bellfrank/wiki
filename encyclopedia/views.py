from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django import forms

from markdown2 import Markdown

markdowner = Markdown()

from . import util

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))

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
    return render(request, "encyclopedia/webpages.html", {
        "title": util.get_entry(title)
    })
