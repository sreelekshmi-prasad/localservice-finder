from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Provider, Service, AvailabilitySlot, Booking
from datetime import datetime
from bson import ObjectId


# Example state-city mapping
STATE_CITY = {
    "California": ["Los Angeles", "San Francisco", "San Diego"],
    "Texas": ["Houston", "Austin", "Dallas"],
    "Florida": ["Miami", "Orlando", "Tampa"],
    "New York": ["New York City", "Buffalo", "Rochester"],
}


# ---------------------- PROVIDER SIGNUP ----------------------
def signup_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        service_name = request.POST.get('service_name')
        service_category = request.POST.get('service_category')
        state = request.POST.get('state')
        city = request.POST.get('city')

        if Provider.objects(email=email).first():
            messages.error(request, 'Email already registered!')
            return redirect("providers:signup")

        provider = Provider(
            full_name=full_name,
            email=email,
            password=password,
            phone=phone,
            service_name=service_name,
            service_category=service_category,
            state=state,
            city=city,
            created_at=datetime.now(),
            is_approved=False
        )
        provider.save()

        # Auto create service
        Service(title=service_name, category=service_category, provider=provider).save()

        messages.success(request, "Signup successful! Please wait for admin approval.")
        return redirect("providers:login")

    return render(request, "providers/signup.html", {"state_city": STATE_CITY})


# ---------------------- PROVIDER LOGIN ----------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        provider = Provider.objects(email=email, password=password).first()

        if provider:
            request.session['provider_id'] = str(provider.id)
            request.session['provider_name'] = provider.full_name
            return redirect('providers:dashboard')

        messages.error(request, 'Invalid credentials!')
    return render(request, 'providers/login.html')


# ---------------------- PROVIDER DASHBOARD ----------------------
def dashboard_view(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    provider = Provider.objects(id=provider_id).first()

    services = Service.objects(provider=provider).order_by('-created_at')
    slots = AvailabilitySlot.objects(provider=provider).order_by('date')

    total_bookings = Booking.objects(slot__in=slots).count()

    return render(request, 'providers/dashboard.html', {
        'provider': provider,
        'services': services,
        'slots': slots,
        'total_bookings': total_bookings,
    })


# ---------------------- ADD SERVICE ----------------------
def add_service_view(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    provider = Provider.objects(id=provider_id).first()

    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')

        Service(title=title, category=category, provider=provider).save()
        messages.success(request, "Service added successfully!")
        return redirect('providers:add_service')

    services = Service.objects(provider=provider)
    return render(request, 'providers/add_service.html', {
        'provider': provider,
        'services': services
    })


# ---------------------- ADD SLOT ----------------------
def add_slot(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    provider = Provider.objects(id=provider_id).first()
    services = Service.objects(provider=provider)

    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        date = request.POST.get('date')
        start = request.POST.get('start_time')
        end = request.POST.get('end_time')

        service = Service.objects(id=ObjectId(service_id)).first()

        AvailabilitySlot(
            provider=provider,
            service=service,
            date=datetime.strptime(date, "%Y-%m-%d"),
            start_time=start,
            end_time=end,
        ).save()

        messages.success(request, "Availability slot added!")
        return redirect('providers:dashboard')

    return render(request, 'providers/add_slot.html', {'services': services})


# ---------------------- EDIT SLOT ----------------------
def edit_slot(request, slot_id):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    provider = Provider.objects(id=provider_id).first()
    slot = AvailabilitySlot.objects(id=ObjectId(slot_id)).first()
    services = Service.objects(provider=provider)

    if request.method == 'POST':
        service_id = request.POST.get('service_id')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        slot.service = Service.objects(id=ObjectId(service_id)).first()
        slot.date = datetime.strptime(date, "%Y-%m-%d")
        slot.start_time = start_time
        slot.end_time = end_time
        slot.save()

        messages.success(request, "Slot updated successfully!")
        return redirect('providers:dashboard')

    return render(request, 'providers/edit_slot.html', {
        'slot': slot,
        'services': services
    })


# ---------------------- DELETE SLOT (SAFE DELETE) ----------------------
def delete_slot(request, slot_id):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    slot = AvailabilitySlot.objects(id=ObjectId(slot_id)).first()

    if not slot:
        messages.error(request, "Slot not found.")
        return redirect('providers:dashboard')

    # ❗ Prevent deleting booked slots
    if Booking.objects(slot=slot).count() > 0:
        messages.error(request, "Cannot delete slot because it already has bookings!")
        return redirect('providers:dashboard')

    slot.delete()
    messages.success(request, "Slot deleted successfully!")
    return redirect('providers:dashboard')


# ---------------------- BOOKED CUSTOMERS ----------------------
def booked_customers(request):
    provider_id = request.session.get('provider_id')
    if not provider_id:
        return redirect('providers:login')

    provider = Provider.objects(id=provider_id).first()
    services = Service.objects(provider=provider)
    slots = AvailabilitySlot.objects(service__in=services)

    bookings = Booking.objects(slot__in=slots).order_by('-booked_at')

    return render(request, 'providers/booked_customers.html', {
        'provider': provider,
        'bookings': bookings
    })


# ---------------------- LOGOUT ----------------------
def logout_view(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect('providers:login')
