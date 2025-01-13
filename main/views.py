from django.shortcuts import render,redirect

#Used for authenticate user, login if authenticated and logout from the session
from django.contrib.auth import authenticate, login, logout 

#Used for restrict from unauthenticated user
from django.contrib.auth.decorators import login_required

# For Displaying messages
from django.contrib import messages

# Used for creatnig Users
from django.contrib.auth.models import User 

# For generating ShortID
from shortuuid import ShortUUID

# Importing Model from Models.py
from main.models import LinksData

# Create your views here.
def home(request):
    return render(request, "index.html")

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username = username).exists():
            messages.info(request, "Invalid Username!")
            return redirect('/login/')
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.info(request, "Invalid Username or Password!")
            return redirect('/login/')
        else:
            login(request, user)
            messages.info(request, "Logged in SuccessFully!")
            return redirect('/shorten-url/')
        
    return render(request, "login.html")

def signup_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request, "Username Already exists")
            return redirect('/signup/')

        user = User.objects.create(
            username = username,
            email = email
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account Created Successfully!!")

        return redirect('/signup/')

    return render(request, "signup.html")

def logout_page(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/login") 
def shorten_url(request):
    
    if request.method == "POST":
        original_link = request.POST.get('input_link')
       
        if not original_link:
            return render(request, "shortenlinks.html", {"error": "Link is required."})
        
        username = request.user.username
       
        shortened_id = ShortUUID().random(length=4)
        
        LinksData.objects.create(
            username = username,
            redirect_link = original_link,
            short_id = shortened_id
        )
        messages.info(request, "Link Shortend Successfully!!")

        return redirect('/shorten-url')
    queryset = LinksData.objects.all()

    return render(request, "shortenlinks.html", context = {"queryset": queryset})


def redirect_url(request, short_id):
    queryset = LinksData.objects.get(short_id = short_id)
    newlink = queryset.redirect_link

    return redirect(newlink)