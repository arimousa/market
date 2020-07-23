from django.shortcuts import render, redirect
from .forms import CustomerRegisterForm, UserRegisterForm
from django.contrib import messages
from market.models import Customer


def register(request):
    if request.method == "POST":
        register_form = UserRegisterForm(request.POST)
        customer_form = CustomerRegisterForm()
        if register_form.is_valid():
            user = register_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            # print(register_form.cleaned_data.get('email'))
            customer.address = ""
            customer.phone = ""
            customer.save()
            messages.success(request, 'New user created, login to get started')
            return redirect('register')
    else:
        register_form = UserRegisterForm()
    return render(request, 'register.html', {'register_form': register_form})
