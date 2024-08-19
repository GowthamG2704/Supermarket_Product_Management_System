
# MySQL Shopping Cart Project

This Python project allows users to interact with a MySQL database to manage a shopping cart. It supports adding products to the cart and checking out, among other functionalities.

# Description:

The **"Supermarket Product Management System"** is a Python-based application designed to streamline the management of supermarket inventory and sales operations. This system enables efficient tracking and processing of products, from adding items to a virtual cart to managing stock levels and generating sales reports. By integrating with a MySQL database, the system ensures accurate and up-to-date information on product availability, pricing, and sales performance, making it an essential tool for supermarket management.


## Features

- **Add Products to Cart**: Users can add products by specifying the product name and quantity. The script checks the availability of the product in the database.
- **View Cart**: Displays the list of products currently in the cart along with their details.
- **Checkout**: Finalizes the purchase and updates the database accordingly.

## Languages Used

- Python
- MySQL

  
## Requirements

- Python 3.x
- MySQL
- Required Python packages:
  - `pymysql`
  - `tabulate`
  - `uuid`

## Setup Instructions

1. **Install Python Packages**:
    ```bash
    pip install pymysql tabulate
    ```

2. **Database Configuration**:
    - Replace the placeholders (`your_user_name`, `your_password`, `your_database_name`) in the script with your actual MySQL credentials.

3. **Run the Script**:
    ```bash
    python project.py
    ```

## Usage

- The script will prompt you to enter product details like the product name and quantity.
- You can view the cart and proceed to checkout using the provided options.

## Notes

- Ensure the MySQL database is set up with the required schema and data before running the script.
- The script includes basic error handling for common issues like invalid product names or insufficient stock.

## License

This project is licensed under the MIT License.


