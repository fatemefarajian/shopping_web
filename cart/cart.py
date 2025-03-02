from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')

        if not cart:
            cart = self.session['cart'] = {}

        self.cart = cart

    # ———————————————————————— افزودن به سبد خرید ———————————————————————
    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 1, 'price': product.new_price, 'weight': product.weight}
        else:
            if self.cart[product_id]['quantity'] < product.inventory:
                self.cart[product_id]['quantity'] += 1

        self.save()

    # ———————————————————— کاهش تعداد کالا از سبد خرید ———————————————————
    def decrease(self, product):
        product_id = str(product.id)
        if self.cart[product_id]['quantity'] > 1:
            self.cart[product_id]['quantity'] -= 1

            self.save()

    # ——————————————————— حذف یک محصول از سبد خرید ———————————————————
    def delete(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]

            self.save()

    # ——————————————— پاکسازی سبد خرید(حذف تمام محصولات) ———————————————
    def clear(self):
        del self.session['cart']
        self.save()

    # ——————————————————————— محاسبه هزینه پستی ———————————————————————
    def get_post_price(self):
        total_weight = sum(item['weight'] * item['quantity'] for item in self.cart.values())

        if total_weight == 0:
            return 0
        elif total_weight < 1000:
            return 20000
        elif 1000 < total_weight < 2000:
            return 30000
        else:
            return 50000

    # ————————————————————— محاسبه هزینه کل محصولات —————————————————————
    def get_total_price(self):
        total_price = sum(item['price'] * item['quantity'] for item in self.cart.values())
        return total_price

    # ——————————————————— محاسبه هزینه نهایی سبد خرید ———————————————————
    def get_final_price(self):
        final_price = self.get_total_price() + self.get_post_price()
        return final_price

    # ————————————————————— مجموع تعداد کل محصولات ——————————————————————
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    # ——————————————————————————— iteration ———————————————————————————— #
    def __iter__(self):
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids)
        cart_dict = self.cart.copy()

        for product in products:
            cart_dict[str(product.id)]['product'] = product

        for item in cart_dict.values():
            yield item

    # —————————————————————————————————————————————————————————————————— #
    def save(self):
        self.session.modified = True
