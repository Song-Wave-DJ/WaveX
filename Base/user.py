from datetime import datetime
import mysql.connector
import pymysql
import time
import uuid



class sql:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': '------',
            'host': 'localhost',
            'database': 'waveX'
        }
        self.connection = mysql.connector.connect(**self.config)
        self.cursor = self.connection.cursor()

    def Query(self, query, values=None):
        self.cursor.execute(query, values)
        result = self.cursor.fetchall()
        return result


def get_user_pass(user, password):
    s = sql()
    query = "SELECT * FROM universal WHERE username = %s AND password = %s"
    values = (user, password)
    result = s.Query(query, values)
    return result


def create_user(id, username, password, role, phone, name):
    import datetime

    # Get the current date
    today = datetime.date.today()
    formatted_date = today.strftime("%Y-%m-%d")

    s = sql()
    query = "INSERT INTO UNIVERSAL (id, username, password, role, phone_number, name , date_column ) VALUES (%s, %s, %s, %s, %s, %s , %s)"
    values = (id, username, password, role, phone, name, formatted_date)
    s.cursor.execute(query, values)
    s.connection.commit()
    return True


def delete_user(id):
    s = sql()
    query = f"delete from universal where Id = '{id}'"
    s.Query(query)
    s.connection.commit()
    return True


def get_waiter_detail(restaurantId):
    s = sql()
    query = "SELECT * FROM restaurant_waiter WHERE restaurant_id = %s"
    values = (restaurantId,)  # Pass the value as a single-element tuple
    result = s.Query(query, values)
    return result

def insert_waiter(restaurant_id, waiter_id, name, email, password, date, phone):
    try:
        role = 'waiter'
        s = sql()
        query = "INSERT INTO restaurant_waiter (restaurant_id, waiter_id, name, email, password, date , phone) VALUES (%s, %s, %s, %s, %s, %s , %s)"
        values = (restaurant_id, waiter_id, name, email, password, date, phone)
        s.Query(query, values)
        query = "INSERT INTO universal(id, username, password, role, phone_number, name, date_column, resId) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (waiter_id, email, password, role, phone, name, date, restaurant_id)
        s.Query(query, values)
        s.connection.commit()
        return True
    except  Exception as e:
        print(f"An exception occurred: {str(e)}")
        return False

def delete_waiter_res(restaurant_id, waiter_id):
    try:
        s = sql()  # Assuming you have a function or class to manage the database connection and cursor
        query = f"DELETE FROM  restaurant_waiter WHERE restaurant_id = '{restaurant_id}' AND waiter_id = '{waiter_id}'"
        s.Query(query)
        query = f"DELETE FROM universal where Id = '{waiter_id}'"
        s.Query(query)
        s.connection.commit()
        return True
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return False

def insert_menu(category_name, menu_name, price, discount, description, restaurant_id, type, available):
    s = sql()
    query = "INSERT INTO menu (category_name, menu_name, price, discount, description, restaurant_id,type , available) VALUES (%s, %s, %s,%s, %s,%s , %s,%s);"
    values = (category_name, menu_name, price, discount, description, restaurant_id, type, available)
    s.cursor.execute(query, values)
    s.connection.commit()


def get_menu_detail(restaurantId):
    s = sql()
    query = "SELECT * FROM menu WHERE restaurant_id = %s"
    values = (restaurantId,)  # Pass the value as a single-element tuple
    result = s.Query(query, values)
    return result


def delete_menu(restaurant_id, menu_name):
    s = sql()  # Assuming you have a function or class to manage the database connection and cursor
    query = "DELETE FROM menu WHERE restaurant_id = %s AND menu_name = %s"
    values = (restaurant_id, menu_name)
    s.cursor.execute(query, values)
    s.connection.commit()
    return True


def get_tables(restaurantId):
    s = sql()
    query = f"SELECT * FROM restaurant_tables WHERE restaurant_id = '{restaurantId}'"
    result = s.Query(query)
    return result


def set_tables(table_no, restaurant_id, url):
    s = sql()
    query = "insert into restaurant_tables(table_no , restaurant_id ,url ) values (%s,%s,%s)"
    values = (table_no, restaurant_id, url)  # Pass the value as a single-element tuple
    s.Query(query, values)
    s.connection.commit()


