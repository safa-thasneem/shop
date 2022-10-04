from django.shortcuts import render, redirect, get_object_or_404
from ecommerceapp.models import product
from .models import cart,cart_item
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    products=product.objects.get(id=product_id)
    try:
        Cart=cart.objects.get(cart_id=_cart_id(request))
    except cart.DoesNotExist:
        Cart=cart.objects.create(
             cart_id=_cart_id(request)
        )
        Cart.save(),
    try:
        Cart_Item=cart_item.objects.get(product=products,cart=Cart)
        if Cart_Item.QUANTITY < Cart_Item.product.stock:
           Cart_Item.QUANTITY +=1
        Cart_Item.save()
    except cart_item.DoesNotExist:
        Cart_Item=cart_item.objects.create(
              product=products,
              QUANTITY=1,
               cart=Cart
        )
        Cart_Item.save()
    return redirect('cart:cart_detail')

def cart_detail(request,total=0,counter=0,Cart_Items=None):
      try:
            Cart=cart.objects.get(cart_id=_cart_id(request))
            Cart_Items=cart_item.objects.filter(cart=Cart,active=True)
            for cart_items in Cart_Items:
                 total+=(cart_items.product.price * cart_items.QUANTITY)
                 counter+=cart_items.QUANTITY

      except ObjectDoesNotExist:
               pass
      return render(request,'cart.html',dict(Cart_Items=Cart_Items,total=total,counter=counter))

def cart_remove(request,product_id):
    Cart=cart.objects.get(cart_id=_cart_id(request))
    Product=get_object_or_404(product,id=product_id)
    Cart_Item=cart_item.objects.get(product=Product,cart=Cart)
    if Cart_Item.QUANTITY >1:
        Cart_Item.QUANTITY-=1
        Cart_Item.save()
    else:
        Cart_Item.delete()
    return redirect('cart:cart_detail')
def full_remove(request,product_id):
    Cart = cart.objects.get(cart_id=_cart_id(request))
    Product = get_object_or_404(product, id=product_id)
    Cart_Item = cart_item.objects.get(product=Product, cart=Cart)
    Cart_Item.delete()
    return redirect('cart:cart_detail')