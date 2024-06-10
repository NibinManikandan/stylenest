# E-Commerce Platform

This is a fully functional and responsive e-commerce platform built using Python and Django for the backend and HTML, CSS, JavaScript, jQuery, Ajax, and Bootstrap for the frontend. The platform provides a user-friendly interface for customers and a comprehensive admin dashboard for managing the store.

## Features

### Customer Side
- **Razorpay Payment Integration:** Secure and seamless payment processing with Razorpay.
- **Repayment Option:** Refunds available if the payment is cancelled.
- **Wallet Payment and Recharge:** Customers can pay using their wallet and recharge it as needed.
- **User Authentication:** Secure login and registration for users.
- **Coupons:** Apply discount coupons at checkout.
- **Category and Product Offers:** Special offers based on categories and individual products.
- **Delivery Charges:** Dynamic calculation of delivery charges.
- **Online Payment Amount Limitations:** Restrict minimum and maximum order amounts for online payments.
- **Order Tracking:** Track the status of orders in real-time.

### Admin Side
- **Dashboard:**
  - Top 5 Selling Products
  - Top Selling Categories
  - Revenue Statistics
  - User Rate
  - Selling Rate
- **Product Management:**
  - Add, Edit, and List Products
  - Manage Product Visibility (List/Unlist)
- **Category Management:**
  - Add, Edit, List, and Unlist Categories
  - Create Category-Specific Offers
- **User Management:**
  - View User Details
  - Manage User Visibility (List/Unlist)
- **Coupon Management:**
  - Create, List, and Unlist Coupons
- **Banner Management:**
  - Create, List, and Unlist Banners
- **Reports:**
  - Download Sales Report (PDF/XLS)
  - Download Products Report (PDF/XLS)
  - Download Cancelled Products Report (PDF/XLS)
- **Order Management:**
  - View Order Status
  - Change Order Status

## Technologies Used

### Backend
- **Python**
- **Django**

### Frontend
- **HTML**
- **CSS**
- **JavaScript**
- **jQuery**
- **Ajax**
- **Bootstrap**

## Project Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/ecommerce-platform.git
    cd ecommerce-platform
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run database migrations:**
    ```sh
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```sh
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```sh
    python manage.py runserver
    ```

7. **Access the application:**
    - Customer Side: `http://127.0.0.1:8000/`
    - Admin Dashboard: `http://127.0.0.1:8000/admin/`

## Usage

### Customer Side
Customers can search products by category or product name also filter by the price variations high to low and low to high and by category, add them to their cart, apply coupons, choose payment methods, and track their orders. The platform supports wallet payments, secure online transactions via Razorpay, and order tracking.

### Admin Side
Admins can manage the entire e-commerce platform through the admin dashboard. They can add, edit, and manage products and categories, view user details, create and manage offers and coupons, monitor sales and revenue, and generate reports.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact me at [nibin2319@gmail.com](mailto:nibin2319@gmail.com).

## live demo
Check out the live demo of the project at [StyleNest](https://stylenest.cloud)
---

Thank you for checking out my e-commerce platform project! I look forward to your feedback and contributions.
