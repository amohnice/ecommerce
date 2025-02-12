from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Sum
from django.core.mail import send_mail
from .models import Product, Cart, CartItem, Order, Wishlist, Review, Coupon, Profile, OrderItem
import requests, datetime
from django.conf import settings
from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)

# Home
def home(request):
    return render(request, 'home.html')

# Authentication
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Error occurred during registration. Please try again.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Products
def product_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if category:
        products = products.filter(category=category)

    return render(request, 'product_list.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'product_detail.html', {'product': product, 'reviews': reviews})

# Cart
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        # Get the product object
        product = get_object_or_404(Product, id=product_id)

        # Get the quantity from the form, default to 1 if not provided
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                raise ValueError("Quantity must be at least 1.")
        except (ValueError, TypeError):
            quantity = 1  # Default to 1 if the quantity is invalid

        # Ensure the user's cart exists
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Try to get or create a CartItem for the user and product
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}  # Set the quantity if the item is created
        )

        if not created:
            # If the item is already in the cart, update the quantity
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, f'Updated {product.name} quantity in your cart.')
        else:
            # If it's a new cart item, set the quantity
            messages.success(request, f'{product.name} added to your cart.')

        # Redirect to the cart page
        return redirect('cart')


@login_required
def view_cart(request):
    # Ensure the user's cart exists
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('product_list')  # Redirect to products list if no cart is found

    cart_items = CartItem.objects.filter(cart=cart)  # Get the related CartItems for the user's cart
    total = sum(item.product.price * item.quantity for item in cart_items)  # Compute total for all items in the cart

    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'total': total})

@login_required
def update_cart(request, product_id):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Get the new quantity from the form
        quantity = int(request.POST['quantity'])

        # Get the product
        product = Product.objects.get(id=product_id)

        # Check if requested quantity exceeds stock
        if quantity > product.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('cart')

        # Check if the cart contains the item
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()

        if cart_item:
            if quantity > 0:
                # Update quantity and recalculate total price
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated successfully.')
            else:
                # Remove the item from the cart if quantity is 0
                cart_item.delete()
                messages.success(request, 'Item removed from cart.')
        else:
            messages.error(request, 'Item not found in cart.')

        return redirect('cart')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = Cart.objects.filter(user=request.user, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
            messages.success(request, 'Item removed from cart.')
        return redirect('cart')

@login_required
def checkout(request):
    # Retrieve the cart items for the current user
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        # If no items in the cart, redirect to the homepage or a relevant page
        return redirect('home')  # Change 'home' to the name of your homepage view

    # Calculate the total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Handle POST request for coupon code and phone number
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        phone = request.POST.get('phone')

        # Validate the coupon
        coupon = None
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, active=True, valid_from__lte=timezone.now(), valid_to__gte=timezone.now())
            except Coupon.DoesNotExist:
                messages.error(request, 'Invalid or expired coupon code.')

        # Apply the discount if the coupon is valid
        if coupon:
            total_price -= (total_price * coupon.discount / 100)
            messages.success(request, f'Coupon applied: {coupon.code} ({coupon.discount}% off)')

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='Pending'
        )

        # Add items from the cart to the order
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )

        # Clear the cart
        cart_items.delete()

        # Redirect to payment or order confirmation
        return redirect('payment')  # You can adjust this to your desired URL

    # If the method is GET, simply render the checkout page with cart items and total price
    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        amount = request.POST.get('amount')

        # Generate a dynamic timestamp in the required format (yyyyMMddHHmmss)
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

        headers = {
            'Authorization': f'Bearer {settings.MPESA_ACCESS_TOKEN}',
            'Content-Type': 'application/json',
        }

        payload = {
            'BusinessShortCode': settings.MPESA_SHORTCODE,
            'Password': settings.MPESA_PASSWORD,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': amount,
            'PartyA': phone,
            'PartyB': settings.MPESA_SHORTCODE,
            'PhoneNumber': phone,
            'CallBackURL': 'https://yourdomain.com/callback',  # Make sure this is a valid URL
            'AccountReference': 'E-commerce',
            'TransactionDesc': 'Payment for order',
        }

        try:
            # Send request to M-Pesa STK Push API
            response = requests.post(
                'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',  # Use the sandbox URL for testing
                headers=headers,
                json=payload,
            )

            if response.status_code == 200:
                # Handle successful response (return success page or redirect)
                return redirect('payment_success')
            else:
                # Log error or return failed payment page
                return redirect('payment_failed')
        except requests.exceptions.RequestException as e:
            # Log the error and return a failure page
            print(f"Error occurred: {e}")
            return redirect('payment_failed')

    return render(request, 'payment.html')

def payment_success(request):
    return render(request, 'payment_success.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')


def mpesa_callback(request):
    if request.method == 'POST':
        # M-Pesa sends a POST request with the payment details
        mpesa_response = request.body.decode('utf-8')  # You may need to parse this JSON properly

        # Optionally, log the response for debugging
        print(mpesa_response)

        # Here, you can handle the response data, such as updating the order status, etc.
        # You will want to check for success or failure and take appropriate action

        return JsonResponse({"Message": "Success"})
    return JsonResponse({"Message": "Failure"}, status=400)

# Orders
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

