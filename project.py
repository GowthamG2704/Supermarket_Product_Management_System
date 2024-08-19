#importing Modules

import pymysql
import uuid
from tabulate import tabulate

#For Connect to MYSQL Database

try:
    connection = pymysql.connect(
        host = 'localhost',
        user = 'your_user_name', #Replace with Your User Name
        password = 'your_password', #Replace with Your Password
        database = 'your_database_name' #Replace with Your Database Name
        )
except pymysql.Error as err:
    print(f"\nError :{err}.")
    
cursor = connection.cursor()

cart =[]

#Function for add Product to cart

def add_to_cart():

    try:
        Product_Name = input("Enter Product Name :").strip().capitalize()

        if not Product_Name:
            print("\nProduct Name cannot be empty.")
            return

        quantity =int(input("Enter Quantity :"))
        print()

        cursor.execute(f"""
            select Unit_Price, Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)
        result = cursor.fetchone()

        if result:
            Unit_Price, Quantity = result

            if quantity > 0:

                if Quantity >= quantity :

                    cart.append((Product_Name,quantity))
                    total_price = Unit_Price * quantity 

                    cursor.execute("""INSERT INTO cart_data ( Product_Name, Unit_Sold, Unit_Price, Price)
                    VALUES (%s, %s, %s, %s)""",
                    (Product_Name, quantity, Unit_Price, total_price))

                    connection.commit()

                    print(f"Added {quantity} units of {Product_Name} to the cart.")

                else:
                    print("Insufficient Stock.")

            else:
                print("Quantity Must Be More Than Zero.")

        else:
            print(f"{Product_Name} is Unavailable.") 

    except ValueError:
        print("\nInvalid Input. Plese Enter The valid Quantity (numeric value)...")

    except Exception as err:
        print(f"\nError : {err}.")
        

#Function for edit Product in cart

def edit_cart():

    try :
        Product_Name = input("Enter Product Name :").strip().capitalize()

        if not Product_Name:
            print("\nProduct Name cannot be empty.")
            return

        New_quantity =int(input("Enter New Quantity :"))
        print()

        cursor.execute(f"""
            select Unit_Price, Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)

        result = cursor.fetchone()

        if result:
            Unit_Price, Quantity = result

            if New_quantity > 0:

                if Quantity >= New_quantity :

                    for i, (name, _ ) in enumerate(cart):

                        if name == Product_Name:

                            cart[i] = (name, New_quantity)
                            new_price = Unit_Price * New_quantity 

                            cursor.execute("""
                                UPDATE cart_data
                                SET Unit_Sold = %s, Price = %s
                                WHERE Product_Name = %s
                                """,
                                (New_quantity, new_price, Product_Name))

                            connection.commit()

                            print(f"Updated Quantity for {Product_Name} to {New_quantity}.")
                            break

                    else:
                        print(f"{Product_Name} Not found in the Cart.")

                else:
                    print("Insufficient Stock")

            else:
                print("Quantity Must Be More Than Zero.")

        else:
            print(f"{Product_Name} is Unavailable.")             

        
    except ValueError:
        print("\nInvalid Input Please Enter Valid Quantity (numeric Value)...")
    
    except Exception as err:
        print(f"\nError : {err}.")


#Function for remove Product in cart

