from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {
        'products': products
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {
        'product': product
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id not in cart:
        cart.append(product_id)

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_ids = request.session.get('cart', [])

    products = Product.objects.filter(id__in=cart_ids)

    total = 0
    for product in products:
        total += product.price

    return render(request, 'store/cart.html', {
        'products': products,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])

    if product_id in cart:
        cart.remove(product_id)

    request.session['cart'] = cart

    return redirect('cart')


def checkout(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        cart_ids = request.session.get('cart', [])
        products = Product.objects.filter(id__in=cart_ids)

        total = 0
        for product in products:
            total += product.price

        order = Order.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            total_amount=total
        )

        for product in products:
            OrderItem.objects.create(
                order=order,
                product=product
            )

        request.session['cart'] = []

        return redirect('success')

    return render(request, 'store/checkout.html')


def success(request):
    return render(request, 'store/success.html')
def track_order(request):
    orders = None

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        orders = Order.objects.filter(
            phone_number=phone_number
        ).order_by('-created_at')

    return render(request, 'store/track_order.html', {
        'orders': orders
    })