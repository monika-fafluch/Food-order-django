from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout, name="logout" ),
    path("menu/", views.menu, name="menu"),
    path("cart/", views.cart, name="cart"),
    path("owner/", views.owner, name="owner"),
    path("ajax_view/", views.ajax_view, name="ajax_view"),
    path("confirm/", views.confirm, name="confirm"),

]
