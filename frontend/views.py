from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
def home(request):
    template=loader.get_template("homepage.html")
    context={'user':request.user}
    return HttpResponse(template.render(context,request))

def about(request):
    template=loader.get_template("about.html")
    context={'user':request.user}
    return HttpResponse(template.render(context,request))

def contact(request):
    template=loader.get_template("contact.html")
    context={'user':request.user}
    return HttpResponse(template.render(context,request))
