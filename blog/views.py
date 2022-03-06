from .models import Flight, Passenger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
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

def flights(request):
    return render(request, "blog/flights.html", {
        "flights": Flight.objects.all()
        })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    return render(request, "blog/flight.html", {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all()
        })        



def book(request, flight_id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=int(request.POST["passenger"]))
        passenger.flight.add(flight)
        return HttpResponseRedirect(reverse("blog:flight", args=(flight.id)))