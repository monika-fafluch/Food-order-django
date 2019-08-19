from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from .models import Items, Orders, Carts
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json


# declare some variables for further usage
id_list = []
total_updated = 0

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
        price = cart[0]["price"]
        toppings = ', '.join(cart[1])
        toppings_steak = ', '.join(cart[2])
        order = Orders(client=client, item=item, topping=toppings, topping_steak=toppings_steak, price=price)
        order.save()
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


def cart(request):
    
    total = 0
    # display cart content 
    user_logged = request.user.username
    client = User.objects.get(username=user_logged)
    items_list = Orders.objects.filter(client=client, status="False")
    # check if there are any orders in this client's cart
    count = items_list.count()
    items = []
    for item in items_list:
        b = {"name": item.item.name, "price": item.price, "toppings": item.topping, "toppings_steak": item.topping_steak, "id": item.id}
        items.append(dict(b))
        # calculate total price of order for one client
        total += item.price
    request.session["total_price"] = total
    request.session.modified = True
    context = {
        "items": items,
        "total": request.session["total_price"],
        "count": count
    }
    return render(request, "orders/cart.html", context) # POST HERE OR SOMETHING

def ajax_view(request):
    if request.method == "POST":
        # remove items from database that were removed from cart
        remove_orders = json.loads(request.body)
        query = Orders.objects.get(id=remove_orders["id"])
        price = query.price
        # update total price after removing items from cart
        request.session["total"] = remove_orders["total"]
        request.session["total_price"] =  float(request.session["total_price"] ) - float(price)
        request.session.modified = True
        Orders.objects.get(id=remove_orders["id"]).delete()
        data = {"msg": request.session["total_price"]}
        print(request.session["total_price"])
        return JsonResponse(data)
      
    
    return HttpResponse("success")


@login_required
def owner(request):
    # get ajax data to change status/remove order in db
    if request.method == "POST":
        change_status = json.loads(request.body)
        order_id = change_status["id"]
        status = change_status["status"]
        # change status in db to "True"(done)
        if status == "True":
            Orders.objects.filter(id=order_id).update(status=status)
            print("status changed")
        # remove order
        elif status == "remove":
            Orders.objects.filter(id=order_id).delete()
            print("deleted")
        else:
            print("incorrect status")

        
    # pass orders details to owner template
    orders = Orders.objects.all()
    context = {
        "orders": orders,
    }
    return render(request, "orders/owner.html", context)

"""def owner_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        myList = data["list"]
        my_ids = ','.join(myList)
        user = request.user
        x = Carts(client=user, ids=my_ids)
        x.save()
        return HttpResponse("success")
    retrieve_orders = Carts.objects.all()
    for order in retrieve_orders:
        for id in order.ids:
            print(id)
    send_data = {"id": [], "username": [], "item": [], "date": [], "status": []}
    print(retrieve_orders)
    for order in orders:
        send_data["id"].append(order.id)
        send_data["username"].append(order.client.username)
        send_data["item"].append(order.item)
        send_data["date"].append(order.date)
        send_data["status"].append(order.status)
    print(send_data)
    return HttpResponse('od')"""

def confirm(request):
    return render(request, "orders/confirmation.html")

def logout(request):
    django_logout(request)
    return render(request, "orders/index.html")