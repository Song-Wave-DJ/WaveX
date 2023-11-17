# pin :  flask --app app.py  --debug run

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
from Base.encrpyt.cipher import *
from Base.user import *


def generate_order_id():
    # Generate a unique identifier (UUID)
    unique_id = str(uuid.uuid4().int)

    # Get the current timestamp
    timestamp = int(time.time())

    # Combine the timestamp and the unique identifier
    order_id = f"{timestamp}{unique_id}"

    return order_id

def generate_random_id(size = 10 ):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(size))
    return random_id

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World! pratham'


@app.route('/api/check_username', methods=['POST'])
def check():
    data = request.get_json()
    print(data)
    username = data.get("email")
    password = data.get("password")
    result = get_user_pass(username, password)[0]
    print(username, password, result)
    key = generate_key()
    if result[3] != 'waiter':
        token = encrypt_message(result[0] , key)
    else :
        token = encrypt_message(result[1], key)
    if result[3] != 'customer':
        dicts = {
            "username": result[1],
            "role": result[3],
            "phone": result[4],
            "access_token": decode(token)  # Fix the typo here
        }
        return jsonify(dicts)
    else :
        dicts = {
            "username": result[1],
            "role": result[3],
            "phone": result[4],
            "access_token": decode(token),
            "session_id":'True'
        }
        return jsonify(dicts)



@app.route('/api/get_waiter', methods=['GET'])
def send_waiter():
    data = request.headers.get('Authorization')
    print(data)
    user_id  = data.split(' ')[1].strip()
    key = generate_key()
    id = decrypt_message(encode(user_id), key)
    result = get_waiter_detail(id)
    print(result)
    dicts = []
    if id :
        for item in result:
            dicts.append({
                'id': item[1],
                'name': item[2],
                'email': item[3],
                'password': item[4],
                'date': item[5],
                'phone': item[6]
            })
        return jsonify(dicts)
    else :
        return jsonify("{message : check access token}")

@app.route('/api/set_waiter', methods=['POST'])
def add_waiter():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    id = decrypt_message(encode(data), key)
    data = request.get_json()
    waiter_id = data.get("waiter_id")
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    date = data.get("date")
    phone = data.get("phone")
    key = insert_waiter(id, waiter_id, name, email, password, date, phone)
    if key :
        return jsonify({
        'message': 'done'
        })
    else :
        return jsonify({
            'message' : 'entry is there'
        })

@app.route('/api/delete_waiter_manager' , methods = ['POST'])
def delete_waiter():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        data = request.get_json()
        waiter_id = data.get("waiter_id")
        print(len(waiter_id) , waiter_id  ,len(user_id), user_id)
        key = delete_waiter_res(user_id , waiter_id)
        if key:
            return jsonify({'mesaage':'Removed'})
        else :
            return jsonify({'message' : 'Waiter is not there'})
    else :
        return jsonify({
            'message':'please check token'
        })


@app.route('/api/set_menu', methods=['POST'])
def add_menu():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)

    if user_id:
        try:
            menu_item_data = request.get_json()
            if not menu_item_data:
                return jsonify({'error': 'Invalid menu item data'})

            # Pass the menu item data to the insert_menu function
            insert_menu(
                category_name=menu_item_data.get('category_name'),
                menu_name=menu_item_data.get('menu_name'),
                price=menu_item_data.get('price'),
                discount=menu_item_data.get('discount'),
                description=menu_item_data.get('description'),
                restaurant_id=user_id,  # Assuming the user_id is the restaurant's ID
                type=menu_item_data.get('type'),
                available=menu_item_data.get('available')
            )
            return jsonify({'message': 'Menu item added successfully'})
        except Exception as e:
            return jsonify({'error': 'Failed to add the menu item: {}'.format(str(e))})
    else:
        return jsonify({'error': 'Invalid access token'})


