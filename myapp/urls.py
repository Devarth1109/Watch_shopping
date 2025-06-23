from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('watchs', views.watchs, name="watchs"),
    path('testimonial', views.testimonial, name="testimonial"),
    path('contact', views.contact, name="contact"),
    path('signup', views.signup, name="signup"),
    path('ajax/e_verify/',views.e_verify,name='e_verify'),
    path('login', views.login, name="login"),
    path('fpswd', views.fpswd, name="fpswd"),
    path('verify_otp', views.verify_otp, name="verify_otp"),
    path('set_new_pswd', views.set_new_pswd, name="set_new_pswd"),
    path('logout', views.logout, name="logout"),

    # Seller Side URLs
    path('seller_index', views.seller_index, name="seller_index"),
    path('seller_about', views.seller_about, name="seller_about"),
    path('seller_watchs', views.seller_watchs, name="seller_watchs"),
    path('seller_contact', views.seller_contact, name="seller_contact"),

    # CRUD of Watch
    path('add_watch', views.add_watch, name="add_watch"),
    path('update_watch/<int:pk>', views.update_watch, name="update_watch"),
    path('delete_watch/<int:pk>', views.delete_watch, name="delete_watch"),

    # Cart
    path('w_details/<int:pk>', views.w_details, name="w_details"),
    path('add_to_cart/<int:pk>', views.add_to_cart, name="add_to_cart"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove_from_cart"),
]