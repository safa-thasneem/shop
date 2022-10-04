from .models import cart,cart_item
from .views import _cart_id

def counter(request):
    item_count=0
    if 'admin' in request.path:
        return {}
    else:
          try:
                Cart=cart.objects.filter(cart_id=_cart_id(request))
                Cart_Items=cart_item.objects.all().filter(cart=Cart[:1])
                for Cart_item in Cart_Items:
                     item_count +=Cart_item.QUANTITY
          except cart.DoesNotExist:
                  item_count =0
    return dict(item_count=item_count)