def delete_table(restaurant_id, table_no):
    s = sql()  # Assuming you have a function or class to manage the database connection and cursor
    query = "DELETE FROM restaurant_tables WHERE restaurant_id = %s AND table_no = %s"
    values = (restaurant_id, table_no)
    s.cursor.execute(query, values)

    # If you want to delete the corresponding entry from the "ALLOMENT" table as well, use the following code:
    query = "DELETE FROM ALLOTMENT WHERE RestaurantId = %s AND TableId = %s"
    s.cursor.execute(query, values)

    s.connection.commit()
    return True


def get_billing_history(id):
    s = sql()
    query = f"select * from billing_history where restaurant_id = '{id}'"
    result = s.Query(query)
    return result


def get_live_billing_history(id):
    s = sql()
    query = f"select * from billing_history where restaurant_id ='{id}' and payment_status='unpaid'"
    result = s.Query(query)
    return result


def show_orders(id):
    s = sql()
    query = "SELECT * FROM ORDERS where restaurant_id = %s"
    values = (id)
    result = s.Query(query, values)
    return result


def update_payment_status(id, order_id, new_status):
    s = sql()
    query = "UPDATE ORDERS SET payment_status = %s WHERE order_id = %s AND restaurant_id = %s ;"
    values = (new_status, order_id, id)
    result = s.Query(query, values)
    s.connection.commit()
    return result


def update_order_status(id, order_id, new_status):
    s = sql()
    query = "UPDATE ORDERS SET status = %s WHERE order_id = %s AND restaurant_id = %s ;"
    values = (new_status, order_id, id)
    result = s.Query(query, values)
    s.connection.commit()
    return result


def manager_one_day():
    s = sql()
    query = ""
    values = ()
    return s.Query(query, values)


# admin-dashboard
def manager_count():
    s = sql()  # Instantiate your SQL class

    # Define the SQL query and values
    query = "SELECT COUNT(*) FROM universal WHERE role = 'manager';"
    values = ()  # Empty tuple if you have no parameters

    # Use the Query method to execute the query
    result = s.Query(query, values)

    # Assuming that the Query method returns the count as a result
    count = result[0][0]  # Access the count from the result

    return count


def waiter_count():
    s = sql()  # Instantiate your SQL class

    # Define the SQL query and values
    query = "SELECT COUNT(*) FROM universal WHERE role = 'waiter';"
    values = ()  # Empty tuple if you have no parameters

    # Use the Query method to execute the query
    result = s.Query(query, values)

    # Assuming that the Query method returns the count as a result
    count = result[0][0]  # Access the count from the result

    return count


def customer_count():
    s = sql()  # Instantiate your SQL class

    # Define the SQL query and values
    query = "SELECT COUNT(*) FROM universal WHERE role = 'customer';"
    values = ()  # Empty tuple if you have no parameters

    # Use the Query method to execute the query
    result = s.Query(query, values)

    # Assuming that the Query method returns the count as a result
    count = result[0][0]  # Access the count from the result

    return count


def admin_count():
    s = sql()  # Instantiate your SQL class
    # Define the SQL query and values
    query = "SELECT COUNT(*) FROM universal WHERE role = 'admin';"
    values = ()  # Empty tuple if you have no parameters

    # Use the Query method to execute the query
    result = s.Query(query, values)

    # Assuming that the Query method returns the count as a result
    count = result[0][0]  # Access the count from the result

    return count


def order_count():
    s = sql()  # Instantiate your SQL class
    # Define the SQL query and values
    query = "SELECT COUNT(*) FROM billing_history;"
    values = ()  # Empty tuple if you have no parameters

    # Use the Query method to execute the query
    result = s.Query(query, values)

    # Assuming that the Query method returns the count as a result
    count = result[0][0]  # Access the count from the result

    return count


def send_music_DJ(id):
    s = sql()
    query = 'SELECT * FROM DJ WHERE restaurant_id = %s'
    values = (id)
    result = s.Query(query, values)
    return result


def reservation(resId, tableId):
    s = sql()
    query = "SELECT * FROM alloment where restaurantId = %s and TableId = %s"
    values = (resId, tableId)
    result = s.Query(query, values)
    s.connection.commit()
    return result


def manager_list_admin():
    s = sql()
    query = "SELECT * FROM UNIVERSAL WHERE role = 'manager'"
    result = s.Query(query)
    return result


def users_list_admin():
    s = sql()
    query = "SELECT * FROM UNIVERSAL WHERE role = 'customer'"
    result = s.Query(query)
    return result