@app.route('/api/get_menu', methods=['GET'])
def send_menu():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    id = decrypt_message(encode(data), key)
    if id:
        result = get_menu_detail(id)
        dicts = []

        for item in result:
            category_name, menu_name, price, discount, description, restaurant_id, Type, Available = item
            menu_dict = {
                'category': category_name,
                'name': menu_name,
                'price': price,
                'discount': discount,
                'description': description,
                'id': restaurant_id,
                'type': Type,
                'available': Available
            }
            dicts.append(menu_dict)

        # Return the menu details as JSON
        return jsonify({'menu': dicts})
    else:
        return jsonify({'error': 'Invalid access token'})


@app.route('/api/delete_menu' , methods = ['POST'])
def remove_menu():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    id = decrypt_message(encode(data), key)
    data = request.get_json()
    if id:
        delete_menu(id , data.get("name"))
        return jsonify({'message':'Done'})
    else :
        return jsonify({'message':'Please check  the access token '})

@app.route('/api/get_table', methods=['GET'])
def restuarant_table_get():
    # Get the access token from the request headers
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user information (e.g., user_id)
    user_id = decrypt_message(encode(data), key)
    print(type(user_id) , user_id )

    if user_id:
        # Here, you can retrieve restaurant table information for the specific user based on their user_id
        table_info = get_tables(str(user_id))

        # Process the table information and format the response
        formatted_table_info = []

        for info in table_info:
            formatted_table_info.append({'table': info[0],'url': info[2]})
        return jsonify(formatted_table_info)
    else:
        return jsonify({'error': 'Invalid access token'})


@app.route('/api/set_table', methods=['POST'])
def add_table():
    data = request.headers.get('Authorization')
    access_token = data.split(' ')[1]

    # Generate a decryption key
    key = generate_key()
    # Decrypt the access token to get user information (e.g., user_id)
    user_id = decrypt_message(encode(access_token), key)
    data = request.get_json()
    url = f'https://song-wave.web.app?restaurant_id={user_id}&table_id={data.get("table_no")}'
    print(data)
    if user_id:
        print(data.get("table_no") , user_id )
        set_tables(data.get("table"), user_id, url)
        return jsonify({
            "message": "Done"
        })
    else:
        return jsonify({
            "message": "check the access token"
        })

@app.route('/api/remove_table' , methods = ['POST'])
def remove_table() :
    data = request.headers.get('Authorization')
    access_token = data.split(' ')[1]

    # Generate a decryption key
    key = generate_key()
    # Decrypt the access token to get user information (e.g., user_id)
    user_id = decrypt_message(encode(access_token), key)
    data = request.get_json()

    if user_id:
        print(data.get("table_no"), user_id)
        delete_table(user_id, data.get("table"))
        return jsonify({
            "message": "Done"
        })
    else:
        return jsonify({
            "message": "check the access token"
        })



@app.route('/api/billing-history', methods=['GET'])
def billing_history():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    user_id = decrypt_message(encode(data), key)

    if user_id:
        try:
            result = get_billing_history(user_id)
            billing_history = []
            for row in result:
                billing_history.append({
                    'id': row[1],
                    'transactionId': row[2],
                    'table no': row[3],
                    'price': float(row[4]),  # Convert to a floating-point number
                    'createdAt': row[5].isoformat(),
                    'status': row[6],
                    'payment_status': row[7],
                    'time': row[9].isoformat() if row[9] else None
                })

            return jsonify({'billing_history': billing_history})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve billing history: {}'.format(str(e))})
    else:
        return jsonify({'error': 'Invalid access token'})


@app.route('/api/live-billing-history', methods=['GET'])
def live_billing_history():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    user_id = decrypt_message(encode(data), key)

    if user_id:
        try:
            result = get_live_billing_history(user_id)
            billing_history = []
            for row in result:
                billing_history.append({
                    'order_id': row[1],
                    'Transaction ID': row[2],
                    'table no': row[3],
                    'Total': float(row[4]),  # Convert to a floating-point number
                    'time': row[5].isoformat(),
                    'Status': row[6],
                    'payment_status': row[7],
                    'waiter_id': row[8],
                    'payment_time': row[9].isoformat() if row[9] else None
                })

            return jsonify({'billing_history': billing_history})
        except Exception as e:
            return jsonify({'error': 'Failed to retrieve billing history: {}'.format(str(e))})
    else:
        return jsonify({'error': 'Invalid access token'})