def send_order_confirmation(order):
    subject = 'Order Confirmation'
    message = f'Thank you for your order! Your order ID is {order.id}. Total: KES {order.total_price}.'
    send_mail(subject, message, 'your_email@gmail.com', [order.user.email])

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'track_order.html', {'order': order})

# Wishlist
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f'{product.name} added to wishlist.')
    return redirect('wishlist')

@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def remove_from_wishlist(request, product_id):
    # Assuming the user is authenticated and has a wishlist model
    if request.user.is_authenticated:
        try:
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=product_id)
            wishlist_item.delete()
        except Wishlist.DoesNotExist:
            pass  # Optionally handle if the item doesn't exist
    return redirect('wishlist')  # Redirect to the wishlist page

# Reviews
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST['rating']
        comment = request.POST['comment']
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return redirect('product_detail', product.id)
    return render(request, 'add_review.html', {'product': product})

# Profile
@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        profile.phone = request.POST['phone']
        profile.address = request.POST['address']
        profile.save()
        return redirect('profile')
    return render(request, 'profile.html', {'profile': profile})

# Coupons
@login_required
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        try:
            coupon = Coupon.objects.get(code=code, active=True)
            # Apply discount logic here
            return redirect('cart')
        except Coupon.DoesNotExist:
            return redirect('cart')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    total_sales = Order.objects.aggregate(total_sales=Sum('total_price'))['total_sales']
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    return render(request, 'admin_dashboard.html', {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_users': total_users,
    })

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders})

def contact_us(request):
    if request.method == 'POST':
        # Handle form submission (e.g., send an email)
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        # Add logic to send an email or save the message to the database
        return redirect('contact_us')
    return render(request, 'contact_us.html')


# Check if the user is an admin
def is_admin(user):
    return user.is_staff

# Admin Dashboard
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# Product Management
@login_required
@user_passes_test(is_admin)
def manage_products(request):
    products = Product.objects.all()
    return render(request, 'admin/manage_products.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        stock = request.POST.get('stock')  # Ensure stock is part of the form

        # Validate that required fields are filled
        if not name or not description or not price or not category or not stock or not image:
            messages.error(request, 'All fields are required!')
            return redirect('add_product')  # Stay on the add product page if validation fails

        try:
            # Ensure the price and stock are valid
            price = float(price)
            stock = int(stock)

            # Create product
            Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                image=image,
                stock=stock  # Don't forget to save stock as well
            )
            messages.success(request, 'Product added successfully!')
            return redirect('manage_products')  # Redirect to the manage products page after successful creation

        except ValueError:
            messages.error(request, 'Invalid price or stock value.')
            return redirect('add_product')  # Stay on the page if there's an error with the values

    return render(request, 'admin/add_product.html')

@login_required
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        logger.info(f"Updating product: {product.name}")
        logger.info(f"Form data: {request.POST}")
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category = request.POST.get('category')
        product.stock = int(request.POST.get('stock', 0))  # Ensure stock is updated
        if 'image' in request.FILES:
            product.image = request.FILES['image']
        product.save()
        messages.success(request, f'{product.name} updated successfully.')
        return redirect('manage_products')
    return render(request, 'admin/edit_product.html', {'product': product})

@login_required
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('manage_products')

# Order Management
@login_required
@user_passes_test(is_admin)
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'admin/manage_orders.html', {'orders': orders})

@login_required
@user_passes_test(is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.status = status
        order.save()
        return redirect('manage_orders')
    return render(request, 'admin/update_order_status.html', {'order': order})

# Coupon Management
@login_required
@user_passes_test(is_admin)
def manage_coupons(request):
    coupons = Coupon.objects.all()
    return render(request, 'admin/manage_coupons.html', {'coupons': coupons})

@login_required
@user_passes_test(is_admin)
def add_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        valid_from = request.POST.get('valid_from')
        valid_to = request.POST.get('valid_to')
        active = request.POST.get('active') == 'on'
        Coupon.objects.create(
            code=code,
            discount=discount,
            valid_from=valid_from,
            valid_to=valid_to,
            active=active
        )
        return redirect('manage_coupons')
    return render(request, 'admin/add_coupon.html')

@login_required
@user_passes_test(is_admin)
def edit_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == 'POST':
        coupon.code = request.POST.get('code')
        coupon.discount = request.POST.get('discount')
        coupon.valid_from = request.POST.get('valid_from')
        coupon.valid_to = request.POST.get('valid_to')
        coupon.active = request.POST.get('active') == 'on'
        coupon.save()
        return redirect('manage_coupons')
    return render(request, 'admin/edit_coupon.html', {'coupon': coupon})

@login_required
@user_passes_test(is_admin)
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    return redirect('manage_coupons')

# Review Management
@login_required
@user_passes_test(is_admin)
def manage_reviews(request):
    reviews = Review.objects.all()
    return render(request, 'admin/manage_reviews.html', {'reviews': reviews})

@login_required
@user_passes_test(is_admin)
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    review.delete()
    return redirect('manage_reviews')

# Wishlist Management
@login_required
@user_passes_test(is_admin)
def manage_wishlists(request):
    wishlists = Wishlist.objects.all()
    return render(request, 'admin/manage_wishlists.html', {'wishlists': wishlists})

# Profile Management
@login_required
@user_passes_test(is_admin)
def manage_profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'admin/manage_profiles.html', {'profiles': profiles})