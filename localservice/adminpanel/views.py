from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from bson.objectid import ObjectId
from .models import AdminUser, Category, Provider, Customer, Service, Review
from providers.models import Provider, Service



# ---------------- Helper Decorator ---------------- #
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            return redirect('adminpanel:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# ---------------- Admin Authentication ---------------- #
def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = AdminUser.objects(email=email).first()
        if admin and admin.check_password(password):
            request.session['admin_id'] = str(admin.id)
            request.session['admin_name'] = admin.name
            return redirect('adminpanel:dashboard')
        else:
            return render(request, 'adminpanel/login.html', {'error': 'Invalid credentials'})
    return render(request, 'adminpanel/login.html')


@login_required
def admin_logout(request):
    request.session.flush()
    return redirect('adminpanel:login')


# ---------------- Dashboard ---------------- #
@login_required
def dashboard(request):
    counts = {
        'providers': Provider.objects.count(),
        'customers': Customer.objects.count(),
        'services': Service.objects.count(),
        'reviews': Review.objects.count(),
        'categories': Category.objects.count(),
    }
    return render(request, 'adminpanel/dashboard.html', {'counts': counts})


# ---------------- Categories ---------------- #
@login_required
def list_categories(request):
    cats = Category.objects.order_by('-created_at')
    return render(request, 'adminpanel/list_categories.html', {'categories': cats})


@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description')
        if name:
            Category(name=name, description=desc).save()
            return redirect('adminpanel:categories')
    return render(request, 'adminpanel/add_category.html')


@login_required
@require_POST
def delete_category(request, cat_id):
    cat = Category.objects(id=ObjectId(cat_id)).first()
    if cat:
        cat.delete()
    return redirect('adminpanel:categories')


# ---------------- Providers ---------------- #
@login_required
def list_providers(request):
    providers = Provider.objects.order_by('-created_at')
    prov_data = []

    for p in providers:
        # Fetch all services by this provider
        services = Service.objects(provider=p)
        prov_data.append({
            'provider': p,
            'services': services
        })

    return render(request, 'adminpanel/list_providers.html', {'prov_data': prov_data})



@login_required
@require_POST
def delete_provider(request, prov_id):
    prov = Provider.objects(id=ObjectId(prov_id)).first()
    if prov:
        # Remove all services of this provider
        Service.objects(provider=prov).delete()
        prov.delete()
    return redirect('adminpanel:providers')


# ---------------- Customers ---------------- #
@login_required
def list_customers(request):
    customers = Customer.objects.order_by('-created_at')
    return render(request, 'adminpanel/list_customers.html', {'customers': customers})


@login_required
@require_POST
def delete_customer(request, cust_id):
    cust = Customer.objects(id=ObjectId(cust_id)).first()
    if cust:
        Review.objects(customer=cust).delete()
        cust.delete()
    return redirect('adminpanel:customers')


# ---------------- Services ---------------- #
@login_required
def list_services(request):
    services = Service.objects.order_by('-created_at')
    return render(request, 'adminpanel/list_services.html', {'services': services})



@login_required
def remove_duplicate_services(request):
    seen = {}
    duplicates = []
    for s in Service.objects:
        key = (s.title.strip().lower(), str(s.provider.id) if s.provider else None)
        if key in seen:
            duplicates.append(s)
        else:
            seen[key] = s
    for d in duplicates:
        d.delete()
    return redirect('adminpanel:services')


# ---------------- Reviews ---------------- #
@login_required
def list_reviews(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'adminpanel/list_reviews.html', {'reviews': reviews})
