from django.shortcuts import render, redirect
from django.conf import settings
from .models import User, Watchs, CartItem
from django.core.mail import send_mail
import random
from django.http import JsonResponse

# Create your views here.
def index(request):
    watch = Watchs.objects.all()
    return render(request,"index.html", {'watch': watch})

def about(request):
    return render(request, "about.html")

def watchs(request):
    watch = Watchs.objects.all()
    return render(request, "watchs.html", {'watch':watch})

def testimonial(request):
    return render(request, "testimonial.html")

def contact(request):
    return render(request, "contact.html")

def signup(request):
    if request.method == "POST": 
        usertype = request.POST['usertype']  
        if not usertype:
            msg1 = "Please select usertype..."
            return render(request, "signup.html", {'msg1':msg1})         
        try:
            user = User.objects.get(email = request.POST['email'])
            msg1 = "Email Already Exists!!!"
            return render(request, 'signup.html', {'msg1':msg1})
        except:
            if request.POST['pswd'] == request.POST['cpswd']:
                User.objects.create(
                    usertype = request.POST['usertype'],
                    fname = request.POST['fname'],
                    lname = request.POST['lname'],
                    email = request.POST['email'],
                    pswd = request.POST['pswd'],
                )
                msg = "SignUp Done Successfully!!!"
                return render(request, 'login.html', {'msg':msg})
                
            else:
                msg1 = "Password and confirm password does not match!!!"
                return render(request, 'signup.html', {'msg1':msg1})
    else:
        return render(request, 'signup.html')
    
def e_verify(request):
    email = request.GET.get('email')
    print(">>>>>>>>>>>>>>>", email)
    data = {'is_taken': User.objects.filter(email__iexact=email).exists()}
    return JsonResponse(data)

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'], pswd=request.POST['pswd'])
            request.session['email'] = user.email
            request.session['fname'] = user.fname  # Store the first name in the session
            if user.usertype == "seller":
                return render(request, "seller_index.html")
            else:
                return redirect('index')
        except User.DoesNotExist:
            msg1 = "Email does not exist!!!"
            return render(request, 'login.html', {'msg1': msg1})

    else:
        return render(request, 'login.html')

    
def fpswd(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            subject = "Forgot Password OTP"
            otp = random.randint(1000, 9999)
            message = f"Hi {user.fname}, Thankyou For Registering In Our App!, Your OTP Is:- "+str(otp)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            return render(request, "verify_otp.html", {'email': user.email, 'otp':str(otp)})
        except User.DoesNotExist:
            msg1 = "You are not register user!!!"
            return render(request, "signup.html", {'msg1':msg1})
    else:
        return render(request, 'fpswd.html')
    
def verify_otp(request):
    email = request.POST['email']
    uotp = request.POST['uotp']
    otp = request.POST['otp']
    if request.method == "POST":
        if uotp == otp:
            return render(request, "set_new_pswd.html", {'email':email}) 
        else:
            msg1 = "OTP does not matched!!!"
            return render(request, "fpswd.html", {'msg1':msg1})
    else:
        return render(request, 'verify_otp.html')
    
def set_new_pswd(request):
    if request.method == "POST":
        email = request.POST['email']
        npswd = request.POST['npswd']
        cnpswd = request.POST['cnpswd']
        if npswd == cnpswd:
            user = User.objects.get(email=email)
            user.pswd=npswd
            user.save()
            return redirect('login')
        else:
            msg1 = "Password and confirm password does not matched!!!"
            return render(request, 'set_new_pswd.html', {'msg1':msg1})
    else:
        return render(request, "set_new_pswd.html")
    
def logout(request):
    del request.session['email']
    return redirect('login')


# Seller Side Views
def seller_index(request):
    watch = Watchs.objects.all()
    return render(request, "seller_index.html", {'watch':watch})

def seller_about(request):
    return render(request, "seller_about.html")

def seller_watchs(request):
    seller = User.objects.get(email = request.session['email'])
    watch = Watchs.objects.filter(user=seller)
    return render(request, "seller_watchs.html", {'watch':watch})

def seller_contact(request):
    return render(request, "seller_contact.html")  


# CRUD of Watch
def add_watch(request):
    if request.method == "POST":
        user = User.objects.get(email = request.session['email'])
        Watchs.objects.create(
            user = user,
            watchtype = request.POST['watchtype'],
            w_image = request.FILES['w_image'],
            w_brand = request.POST['w_brand'],
            w_model = request.POST['w_model'],
            w_price = request.POST['w_price'],
            w_features = request.POST['w_features'],
        )
        msg = "Watchs added successfully!!!"
        return render(request, 'add_watch.html', {'msg':msg})
    else:
        return render(request, "add_watch.html")

def update_watch(request, pk):
    seller = User.objects.get(email = request.session['email'])
    watch = Watchs.objects.get(pk=pk, user=seller)

    if request.method == "POST":
        watch.user = seller
        watch.watchtype = request.POST['watchtype']
        watch.w_image = request.FILES['w_image']
        watch.w_brand = request.POST['w_brand']
        watch.w_model = request.POST['w_model']
        watch.w_price = request.POST['w_price']
        watch.w_features = request.POST['w_features']
        watch.save()
        return redirect('seller_watchs')
    else:
        return render(request, "update_watch.html", {'watch':watch})
    
def delete_watch(request, pk):
    seller = User.objects.get(email = request.session['email'])
    watch = Watchs.objects.get(pk=pk, user=seller)
    watch.delete()
    return redirect('seller_index')


def w_details(request, pk):
    watch = Watchs.objects.get(pk=pk)
    return render(request, "w_details.html", {'watch':watch})

def add_to_cart(request, pk):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        watch = Watchs.objects.get(pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            watch=watch,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return redirect('view_cart')

def view_cart(request):
        user = User.objects.get(email = request.session['email'])
        cart_items = CartItem.objects.filter(user=user)
        return render(request, "view_cart.html", {'cart_items':cart_items})

def remove_from_cart(request, pk):
    user = User.objects.get(email = request.session['email'])
    cart_items = CartItem.objects.filter(pk=pk, user=user)
    cart_items.delete()
    return redirect('view_cart')

def my_orders(request):
    return render(request, "my_orders.html")
