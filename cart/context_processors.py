from .cart import Cart


def cart_context(request):
    return {'cart': Cart(request)}