def remove_from_cart():

    try :

        Product_Name = input("Enter Product Name :").strip().capitalize()
        print()

        if not Product_Name:
            print("Product name cannot be empty.")
            return

        cursor.execute(f"""
            select Unit_Price, Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)
        result = cursor.fetchone()

        if result:

            for i in cart:

                if i[0] == Product_Name:

                    cart.remove(i)
                    
                    cursor.execute("""
                        DELETE FROM cart_data
                        WHERE Product_Name = %s
                        """, (Product_Name,))

                    connection.commit()

                    print(f"Removed {Product_Name} From The cart.")
                    break

            else:
                print(f"{Product_Name} Not found in the Cart.")


        else:
            print(f"{Product_Name} is Unavailable.")  


    except Exception as err :
        print(f"\nError :{err}.")


#Function for buy Product in cart

def buy_products():
    
    try :

        if not cart:
            print("This cart is empty.")
            return

        total_amount = 0
        product_prices = {}

        order_id = str(uuid.uuid4())

        for Product_Name,quantity in cart:
            
            cursor.execute(f"select Product_id, Unit_Price, Quantity from products_data where Product_Name = '{Product_Name}'")
            Product_id, unit_price, existing_quantity = cursor.fetchone()
            product_prices[Product_Name] = unit_price
            total_price = unit_price * quantity
            total_amount += total_price
            
        for Product_Name, quantity in cart:

            cursor.execute("""INSERT INTO selling_data (Order_id,Product_id, Product_Name, Unit_Sold, Total_Cost)
                VALUES (%s, %s, %s, %s, %s)""",
                (order_id, Product_id, Product_Name, quantity, total_amount))

            new_quantity = existing_quantity - quantity

            cursor.execute(f"""
                UPDATE products_data
                SET Quantity = {new_quantity}
                WHERE Product_Name = '{Product_Name}'
                """)

        cart.clear()

        cursor.execute("TRUNCATE TABLE cart_data")
            
        connection.commit()

        print(f"Total amount for the Purchase: {total_amount:.2f}.")

        print(f"\nPurchase Details Stored With Order ID: {order_id}.")

    except Exception as err:
        print(f"Error :{err}.")

    except ValueError:
        print("Invalid Input Please Enter Valid Quantity (numeric Value)...")


#Function for view Product data from Database

def products_list():

    try:

        cursor.execute("SELECT * FROM products_data")
        result = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        print(tabulate(result, headers=headers, tablefmt="grid"))


    except Exception as err:

        print(f"Error: {err}")


#Function for view Sales data from Database

def sales():

    try:

        cursor.execute("SELECT * FROM selling_data")
        result = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        print(tabulate(result, headers=headers, tablefmt="grid"))


    except Exception as err:

        print(f"Error: {err}.")


#Function for view Cart data from Database

def view_cart():

    try:

        cursor.execute("SELECT * FROM cart_data")
        result = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]

        print(tabulate(result, headers=headers, tablefmt="grid"))

    except Exception as err:

        print(f"Error: {err}.")
        

#Function for add Product stocks to Database

def add_stock():

    try:

        Product_id = input("Enter Product ID :").upper()

        if not Product_id:
            print("\nProduct ID cannot be empty.")
            return

        Product_Name = input("Enter Product Name :").strip().capitalize()

        if not Product_Name:
            print("\nProduct name cannot be empty.")
            return

        Unit_Price = int(input("Enter Unit Price For the Product :"))

        if Unit_Price <= 0 :
            print("\nUnit Price Must be more than Zero.")
            return

        quantity =int(input("Enter Quantity :"))

        if quantity < 0 :
            print("\nQuantity Must be Positive.")
            return

        print()

        cursor.execute("""INSERT INTO products_data (Product_id, Product_Name, Unit_Price, Quantity)
                    VALUES (%s, %s, %s, %s)""",
                    (Product_id, Product_Name, Unit_Price, quantity))

        connection.commit()

        print(f"New Stock {Product_Name} is Added Successfully...")

    except ValueError as er:
        print("\nEnter Numeric Value.")

    except Exception as err:
        print(f"\nError: {err}.")


#Function for Update stock Quantity to Database

def update_stock():

    try:

        Product_Name = input("Enter product name :").strip().capitalize()

        if not Product_Name:
            print("\nProduct name cannot be empty.")
            return

        new_quantity =int(input("Enter quantity :"))
        print()

        cursor.execute(f"""
            select Unit_Price, Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)
        result = cursor.fetchone()

        if result:

            if new_quantity >= 0 :

                cursor.execute(f"""
                    UPDATE products_data
                    SET Quantity = {new_quantity}
                    WHERE Product_Name = '{Product_Name}'
                    """)

                connection.commit()

                print("Stock Updated Successfully...")

            else :
                print("Quantity Must be Positive.")

        else :
            print(f"{Product_Name} is Unavailable.")

    except ValueError as er:
        print("\nEnter Numeric Value.")

    except Exception as err:
        print(f"\nError: {err}.")


#Function for Update stock Price to Database

