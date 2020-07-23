from django.shortcuts import render, redirect
from django.http import HttpResponse
from market.models import Product, Order, Customer, OrderRow
from market.forms import ProductForm, OrderRowForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    context = {
        'index_text': "welcome to index page."
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        'about_text': "welcome to about page."
    }
    return render(request, 'about.html', context)


def contact(request):
    context = {
        'contact_text': "welcome to contact page."
    }
    return render(request, 'contact.html', context)


@login_required
def product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid:
            form.save()
            messages.success(request, "New product added!")
        return redirect('product')
    else:
        all_products = Product.objects.all()
        paginator = Paginator(all_products, 5)
        page = request.GET.get('pg')
        all_products = paginator.get_page(page)
        return render(request, 'product.html', {'all_products': all_products})


@login_required
def delete_product(request, product_code):
    product_d = Product.objects.get(pk=product_code)
    product_d.delete()
    return redirect('product')


@login_required
def edit_product(request, product_code):
    if request.method == 'POST':
        product_obj = Product.objects.get(pk=product_code)
        form = ProductForm(request.POST or None, instance=product_obj)
        if form.is_valid():
            form.save()
        messages.success(request, "Product edited!")
        return redirect('product')
    else:
        product_obj = Product.objects.get(pk=product_code)
        return render(request, 'edit.html', {'product_obj': product_obj})


def shop(request):
    all_products = Product.objects.all()
    paginator = Paginator(all_products, 5)
    page = request.GET.get('pg')
    all_products = paginator.get_page(page)
    return render(request, 'shop.html', {'all_products': all_products})


@login_required
def order(request):
    all_orders = OrderRow.objects.all()
    paginator = Paginator(all_orders, 5)
    page = request.GET.get('pg')
    all_orders = paginator.get_page(page)
    return render(request, 'order.html', {'all-orders': all_orders})


def buy(request, product_code):
    amount = 0
    if request.method == 'POST':
        buy_form = OrderRowForm(request.POST or None)
        if buy_form.is_valid():
            amount = buy_form.cleaned_data.get('amount')
        customer = list(Customer.objects.filter(user=request.user))[0]
        product_obj = Product.objects.get(code=product_code)
        order_product = Order(customer=customer, status=1)
        order_product.add_product(product_obj, amount=amount)
        order_product.submit()
        order_product.send()
        return redirect('product')
    else:
        product_obj = Product.objects.get(pk=product_code)
        return render(request, 'buy.html', {'product_obj': product_obj})
