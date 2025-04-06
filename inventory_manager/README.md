# Beverage Store Management System

## Overview
This Streamlit-based web application is a comprehensive management system for a beverage store. It features both customer-facing and employee-facing interfaces with a shared SQLite database backend.

## Features

### Customer Interface
- Browse beverage inventory with category filtering
- Add items to cart with quantity selection
- View and modify shopping cart
- Complete checkout process with shipping and payment information
- View order history for the current session

### Employee Interface
- Secure login system for employees
- Comprehensive inventory management
  - View current inventory
  - Add new items to the catalog
  - Edit existing items
  - Delete items (with confirmation)
- Sales reporting
  - View transaction history
  - See detailed order information
  - Export data to CSV

## Project Structure
- `main.py` - Entry point for the application
- `db_setup.py` - Database initialization and setup
- `customer.py` - Customer-facing interface and functionality
- `employee.py` - Employee interface with inventory management
- `cart.py` - Shopping cart functionality and transaction processing

## Database Schema
The application uses SQLite with the following tables:
- `catalog` - Store inventory items
- `cart` - Temporary shopping cart storage
- `transactions` - Completed orders
- `transaction_items` - Items within completed orders
- `employees` - Employee login credentials

## How to Run
1. Ensure you have Python and Streamlit installed
2. Install required dependencies: `pip install streamlit pandas sqlite3`
3. Run the application: `streamlit run main.py`
4. Access the application through your browser at the provided URL

## Default Login Credentials
For testing/demo purposes, you can log in as an employee using:
- Username: `username`
- Password: `password`

## Future Improvements
- User account creation and login for customers
- Persistent order history for registered customers
- Enhanced inventory reporting and analytics
- Product image support
- Advanced search functionality
