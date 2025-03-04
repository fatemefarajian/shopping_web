from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from shop.models import Product
from .cart import Cart

@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = Cart(request)

        cart.add(product)

        context = {
            'item_count': len(cart),
            'total_price': cart.get_total_price(),
        }

        return JsonResponse(context)

    except:
        return JsonResponse({"error": "Something went wrong"})