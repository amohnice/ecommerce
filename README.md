## Directory structure:
└── amohnice-e-commerce/
    ├── db.sqlite3
    ├── manage.py
    ├── requirements.txt
    ├── ecommerce/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── __pycache__/
    ├── media/
    │   └── products/
    └── store/
        ├── __init__.py
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        ├── views.py
        ├── __pycache__/
        ├── migrations/
        │   ├── 0001_initial.py
        │   ├── 0002_cart_order_orderitem_order_products.py
        │   ├── 0003_coupon_profile_review_wishlist.py
        │   ├── 0004_order_coupon.py
        │   ├── 0005_cart_created_at_product_stock_cartitem.py
        │   ├── 0006_remove_cart_product_remove_cart_quantity_and_more.py
        │   ├── __init__.py
        │   └── __pycache__/
        ├── static/
        │   └── images/
        └── templates/
            ├── add_review.html
            ├── admin_dashboard.html
            ├── base.html
            ├── cart.html
            ├── checkout.html
            ├── contact_us.html
            ├── home.html
            ├── login.html
            ├── order_detail.html
            ├── orders.html
            ├── payment.html
            ├── payment_failed.html
            ├── payment_success.html
            ├── product_detail.html
            ├── product_list.html
            ├── profile.html
            ├── register.html
            ├── track_order.html
            ├── wishlist.html
            └── admin/
                ├── add_coupon.html
                ├── add_product.html
                ├── edit_coupon.html
                ├── edit_product.html
                ├── manage_coupons.html
                ├── manage_orders.html
                ├── manage_products.html
                ├── manage_profiles.html
                ├── manage_reviews.html
                ├── manage_wishlists.html
                └── update_order_status.html
