from django.shortcuts import render

def mainms(request):
    return render(request, 'mindsync/mindsync.html')
