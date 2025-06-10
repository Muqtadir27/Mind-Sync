from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from .models import User

from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Let the form's save method handle everything, including password hashing
            form.save()
            return redirect('Login')
        else:
            print("Form is invalid:", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'Student/signup.html', {'form': form})




from django.shortcuts import render, redirect
from .forms import LoginForm
from .models import User

from django.contrib.auth.hashers import check_password

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            studentid = form.cleaned_data['studentid']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(studentid=studentid)
                if check_password(password, user.password):
                    # login successful
                    return redirect('Studenthome')
                else:
                    form.add_error(None, "Invalid student ID or password")
            except User.DoesNotExist:
                form.add_error(None, "Invalid student ID or password")
    else:
        form = LoginForm()
    return render(request, 'Student/login.html', {'form': form})





def mailrvry(req):
    return render(req,'Student/Recovery.html')

