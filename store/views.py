from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem
from .mpesa import stk_push
from django.http import JsonResponse

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
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def checkout(request):
    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        cart_data = request.session.get('cart', {})

        total = 0

        order = Order.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            total_amount=0
        )

        for product_id, quantity in cart_data.items():

            product = Product.objects.get(id=product_id)

            total += product.price * quantity

            for i in range(quantity):
                OrderItem.objects.create(
                    order=order,
                    product=product
                )

        order.total_amount = total
        order.save()

        response = stk_push(
            phone_number,
            int(total)
        )

        print("MPESA RESPONSE:")
        print(response)

        request.session['cart'] = {}

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


import json

def mpesa_payment(request):

    response = stk_push(
        "254718236911",
        1
    )

    return JsonResponse(response)
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)

    return JsonResponse({
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    })