from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Authentication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),

    # Cart
    path('cart/', views.view_cart, name='cart'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Checkout and Payment
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.initiate_payment, name='payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    path('callback/', views.mpesa_callback, name='mpesa_callback'),

    # Orders
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),

    # Wishlist
    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Reviews
    path('review/<int:product_id>/', views.add_review, name='add_review'),

    # Profile
    path('profile/', views.profile, name='profile'),

    # Coupons
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),

    path('orders/', views.order_history, name='orders'),  # Order history page
    path('contact-us/', views.contact_us, name='contact_us'),  # Contact Us page

    # Admin Dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Product Management
    path('admin-dashboard/products/', views.manage_products, name='manage_products'),
    path('admin-dashboard/products/add/', views.add_product, name='add_product'),
    path('admin-dashboard/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('admin-dashboard/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),

    # Order Management
    path('admin-dashboard/orders/', views.manage_orders, name='manage_orders'),
    path('admin-dashboard/orders/update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),

    # Coupon Management
    path('admin-dashboard/coupons/', views.manage_coupons, name='manage_coupons'),
    path('admin-dashboard/coupons/add/', views.add_coupon, name='add_coupon'),
    path('admin-dashboard/coupons/edit/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('admin-dashboard/coupons/delete/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),

    # Review Management
    path('admin-dashboard/reviews/', views.manage_reviews, name='manage_reviews'),
    path('admin-dashboard/reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),

    # Wishlist Management
    path('admin-dashboard/wishlists/', views.manage_wishlists, name='manage_wishlists'),

    path('admin-dashboard/categories/', views.manage_categories, name='manage_categories'),
    path('admin-dashboard/add/category/', views.add_category, name='add_category'),
    path('admin-dashboard/edit/category/<int:id>/', views.edit_category, name='edit_category'),
    path('admin-dashboard/delete/category/<int:id>/', views.delete_category, name='delete_category'),

    # Profile Management
    path('admin-dashboard/profiles/', views.manage_profiles, name='manage_profiles'),
]