@app.route('/api/show-orders', methods=['GET'])
def show_orders():
    access_token = request.headers.get('access_token')
    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user information (e.g., user_id)
    user_id = decrypt_message(encode(access_token), key)

    if user_id:
        # Here, you can retrieve the orders for the specific user using their user_id
        orders = show_orders(user_id)

        # Process the orders and format the response
        formatted_orders = []

        for order in orders:
            formatted_order = {
                'restaurant_id': order['restaurant_id'],
                'order_id': order['order_id'],
                'table_no': order['table_no'],
                'food_name': order['food_name'],
                'total': order['total'],
                'date_time': order['date_time'].isoformat(),
                'status': order['status'],
                'payment_status': order['payment_status']
            }
            formatted_orders.append(formatted_order)

        return jsonify({'orders': formatted_orders})
    else:
        return jsonify({'error': 'Invalid access token'})


@app.route('/api/accept-payment', methods=['POST'])
def accept_payment():
    access_token = request.headers.get('access_token')

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)
    order_id = request.get_json().get("order_id")

    if user_id:
        result = update_payment_status(user_id, order_id, 'Accepted')
        
        if result:
            return jsonify({'message': 'Payment accepted successfully'})
        else:
            return jsonify({'error': 'Failed to accept payment'})
    else:
        return jsonify({'error': 'Invalid access token or missing user/order information'})


@app.route('/api/decline-payment', methods=['POST'])
def decilne_payment():
    access_token = request.headers.get('access_token')

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)
    order_id = request.get_json().get("order_id")

    if user_id:
        result = update_payment_status(user_id, order_id, 'Accepted')

        if result:
            return jsonify({'message': 'Payment accepted successfully'})
        else:
            return jsonify({'error': 'Failed to accept payment'})
    else:
        return jsonify({'error': 'Invalid access token or missing user/order information'})




@app.route('/api/reject-order', methods=['POST'])
def reject_order():
    access_token = request.headers.get('access_token')

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)
    order_id = request.get_json().get("order_id")

    if user_id:
        result = update_order_status(user_id, order_id, 'Rejected')

        if result:
            return jsonify({'message': 'Payment accepted successfully'})
        else:
            return jsonify({'error': 'Failed to accept payment'})
    else:
        return jsonify({'error': 'Invalid access token or missing user/order information'})

@app.route('/api/tax' , methods  = ['POST'])
def change_tax():
    access_token = request.headers.get('access_token')

    # Generate a decryption key (You should have the implementation for this)
    key = generate_key()

    # Decrypt the access token to get user and order information (You should have the implementation for this)
    user_id = decrypt_message(access_token, key)

    if user_id:
        data = request.get_json()

        # Extract data from the JSON payload
        id = data.get(user_id)
        new_tax = data.get('new_tax')
        new_GST = data.get('new_GST')
        new_offer = data.get('new_offer')

        # Call the edit_tax function with the extracted data
        result = edit_tax(id, new_tax, new_GST, new_offer)

        if result:
            return jsonify({'message': 'Tax information updated successfully'})
        else:
            return jsonify({'message': 'Failed to update tax information'})
    else:
        return jsonify({'message': 'Check tokens'})



# manager dashboard
@app.route('/api/one_day_manger_pie' , methods = ['POST'])
def pie_time_category_manager():
    access_token = request.headers.get('access_token')
    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)
    if user_id:
        result =one_day_manager(user_id)
        return jsonify(result)

@app.route('/api/one_week_manager' , methods = ['POST'])
def pie_week_dashboard_manager():
    access_token = request.headers.get('access_token')
    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)
    num_days = 7  # Replace with the number of days you want to retrieve data for
    labels, data = get_labels_and_data(user_id, num_days)
    return jsonify({
        "labels": labels ,
        "data":data
    })


