from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Q
from .models import Medicine, Cart, Order, Payment,Address,CUser
from .forms import AddressForm
# Home Page
def index(req):
    allMedicine = Medicine.objects.all()
    context = {"allMedicine": allMedicine}
    return render(req, "index.html", context)



# Password Validation Function
def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters")

    has_upper, has_lower, has_digit, has_special = False, False, False, False
    special_char = "@#!?*&%$"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_char:
            has_special = True

    if not all([has_upper, has_lower, has_digit, has_special]):
        raise ValidationError("Password must contain uppercase, lowercase, digit & special char.")

    common_passwords = ["password", "123456", "qwerty", "abc123"]
    if password in common_passwords:
        raise ValidationError("This password is too common. Please try another.")


# Signup Function
def signup(req):
    if req.method == "GET":
        return render(req, "signup.html")
    
    uname, upass, ucpass = req.POST["uname"], req.POST["upass"], req.POST["ucpass"]

    context = {}
    if not uname or not upass or not ucpass:
        context["errmsg"] = "Fields can't be empty"
    elif upass != ucpass:
        context["errmsg"] = "Password and confirm password do not match"
    elif upass == uname:
        context["errmsg"] = "Password cannot be the same as username"
    else:
        try:
            validate_password(upass)
            userdata = User.objects.create(username=uname)
            userdata.set_password(upass)
            userdata.save()
            return redirect("signin")
        except ValidationError as e:
            context["errmsg"] = str(e)
        except:
            context["errmsg"] = "User already exists"

    return render(req, "signup.html", context)


# Signin Function
def signin(req):
    if req.method == "GET":
        return render(req, "signin.html")
    
    uname, upass = req.POST["uname"], req.POST["upass"]
    context = {}

    if not uname or not upass:
        context["errmsg"] = "Fields can't be empty"
        return render(req, "signin.html", context)
    
    userdata = authenticate(username=uname, password=upass)

    if userdata:
        login(req, userdata)
        return redirect("index")
    else:
        context["errmsg"] = "Invalid username or password"
        return render(req, "signin.html", context)


# Logout Function
def userlogout(request):
    logout(request)
    return redirect("index")


# Order Function
def order(request):
    if request.method == "POST":
        messages.success(request, "Your order has been placed successfully!")
        return redirect("index")
    return render(request, "home.html")


# Forgot Password
def forgotpass(req):
    if req.method == "GET":
        return render(req, "forgotpass.html")
    
    uname = req.POST.get("uname")
    if User.objects.filter(username=uname).exists():
        return redirect("resetpassword", uname=uname)
    else:
        messages.error(req, "User not found")
        return redirect("forgotpass")


# Reset Password
def resetpassword(req, uname):
    if req.method == "GET":
        return render(req, "resetpassword.html")

    upass = req.POST.get("new_password")
    try:
        userdata = User.objects.get(username=uname)
        validate_password(upass)
        userdata.set_password(upass)
        userdata.save()
        return redirect("signin")
    except ValidationError as e:
        messages.error(req, ", ".join(e.messages))
        return redirect("resetpassword", uname=uname)


# About Page
def about(req):
    return render(req, "about.html")


# Contact Page
def contact(req):
    return render(req, "contact.html")


# Search Medicine
def searchmedicine(req):
    query = req.GET.get("q", "").strip()
    if query:
        allMedicine = Medicine.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if not allMedicine.exists():
            messages.error(req, "No result found!")
            return redirect("index")
    else:
        allMedicine = Medicine.objects.all()

    context = {"allMedicine": allMedicine}
    return render(req, "index.html", context)

def showcarts(req):
    username=req.user
    allcarts=Cart.objects.filter(userid=username.id)
    print(allcarts,len(allcarts))
    totalitems=len(allcarts)
    totalamount=0
    for x in allcarts:
        totalamount+=x.productid.price*x.qty
    if username.is_authenticated:
        context={'allcarts':allcarts,"username":username,'totalitems':totalitems,"totalamount":totalamount}
    else:
        context={'allcarts':allcarts,"totalitems":totalitems,"totalamount":totalamount}
    return render(req, 'showcarts.html',context)


# def addtocart(req,medicineid):
#     if req.user.is_authenticated:
#         userid=req.user
#     else:
#         userid=None
   
#     allMedicine=get_object_or_404(Medicine,medicineid=medicineid)
#     cartitem, created = Cart.objects.get_or_create(userid=userid, productid=allMedicine)
#     print(cartitem)
#     print(created)

#     if not created:
#         cartitem.qty+=1
#     else:
#         cartitem.qty=1
#     cartitem.save()
#     return redirect("/showcarts")

def addtocart(req, medicineid):
    if req.user.is_authenticated:
        userid = req.user
    else:
        userid = None

    allMedicine = get_object_or_404(Medicine, medicineid=medicineid)
    print(allMedicine)
    cartitem, created = Cart.objects.get_or_create(userid=userid, productid=allMedicine)

    print(cartitem)
    print(created)

    if not created:
        cartitem.qty += 1
    else:
        cartitem.qty = 1
    cartitem.save()

    return redirect("/showcarts")



def removecart(req, medicineid):
    if not req.user.is_authenticated:
        return redirect("signin")

    user = req.user
    cart_item = get_object_or_404(Cart, medicineid=medicineid, userid=user)
    cart_item.delete()

    messages.success(req, "Item has been removed from your cart!")
    return redirect("showcarts")


def updateqty(req, qv, medicineid):
    if not req.user.is_authenticated:
        return redirect("signin")

    cart_item = get_object_or_404(Cart, medicineid=medicineid, userid=req.user.CUser)


    if qv == 1:
        cart_item.qty += 1
    elif cart_item.qty > 1:
        cart_item.qty -= 1
    else:
        cart_item.delete()
        return redirect("showcarts")

    cart_item.save()
    return redirect("showcarts")


def addaddress(req):
    if not req.user.is_authenticated:
        return redirect("signin")

    if req.method == "POST":
        form = AddressForm(req.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.userid = req.user
            address.save()
            messages.success(req, "Address added successfully!")
            return redirect("showaddress")
    else:
        form = AddressForm()

    return render(req, 'addaddress.html', {'form': form})


def showaddress(req):
    if not req.user.is_authenticated:
        return redirect("signin")

    addresses = Address.objects.filter(userid=req.user)
    return render(req, 'showaddress.html', {'addresses': addresses})


from django.shortcuts import render