def add_tax_col(id, tax, GST, offer):
    # Assuming you have a function or class to manage the database connection
    s = sql()

    # Define the attributes and their values
    tax_attributes = {
        "restaurant_id": id,
        "tax": tax,
        "GST": GST,
        "offer": offer
    }

    # Generate the SQL insert statement
    query = f"INSERT INTO Taxes ({', '.join(tax_attributes.keys())}) VALUES ({', '.join(['%s'] * len(tax_attributes))})"
    values = tuple(tax_attributes.values())

    # Execute the insert statement
    s.Query(query, values)
    s.connection.commit()
    return True


def edit_tax(id, new_tax, new_GST, new_offer):
    # Assuming you have a function or class to manage the database connection
    s = sql()

    # Generate the SQL UPDATE statement
    query = "UPDATE Taxes SET tax = %s, GST = %s, offer = %s WHERE id = %s"
    values = (new_tax, new_GST, new_offer, id)

    # Execute the UPDATE statement
    s.Query(query, values)
    s.connection.commit()
    return True


def check_prev_order(orderid):
    s = sql()

    # Define your SQL query with a placeholder for the orderid
    query = "SELECT * FROM orders WHERE order_id = %s"

    # Place the orderid in a tuple for the query
    values = (orderid,)

    # Execute the query with the provided values
    result = s.Query(query, values)

    # Commit the transaction (if necessary)
    s.connection.commit()
    if result:
        return True
    else:
        return False


def insert_order(restaurant_id, order_id, table_no, food_name, total, date_time):
    # Assuming you have a function or class to manage the database connection
    s = sql()

    # Generate the SQL INSERT statement
    query = "INSERT INTO Orders (restaurant_id, order_id, table_no, food_name, total, date_time) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (restaurant_id, order_id, table_no, food_name, total, date_time)

    # Execute the INSERT statement
    s.Query(query, values)
    s.connection.commit()
    return True


def update_order(restaurant_id, order_id, table_no, food_name, total, date_time, status, payment_status):
    # Assuming you have a function or class to manage the database connection
    s = sql()

    # Generate the SQL UPDATE statement
    query = "UPDATE Orders SET table_no = %s, food_name = %s, total = %s, date_time = %s, status = %s, payment_status = %s WHERE restaurant_id = %s AND order_id = %s"
    values = (table_no, food_name, total, date_time, status, payment_status, restaurant_id, order_id)

    # Execute the UPDATE statement
    s.Query(query, values)
    s.connection.commit()
    return True



def one_day_manager(id):
    import pymysql  # Assuming you are using MySQL
    import datetime
    from collections import defaultdict

    # Database connection configuration
    db_config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'waveX'
    }

    # Define the date for the specific day
    selected_date = datetime.date(2023, 10, 17)  # Replace with your desired date
    restaurant_id = id
    # Connect to the database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # SQL query to fetch data for the specified date
    sql_query = f"""
        SELECT DATE_FORMAT(`Date and Time`, '%H:00') AS Hour, COUNT(*) AS Count
        FROM billing_history
        WHERE DATE(`Date and Time`) = '{selected_date}' and restaurant_id = '{restaurant_id}'
        GROUP BY Hour
        ORDER BY Hour
    """

    cursor.execute(sql_query)
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    connection.close()

    # Organize the data into an array with labels for each hour
    hourly_data = defaultdict(int)

    for hour, count in data:
        hourly_data[hour] = count

    # Convert the defaultdict to a list of dictionaries
    result = [{"hour": hour, "count": count} for hour, count in hourly_data.items()]
    return result


db_config = {
    'user': 'root',
    'password': '-----------',
    'host': 'localhost',
    'database': 'waveX'
}


def get_labels_and_data(restaurant_id, num_days):
    # Calculate the end date (today) and the start date (num_days ago)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=num_days - 1)

    # Initialize lists to store labels (dates) and data (order counts)
    labels = []
    data = []

    # Connect to the database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Loop through each day within the specified number of days
    current_date = start_date
    while current_date <= end_date:
        # SQL query to fetch the count of order IDs for the specified date and restaurant_id
        sql_query = f"""
            SELECT COUNT(DISTINCT order_id) AS Count
            FROM billing_history
            WHERE DATE(`Date and Time`) = '{current_date}' and restaurant_id = '{restaurant_id}'
        """

        cursor.execute(sql_query)
        order_count = cursor.fetchone()[0]

        # Append the date (label) and order count (data) to their respective lists
        labels.append(current_date.isoformat())
        data.append(order_count)
        # Move to the next day
        current_date += datetime.timedelta(days=1)
    # Close the database connection
    cursor.close()
    connection.close()
    return labels, data


# ordes sql