def bar_category_manger():
    pass


def pie_time_menu_manager():
    pass


def bar_menu_maanger():
    pass


def pie_week_menu_manager():
    pass


# admin-dasboard
@app.route('/api/add_manager', methods=['POST'])
def add_manager_():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)

    if user_id:
        data = request.get_json()

        # Assuming your 'data' dictionary contains the attributes for the new manager
        id = generate_random_id()
        username = data.get('email')
        password = data.get('password')
        role = 'manager'
        phone = data.get('phone')
        name = data.get('name')

        # Call your 'create_user' function with the provided attributes
        result = create_user(id, username, password, role, phone, name)
        if result:
            return jsonify({'message': 'Manager created successfully'})
        else:
            return jsonify({'message': 'Failed to create manager'})
    else:
        return jsonify({'message': 'Check tokens'})


@app.route('/api/admin_manager_list', methods = ['GET'])
def manager_list():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        records = manager_list_admin()
        results = []
        for record in records:
            result_dict = {
                'id': record[0],
                'email': record[1],
                'password': record[2],
                'role': record[3],
                'phone_number': record[4],
                'name': record[5],
                'createdAt':record[6]
            }
            results.append(result_dict)

        return jsonify(results)
    else:
        return jsonify({
            'message':'check tokens '
        })


@app.route('/api/admin_user_list', methods = ['GET'])
def user_list():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        records = users_list_admin()
        results = []
        for record in records:
            result_dict = {
                'id': record[0],
                'email': record[1],
                'password': record[2],
                'role': record[3],
                'phone_number': record[4],
                'name': record[5],
                'createdAt':record[6] ,
            }
            results.append(result_dict)

        return jsonify(results)
    else:
        return jsonify({
            'message':'check tokens '
        })



@app.route('/api/admin_count_manager' , methods = ['GET'])
def count_manager():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        count = manager_count()
        return jsonify({
            "count":count
        })
    else :
        return jsonify({
            "please check the access_token"
        })

@app.route('/api/admin_count_waiter' ,methods = ['GET'])
def count_waiter():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        count = waiter_count()
        return jsonify({
            "count": count
        })
    else:
        return jsonify({
            "please check the access_token"
        })

@app.route('/api/admin_count_orders' ,methods = ['GET'])
def count_order():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    if user_id:
        count = order_count()
        return jsonify({
            "count": count
        })
    else:
        return jsonify({
            "please check the access_token"
        })

@app.route('/api/admin_remove_manager' , methods = ['POST'])
def remove_manager():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    data = request.get_json()
    if user_id:
        id = data.get("id")
        delete_user(id)
        return jsonify({
            'message':'succesfuly removed '
        })
    else :
        return jsonify({
            'message': 'please check the access_token'
        })

@app.route('/api/admin_remove_user' , methods = ['POST'])
def remove_user():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)
    data = request.get_json()
    if user_id:
        id = data.get("id")
        delete_user(id)
        return jsonify({
            'message':'succesfuly removed '
        })
    else :
        return jsonify({
            'message': 'please check the access_token'
        })

@app.route('/api/create_user' , methods = ['POST'])
def customer():
    data = request.get_json()
    email = data.get("email")
    password =data.get("password")
    name = data.get("name")
    phone = data.get("phone")
    create_user(generate_random_id() ,email , password , 'customer' , phone , name )
    return jsonify({
        "message":"Successfully created"
    })

# DJ -user
def get_music():
    access_token = request.headers.get('access_token')

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)


