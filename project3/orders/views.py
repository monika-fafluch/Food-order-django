from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from .models import Items, Orders
from django.urls import reverse
import simplejson as json

# Create your views here.
def index(request):
    if request.method == "GET":
        user = request.POST.get("username")
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('menu'))
        else:
            return render(request, "orders/index.html")
    else:
        # authenticate the user
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            loginError = "Invalid credentials"
            return render(request, "orders/index.html", {"loginError": loginError})
        else:
            login(request, user)
        return HttpResponseRedirect(reverse('menu'))

def register(request):
    if request.method == "GET":
        return render(request, "orders/register.html")
    else:
        username = request.POST.get("username-register")
        password = request.POST.get("password-register")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm-password")
        # backend validation/check if username/password isn't empty
        if not username or not password:
            error0 = "No username/password"
            return render(request, "orders/register.html", {"error0": error0})
        # check if passwords match
        if password != confirm_password:
            error = "Passwords do not match."
            return render(request, "orders/register.html", {"error": error})
        # create a user object and redirect to login page
        user = User.objects.create_user(username=email, email=email, password=password)
        user.save()
        return HttpResponseRedirect(reverse('index'))

def menu(request):
    if request.method == "POST":

        cart = json.loads(request.body)
        user_logged = request.user.username
        client = User.objects.get(username=user_logged)
        item = Items.objects.get(name=cart[0]["name"], dish=cart[0]["dish"])
        toppings = ','.join(cart[1])
        toppings_steak = ','.join(cart[2])
        order = Orders(client=client, item=item, topping=toppings, topping_steak=toppings_steak)
        order.save()
        print(order)
        return HttpResponse("success")
    context = {
        "items": Items.objects.filter(dish="regular pizza"),
        "selects": Items.objects.filter(dish="Toppings"),
        "items_sicilian": Items.objects.filter(dish="sicilian pizza"),
        "subs": Items.objects.filter(dish="Subs"),
        "pasta": Items.objects.filter(dish="Pasta"),
        "salads": Items.objects.filter(dish="Salad"),
        "dinner_platters": Items.objects.filter(dish="Dinner Platters")
    }
    return render(request, "orders/items.html", context)

def logout(request):
    django_logout(request)
    return render(request, "orders/index.html")