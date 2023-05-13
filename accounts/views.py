from django.shortcuts import render,redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from panel.views import instructions,dashboard

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                return redirect('/dashboard/panel/0/')
            return redirect(instructions)
        else:
            messages.error(request,"Invalid Credentials")
    return redirect(home)

def logout(request):
    auth.logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect(home)