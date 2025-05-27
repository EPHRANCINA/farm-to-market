from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, ProductImage
from .forms import ProductForm, ProductImageForm

@login_required(login_url='users:login')
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/dashboard.html', {
        'products': products,
        'title': 'Dashboard'
    })

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.seller = request.user
            
            # Update user profile with seller information
            user = request.user
            user.first_name = product_form.cleaned_data['seller_name'].split()[0] if ' ' in product_form.cleaned_data['seller_name'] else product_form.cleaned_data['seller_name']
            user.last_name = ' '.join(product_form.cleaned_data['seller_name'].split()[1:]) if ' ' in product_form.cleaned_data['seller_name'] else ''
            user.email = product_form.cleaned_data['seller_email']
            user.phone_number = product_form.cleaned_data['seller_phone']
            user.address = product_form.cleaned_data['seller_address']
            user.save()
            
            product.save()
            
            # Handle multiple images
            if image_form.is_valid() and request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=image)
            
            messages.success(request, 'Product created successfully!')
            return redirect('products:dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        # Pre-fill seller information from user profile
        initial_data = {
            'seller_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'seller_email': request.user.email,
            'seller_phone': request.user.phone_number or '',
            'seller_address': request.user.address or '',
        }
        product_form = ProductForm(initial=initial_data)
        image_form = ProductImageForm()
    
    return render(request, 'products/form.html', {
        'form': product_form,
        'image_form': image_form,
        'action': 'Create'
    })

@login_required(login_url='users:login')
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})

@login_required(login_url='users:login')
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if product_form.is_valid():
            product = product_form.save()
            
            # Handle multiple images
            if image_form.is_valid() and request.FILES.getlist('images'):
                for image in request.FILES.getlist('images'):
                    ProductImage.objects.create(product=product, image=image)
            
            return redirect('products:dashboard')
    else:
        product_form = ProductForm(instance=product)
        image_form = ProductImageForm()
    
    return render(request, 'products/form.html', {
        'form': product_form,
        'image_form': image_form,
        'action': 'Update'
    })

@login_required(login_url='users:login')
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('products:list')
    return render(request, 'products/confirm_delete.html', {'product': product})

@login_required(login_url='users:login')
def verify_id(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        action = request.POST.get('action')
        
        if not id_number:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter your ID number'
            })
        
        # Here you would typically verify the ID number
        # For now, we'll just redirect based on the action
        if action == 'buy':
            return JsonResponse({
                'status': 'success',
                'redirect': '/products/'
            })
        else:  # sell
            return JsonResponse({
                'status': 'success',
                'redirect': '/products/create/'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    })