def do_orders(restaurant_id , table_no ,order_id , food_name , user_id , total , date_time, status = 'pending', payment_status = 'pending'):
    s = sql()
    query = "INSERT INTO orders(restaurant_id, table_no, order_id, food_name, total, date_time, status, payment_status ,user_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    values = (restaurant_id, table_no, order_id, food_name, total, date_time, status, payment_status ,user_id)
    try:
        s.Query(query, values)
        query = "INSERT INTO waiter_history (restaurant_id, order_id, table_no, total, date_time, status, payment_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (restaurant_id, order_id, table_no, total, date_time, status, payment_status)
        s.Query(query ,values)
        s.connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def insert_order(user_id, restaurant_id, table_id, menu_id, quantity , order_id):
    s = sql()
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        # Insert the order details into the user_orders_history table
        query = "INSERT INTO user_orders_history (order_id, menu_id, quantity, customer_id) VALUES (%s, %s, %s, %s);"
        values = (order_id, menu_id, quantity, user_id)
        s.Query(query, values)
        # Insert the order into the orders and waiter_history tables
        do_orders(restaurant_id, table_id, order_id, menu_id, user_id,0, date_time)
        s.connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
def show_unaccpted(id):
    try:
        s = sql()
        query= f"select * from universal where username = '{id}'"
        result = s.Query(query)[0]
        resId = result[7]
        query = f"select * from waiter_history where restaurant_id = '{resId}' and status = 'pending' and (waiter_id IS NULL OR waiter_id = '{id}')"
        result = s.Query(query)
        return result
    except mysql.connector.Error as err:
        print(f"Error : {err}")

def accept(id, waiter_id):
    try:
        s = sql()
        query = f"UPDATE orders SET status = 'accepted' WHERE order_id = '{id}';"
        s.Query(query)
        s.connection.commit()
        a = 'accepted'
        # Corrected the second SQL statement
        query = f"UPDATE waiter_history SET waiter_id = '{waiter_id}' WHERE order_id = '{id}'"
        s.Query(query)
        query =f"UPDATE waiter_history SET status = '{a}' WHERE order_id = '{id}'"
        s.Query(query)
        s.connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error : {err}")
        return False

def decline(id, waiter_id):
    try:
        s = sql()
        query = f"UPDATE orders SET status = 'declined' WHERE order_id = '{id}';"
        s.Query(query)
        s.connection.commit()
        a = 'declined'
        # Corrected the second SQL statement
        query = f"UPDATE waiter_history SET waiter_id = '{waiter_id}' WHERE order_id = '{id}'"
        s.Query(query)
        query =f"UPDATE waiter_history SET status = '{a}' WHERE order_id = '{id}'"
        s.Query(query)
        s.connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error : {err}")
        return False

def get_user_menu(restaurantId ):
    s = sql()
    query = f"SELECT category_id, category_name, item_id, type, price, url,menu_name FROM item WHERE restaurant_id = '{restaurantId}'"
    menu_items = s.Query(query)
    categorized_menu = {}

    for item in menu_items:
        category_id = item[0]
        category_name = item[1]
        menu_id = item[2]

        # If the category_id is not in the categorized_menu, create a new category
        if category_id not in categorized_menu:
            categorized_menu[category_name] = {
                "id": category_id,
                "title": category_name,
                "menus": []
            }

        # Append the menu item to the corresponding category
        categorized_menu[category_name]["menus"].append({
            "id": menu_id,
            "title":item[6],
            "type": item[3],  # type (veg or nonveg)
            "price": item[4],  # price
            "url": item[5]  # url

        })
    return categorized_menu
def show_bill(order_id):
    try:
        # Create a database connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="-------",
            database="wavex"
        )
        cursor = connection.cursor()
        # Retrieve order information
        order_query = f"SELECT food_name, total FROM orders WHERE order_id = '{order_id}'"
        cursor.execute(order_query)
        order_result = cursor.fetchone()

        if order_result:
            food_name = order_result[0]
            total_amount = order_result[1]

            # Retrieve the list of items and quantities from user_orders_history
            items_query = f"SELECT menu_id, quantity FROM user_orders_history WHERE order_id = '{order_id}'"
            cursor.execute(items_query)
            items_result = cursor.fetchall()

            items = [{"menu_id": item[0], "quantity": item[1]} for item in items_result]

            bill_info = {
                "order_id": order_id,
                "food_name": food_name,
                "total_amount": total_amount,
                "items": items
            }

            return bill_info

        else:
            return {"error": "Order not found"}

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return {"error": "An error occurred while fetching the bill"}
    finally:
        # Close cursor and connection
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
