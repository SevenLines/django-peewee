from django.http import HttpResponse
from django.shortcuts import render, render_to_response


# Create your views here.
from test_django_peewee.models import TestModel


def index(request):
    TestModel.objects.create()
    data = TestModel.objects.all()
    return render_to_response("index.html", {
        "data": data
    })
