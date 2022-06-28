import bcrypt
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect, render
from app_one.models import User
from django.contrib import messages

def index(request):
    return render(request,"home.html")


def register(request):
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/register")
        else:
            password = request.POST["password"]
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode(), salt)
            user = User()
            user.first_name = request.POST["first_name"]
            user.last_name = request.POST["last_name"]
            user.email = request.POST["email"]
            user.password = request.POST["password"]
            user.password = hash.decode()
            user.save()
            if user.id==1:
                user.is_admin = True
                user.save()
            messages.success(request, "User has been sucessfully registered")
        return redirect("/signin")
    return render(request,"register.html")





def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                request.session["loggedInUser"] = user.id
                if user.is_admin == True:
                    return render(request, "admin_dashboard.html")
                return render(request, 'user_dashboard.html')
            messages.error(
                request, "Incorrect Password")

        except User.DoesNotExist:
            messages.error(
                request, "You do not have an account ,Please Register first !")
        return redirect("/")
    return render(request,"signin.html")
    