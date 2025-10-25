from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Provider,Service

# Example state-city mapping
STATE_CITY = {
    "California": ["Los Angeles", "San Francisco", "San Diego"],
    "Texas": ["Houston", "Austin", "Dallas"],
    "Florida": ["Miami", "Orlando", "Tampa"],
    "New York": ["New York City", "Buffalo", "Rochester"],
}

def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        state = request.POST.get('state')
        city = request.POST.get('city')

        if Provider.objects(email=email).first():
            messages.error(request, 'Email already registered!')
        else:
            Provider(
                full_name=full_name,
                email=email,
                password=password,
                phone=phone,
                bio=bio,
                state=state,
                city=city
            ).save()
            messages.success(request, 'Signup successful! Please login.')
            return redirect('providers:login')

    return render(request, 'providers/signup.html', {'state_city': STATE_CITY})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        provider = Provider.objects(email=email, password=password).first()
        if provider:
            request.session['provider_id'] = str(provider.id)
            request.session['provider_name'] = provider.full_name
            return redirect('providers:dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    return render(request, 'providers/login.html')

def add_service_view(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    from .models import Service, Provider
    provider = Provider.objects(id=provider_id).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')

        Service(
            title=title,
            category=category,
            provider=provider
        ).save()
        messages.success(request, "Service added successfully!")

    services = Service.objects(provider=provider)
    return render(request, 'providers/add_service.html', {'provider': provider, 'services': services})



def dashboard_view(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')
    provider = Provider.objects(id=provider_id).first()

    # get services of this provider
    services = Service.objects(provider=provider).order_by('-created_at')

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        if title:
            Service(provider=provider, title=title, category=category).save()
            return redirect('providers:dashboard')

    return render(request, 'providers/dashboard.html', {
        'provider': provider,
        'services': services
    })
def logout_view(request):
    request.session.flush()
    return redirect('providers:login')
