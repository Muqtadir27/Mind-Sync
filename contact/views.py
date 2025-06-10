from django.shortcuts import render

# Create your views here.
def Contact(req):
    return render(req,'contact/contact.html')