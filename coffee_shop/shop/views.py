from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Order, OrderItem
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ContactForm

def home(request):
    products = Product.objects.filter(available=True)[:6]  # Featured products
    return render(request, 'home.html', {'products': products})

def menu(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    products = Product.objects.filter(available=True)
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category__name=category)
    categories = Category.objects.all()
    return render(request, 'menu.html', {'products': products, 'categories': categories})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to cart!")
    return redirect('menu')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        items.append({'product': product, 'quantity': quantity, 'subtotal': subtotal})
        total += subtotal
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Cart is empty!")
            return redirect('cart')
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            total += product.price * quantity
        order.total = total
        order.save()
        request.session['cart'] = {}
        messages.success(request, "Order placed!")
        return redirect('home')
    return render(request, 'checkout.html')

def about(request):
    return render(request, 'about.html')
def logout_view(request):
    logout(request)
    return redirect('/')
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Thank you! Your message has been sent successfully. We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'contact_info': {
            'address': '123 Coffee Street, Downtown City, CA 90210',
            'phone': '(555) 123-4567',
            'email': 'hello@coffeecorner.com',
            'hours': 'Mon-Fri: 7AM-8PM | Sat-Sun: 8AM-6PM'
        }
    }
    return render(request, 'contact.html', context)