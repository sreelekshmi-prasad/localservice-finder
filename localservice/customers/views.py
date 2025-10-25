from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        if Customer.objects(email=email).first():
            messages.error(request, 'Email already registered!')
        else:
            Customer(name=name, email=email, password=password, phone=phone).save()
            messages.success(request, 'Signup successful! Please login.')
            return redirect('customers:login')

    return render(request, 'customers/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Customer.objects(email=email, password=password).first()
        if user:
            # Optional: store in session
            request.session['customer_id'] = str(user.id)
            request.session['customer_name'] = user.name
            return render(request, 'customers/dashboard.html', {'customer': user})
        else:
            messages.error(request, 'Invalid credentials!')

    return render(request, 'customers/login.html')
