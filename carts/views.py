from django.shortcuts import render,redirect
from accounts.forms import LoginForm,GuestForm
from accounts.models import GuestEmail
from .models import Cart
from orders.models import Order
from products.models import Product
from billing.models import BillingProfile
# Create your views here.
def cart_create(user=None):
    cart_obj=Cart.objects.create(user=None)
    print("new cart created")
    return cart_obj

def cart_home(request):
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    return render(request,'carts/views.html',{"cart":cart_obj})


def cart_update(request):
    product_id=request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj=Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("product has been gone")
            return redirect("cart:cart_home")
        cart_obj,new_obj=Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
                cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
            request.session['cart_items']=cart_obj.products.count()
        return redirect("cart:cart_home")


def checkout_home(request):
    cart_obj,cart_created=Cart.objects.new_or_get(request)
    order_obj=None
    if cart_created or cart_obj.products.count()==0:
        return redirect("cart:cart_home")
    user=request.user
    billing_profile=None
    login_form=LoginForm()
    guest_form=GuestForm()
    guest_email_id=request.session.get('guest_email_id')
    if user.is_authenticated():
        billing_profile,billing_profile_created=BillingProfile.objects.get_or_create(user=user)

    elif guest_email_id is not None:
        guest_email_obj=GuestEmail.objects.get(id=guest_email_id)
        billing_profile,billing_guest_profile_created=BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    
    else:
        pass
    if billing_profile is not None:
        order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True)
        if order_qs.count()==1:
            order_obj=order_qs.first()
        else:
            old_order_qs=Order.objects.exclude(billing_profile=billing_profile).filter(cart=cart_obj,active=True)
            if old_order_qs.exists():
                old_order_qs.update(active=False)
            order_obj=Order.objects.create(billing_profile=billing_profile,cart=cart_obj)

    context={
        "object":order_obj,
        "billing_profile":billing_profile,
        'login_form':login_form,
        'guest_form':guest_form,

    }

    return render(request,"checkout.html",context)