def update_price():

    try:

        Product_Name = input("Enter product name :").strip().capitalize()

        if not Product_Name:
            print("\nProduct name cannot be empty.")
            return

        Unit_Price = int(input("Enter Unit Price For the Product :"))
        print()

        cursor.execute(f"""
            select Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)
        result = cursor.fetchone()

        if result:

            if Unit_Price > 0 :

                cursor.execute(f"""
                    UPDATE products_data
                    SET Unit_Price = {Unit_Price}
                    WHERE Product_Name = '{Product_Name}'
                    """)

                connection.commit()

                print(f"Price of the Product {Product_Name} is Changed...")

            else :
                print("Unit Price Must be more than Zero.")

        else :
            print(f"{Product_Name} is Unavailable.")

    except ValueError as er:
        print("\nEnter Numeric Value.")

    except Exception as err:
        print(f"\nError: {err}.")


#Function for Delete Product from Database

def delete_product():

    try :
        Product_Name = input("Enter product name :").strip().capitalize()
        print()

        if not Product_Name:
            print("Product name cannot be empty.")
            return

        cursor.execute(f"""
            select Unit_Price, Quantity from products_data
            where Product_Name = '{Product_Name}' ;
        """)
        result = cursor.fetchone()

        if result:

            cursor.execute("""
                DELETE FROM products_data
                WHERE Product_Name = %s
                """, (Product_Name,))

            connection.commit()

            print(f"Product {Product_Name} is Deleted From The Stock Table Successfully...")

        else:
            print(f"{Product_Name} is Unavailable.")  

    except Exception as err :
        print(f"\nError :{err}.")

def done():

    cart.clear()

    cursor.execute("TRUNCATE TABLE cart_data")

    print("Thank You For Visiting Our Store... Have a Nice Day...")

    exit()

def user():

    while True:

        try:

            print("\nWelcome To Python Super Market")
            print()
            print("1. View Stocks")
            print("2. Add Product To Cart")
            print("3. Edit Cart")
            print("4. Remove Product From Cart")
            print("5. View cart")
            print("6. Buy Products From Cart")
            print("7. Exit")
            print()
            choice = int(input("Enter Your Choice (1-7): "))
            print()

            if choice == 1:
                products_list()

            elif choice == 2:
                add_to_cart()

            elif choice == 3:
                edit_cart()

            elif choice == 4:
                remove_from_cart()

            elif choice == 5:
                view_cart()

            elif choice == 6:
                buy_products()

            elif choice == 7:
                done()

            elif choice < 0 :
                print("Choice Must Be Positive.")

            else:
                print("Invalid Choice. Please Select a Valid Option (1-7).")

        except Exception as err:
            print("\nPlease Enter the Numeric Value (1-7).")


def manager():

    while True:

        try:

            print("\nWelcome To Python Super Market")
            print()
            print("1. View Stocks")
            print("2. Add New Stocks")
            print("3. Update Stock Quantity")
            print("4. Update Stock Price")
            print("5. Delete Product")
            print("6. View Sales Record")
            print("7. Exit")
            print()
            choice = int(input("Enter Your Choice (1-7): "))
            print()

            if choice == 1:
                products_list()

            elif choice == 2:
                add_stock()

            elif choice == 3:
                update_stock()

            elif choice == 4:
                update_price()

            elif choice == 5:
                delete_product()

            elif choice == 6:
                sales()

            elif choice == 7:
                
                print("Thank You For Your Contribution...")
                exit()

            elif choice < 0 :
                print("Choice Must Be Positive.")

            else:
                print("Invalid Choice. Please Select a Valid Option (1-7).")

        except Exception as err:
            print("\nPlease Enter the Numeric Value (1-7).")


while True:

        try:

            print("\nWelcome To Python Super Market")
            print()
            print("1. Login as a Manager")
            print("2. Login as a Customer")
            print("3. Exit")
            print()
            choice = int(input("Enter Your Choice (1-3): "))
            print()

            if choice == 1:
                manager()

            elif choice == 2:
                user()

            elif choice == 3:
                
                print("Thank You... Have a Nice Day...")
                exit()

            elif choice < 0 :
                print("Choice Must Be Positive.")

            else:
                print("Invalid Choice. Please Select a Valid Option (1-3).")

        except Exception as err:
            print("\nPlease Enter the Numeric Value (1-3).")


connection.close()