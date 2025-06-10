from django.shortcuts import render

# Create your views here.
def whyus(req):
    return render(req,'yus/whyus.html')