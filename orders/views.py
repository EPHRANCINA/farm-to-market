from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
@transaction.atomic
def order_create(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity <= 0 or quantity > product.quantity:
        messages.error(request, 'Invalid quantity.')
        return redirect('products:detail', pk=product_pk)
    
    order = Order.objects.create(
        user=request.user,
        total_amount=product.price * quantity
    )
    
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=quantity,
        price=product.price
    )
    
    product.quantity -= quantity
    product.save()
    
    messages.success(request, 'Order placed successfully!')
    return redirect('orders:detail', pk=order.pk)

@login_required
def order_cancel(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'Only pending orders can be cancelled.')
    return redirect('orders:detail', pk=order.pk)
