from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from providers.models import Provider, Service, AvailabilitySlot, Booking
from datetime import datetime

# ---------------- Signup ----------------
def customer_signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if Customer.objects(email=email).first():
            messages.error(request, "Email already registered!")
            return redirect("customers:signup")

        Customer(name=name, email=email, password=password, phone=phone).save()
        messages.success(request, "Signup successful! Please login.")
        return redirect("customers:login")

    return render(request, "customers/signup.html")


# ---------------- Login ----------------
def customer_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        customer = Customer.objects(email=email, password=password).first()

        if customer:
            request.session["customer_id"] = str(customer.id)
            request.session["customer_name"] = customer.name
            return redirect("customers:dashboard")

        messages.error(request, "Invalid credentials!")

    return render(request, "customers/login.html")


# ---------------- Logout ----------------
def customer_logout(request):
    request.session.flush()
    return redirect("customers:login")


# ---------------- Dashboard ----------------
def customer_dashboard(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("customers:login")

    customer = Customer.objects(id=customer_id).first()
    approved_providers = Provider.objects(is_approved=True)
    services = Service.objects(provider__in=approved_providers)

    return render(request, "customers/dashboard.html", {
        "customer": customer,
        "services": services
    })


# ---------------- View slots for a service ----------------
def view_slots(request, service_id):
    service = Service.objects(id=service_id).first()
    slots = AvailabilitySlot.objects(service=service).order_by("date")
    return render(request, "customers/slots.html", {
        "service": service,
        "slots": slots
    })


# ---------------- Book a slot ----------------
def book_slot(request, slot_id):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("customers:login")

    customer = Customer.objects(id=customer_id).first()
    slot = AvailabilitySlot.objects(id=slot_id).first()

    # Prevent double booking
    if Booking.objects(slot=slot).first():
        messages.error(request, "This slot is already booked!")
        return redirect("customers:dashboard")

    Booking(slot=slot, customer_name=customer.name, customer_email=customer.email, customer_phone=customer.phone).save()
    messages.success(request, "Slot booked successfully!")
    return redirect("customers:my_bookings")


# ---------------- My bookings ----------------
def my_bookings(request):
    customer_id = request.session.get("customer_id")
    if not customer_id:
        return redirect("customers:login")

    customer = Customer.objects(id=customer_id).first()
    bookings = Booking.objects(customer_email=customer.email)

    valid_bookings = []
    for b in bookings:
        try:
            _ = b.slot  # access slot → will crash if missing
            valid_bookings.append(b)
        except:
            # remove corrupted booking
            b.delete()

    return render(request, "customers/my_bookings.html", {
        "bookings": valid_bookings
    })
