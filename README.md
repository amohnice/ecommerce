## Installation

1. Clone the Repository
(git clone https://github.com/amohnice/E-Commerce.git)
cd E-Commerce

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

Visit http://127.0.0.1:8000/ in your browser to access the application.

## Features

    User authentication (login, register, profile management)
    Browse and filter products
    Add products to cart and proceed to checkout
    Payment gateway integration (success/failure pages)
    Admin dashboard to manage products, orders, users, coupons, and more
    Reviews and ratings for products
    Wishlist functionality
    Order tracking and management

## Contributing

Feel free to fork this repository, create a branch, and submit pull requests. Please make sure to follow the coding conventions and write tests for new features.