@app.route('/api/send_music', methods=['GET'])
def send_music():
    access_token = request.headers.get('access_token')

    # Generate a decryption key
    key = generate_key()

    # Decrypt the access token to get user and order information
    user_id = decrypt_message(encode(access_token), key)

    result = send_music_DJ(user_id)

    music_data = []
    for row in result:
        music_data.append({
            'Thumbnail': row[0],
            'Song_name': row[1],
            'Duration': row[2].total_seconds() if row[2] else None,  # Convert time to seconds
            'Artist': row[3],
            'DateTime': row[4].isoformat() if row[4] else None,  # Format datetime as ISO string
            'Set_waiting_time': row[5].total_seconds() if row[5] else None,  # Convert time to seconds
            'Request_status': row[6]
        })
    return jsonify(result)


@app.route('/api/user_menu' , methods = ['GET'])
def user_menu():
    restaurantId = request.args.get("restaurantId")
    menu  = get_user_menu(restaurantId)
    return jsonify(menu)


@app.route('/api/take_order', methods=['POST'])
def get_order():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    user_id = decrypt_message(encode(data), key)

    restaurantId = request.args.get("restaurantId")
    tableId = request.args.get("tableId")
    order_data = request.get_json()
    order_id = generate_order_id()
    if user_id:
        for item in order_data:
            categoryId = item.get("categoryId")
            menuId = item.get("menuId")
            Qty = item.get("Qty")

            # Insert the order into the user_orders_history table
            insert_order(user_id, restaurantId, tableId, menuId, Qty , order_id)

        return jsonify({"message": "Order placed successfully"})
    else:
        return jsonify({"message": "Unknown user"})


# waiter acceptance
@app.route('/api/show_waiter_unaccepted_order' , methods =['GET'])
def waiter_acceptance():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    waiter_username  = decrypt_message(encode(data), key)
    result = show_unaccpted(waiter_username)

    orders = []
    for row in result:
        orders.append({
            "restaurant_id": row[0],  # Replace with actual column names
            "order_id": row[1],
            "table_no": row[3],
            "total": row[4],
            "date_time": row[5],
            "status": row[6],
            "payment_status": row[7],
        })

    return jsonify({
        "result":orders
    })

@app.route('/api/accept_' , methods = ['POST'])
def accept_order():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    waiter_username = decrypt_message(encode(data), key)
    print(waiter_username)
    data = request.get_json()
    order_id = data.get("order_id")
    result = accept(order_id , waiter_username)
    if result :
        return jsonify({
            'message': "Done"
        })
    else :
        return ({
            'message': 'Undone'
        })

@app.route('/api/decline_' , methods = ['POST'])
def decline_order():
    data = request.headers.get('Authorization')
    data = data.split(' ')[1]
    key = generate_key()
    waiter_username = decrypt_message(encode(data), key)
    print(waiter_username)
    data = request.get_json()
    order_id = data.get("order_id")
    result = decline(order_id , waiter_username)
    if result :
        return jsonify({
            'message': "Done"
        })
    else :
        return ({
            'message': 'Undone'
        })

@app.route('/api/view_bill', methods=['GET'])
def view_bill():
    # Get the access token and order_id from the request headers
    access_token = request.headers.get('Authorization').split('Bearer')[1].strip()

    data = request.get_json()
    order_id = data.get("order_id")

    # Decrypt the access token to get user information (You should have the implementation for this)
    key = generate_key()
    user_id = decrypt_message(encode(access_token), key)

    if user_id:
        # Retrieve the bill information for the specified order_id
        bill_info = show_bill(order_id)
        print(bill_info)

        if bill_info:
            # Extract relevant information
            items = bill_info["items"]
            total_amount = bill_info["total_amount"]

            # Format the bill based on food name and quantity
            formatted_bill = {
                "order_id": order_id,
                "items": [{
                    "food_name": item["food_name"],
                    "quantity": item["quantity"],
                    "price_per_item": item["price"],
                    "total_price": item["quantity"] * item["price"]
                } for item in items],
                "total_amount": total_amount
            }

            return jsonify(formatted_bill)
        else:
            return jsonify({"error": "Order not found"}, 404)
    else:
        return jsonify({"error": "Unauthorized"}, 401)




if __name__ == '__main__':
    app.run()
