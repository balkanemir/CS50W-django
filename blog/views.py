from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

class TestForm(forms.Form):
    test = forms.CharField(max_length=12)

def index(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data["test"]
            request.session["testlist"] += [test]
            return HttpResponseRedirect(reverse("blog:home"))
        else:
            return render(request, "blog/index.html", {
                "form": form
            })    
    return render(request, "blog/index.html", {
        "form": TestForm()
    })



def home(request):
    if "testlist" not in request.session:
        request.session["testlist"] = []
    return render(request, "blog/home.html", {
        "testlist": request.session["testlist"]
    })

