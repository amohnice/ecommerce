## Installation Guide

1. Clone the Repository

       git clone (https://github.com/amohnice/ecommerce.git)

       cd ecommerce

2. Create a Virtual Environment

       python3 -m venv venv

       source venv/bin/activate  # On Windows, use venv\Scripts\activate

3. Install Dependencies

        pip install -r requirements.txt

4. Set Up the Database

        python manage.py migrate

5. Create a Superuser (Optional, for Admin Access)
    
        python manage.py createsuperuser

6. Run the Development Server

        python manage.py runserver

- Visit http://127.0.0.1:8000/ in your browser to access the application.
- Visit http://127.0.0.1:8000/admin in your browser to access the admin-site.
- Admin-site: Username: - admin
              password: - admin123
- Alternatively, you can log in to the admin interface using the credentials above.

## Features

1. User authentication (login, register, profile management)
2. Browse and filter products
3. Add products to cart and proceed to checkout
4. M-Pesa Payment gateway integration (success/failure pages)
5. Admin dashboard to manage products, orders, users, coupons, and more
6. Reviews and ratings for products
7. Wishlist functionality
8. Order tracking and management

## Contributing

Feel free to fork this repository, create a branch, and submit pull requests. Please make sure to follow the coding conventions and write tests for new features.

## Deployment 
- **It is a readonly database**

- Live demo[(https://ecommerce-puce-kappa.vercel.app/)]
- Pitch deck presentation[(https://www.canva.com/design/DAGe_gxykTQ/hGXemfEzN4W-2LC76dQQHA/view?utm_content=DAGe_gxykTQ&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hcce5ae2d14)]

