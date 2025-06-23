from django.contrib import admin
from .models import User, Watchs, CartItem
# Register your models here.

admin.site.register(User)
admin.site.register(Watchs)
admin.site.register(CartItem)
