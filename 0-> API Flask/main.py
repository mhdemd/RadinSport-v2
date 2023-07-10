from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from datetime import timedelta
import mysql.connector
from datetime import datetime
import logging
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import os
import unicodedata
import re

app = Flask(__name__)

# set the logging level to DEBUG
app.logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('app.log')

# add the file handler to the app logger
app.logger.addHandler(handler)

app.secret_key = 'secret_key'

# Configuration settings for MySQL database
app.config['MYSQL_HOST'] = '217.182.208.105' # Replace with your MySQL host name or IP address
app.config['MYSQL_USER'] = 'mahdiema_digi' # Replace with your MySQL database username
app.config['MYSQL_PASSWORD'] = '[O&Q8uJ)NSoY' # Replace with your MySQL database password
app.config['MYSQL_DB'] = 'mahdiema_digi' # Replace with your MySQL database name
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

#################################################### RadinSport APIs
@app.route('/api_1')
def index_1():
    cursor = mysql.cursor()

    cursor.execute("SELECT DISTINCT DKP,title,detail_3,detail_4,off,price,price_off FROM products WHERE cat = 'H' AND stock != 0 AND off != 0 ;")
    results = cursor.fetchall()
    
    # Close the cursor
    cursor.close()

    return jsonify(results)

@app.route('/api_2')
def index_2():
    cursor = mysql.cursor()

    cursor.execute("SELECT DISTINCT DKP,title,detail_3,detail_4,off,price,price_off,version FROM products WHERE cat = 'GL' AND stock != 0 AND off != 0 ;")
    results = cursor.fetchall()
    
    # Close the cursor
    cursor.close()

    return jsonify(results)

@app.route('/api_3', methods=['GET'])
def index_3():

    cursor = mysql.cursor()

    DKP = request.args.get('variable')

    my_query = """
        SELECT title, code, cat, DKP, stock_temp, price, price_off, off, size, color_fa, color, material, made_in, type, detail_1, detail_2, detail_3, detail_4
        FROM products
        WHERE stock_temp != 0
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45
          AND DKP = %s
        UNION
        SELECT title, code, cat, DKP, stock, price, price_off, off, size, color_fa, color, material, made_in, type, detail_1, detail_2, detail_3, detail_4
        FROM products
        WHERE stock != 0
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) > 45
          AND DKP = %s
    """
    
    cursor.execute(my_query, (DKP, DKP))

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)

@app.route('/api_4', methods=['GET'])
def index_4():
    cursor = mysql.cursor()
    
    DKP = request.args.get('variable1')
    cat = request.args.get('variable2')
    cursor.execute("SELECT DISTINCT DKP FROM products WHERE cat = \'%s\' AND stock != 0 AND DKP != \'%s\' LIMIT 5;"%(cat, DKP))
    results = cursor.fetchall()
    
    # Close the cursor
    cursor.close()

    return jsonify(results)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    cursor = mysql.cursor()
    
    my_dict =  request.json
    
    # Insert data into the products table
    query2 = "UPDATE products SET stock_temp = stock_temp - 1 WHERE code = %s AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45"
    query3 = "UPDATE products SET stock_temp = stock - 1 WHERE code = %s AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) > 45"
    query4 = "UPDATE products SET stock_temp_time = NOW() WHERE code = %s"
    
    cursor.execute(query2, (my_dict['code'],))
    cursor.execute(query3, (my_dict['code'],))
    cursor.execute(query4, (my_dict['code'],))
    
    # Close the cursor
    mysql.commit()
    cursor.close()
    
    return {'message': 'Ok'}

@app.route('/get_new_stock_to_add', methods=['GET'])# for +
def get_new_stock_to_add():
    cursor = mysql.cursor()

    code = request.args.get('variable')

    my_query = """
        SELECT stock_temp
        FROM products
        WHERE stock_temp != 0
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45
          AND code = %s
        UNION
        SELECT stock
        FROM products
        WHERE stock != 0
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) > 45
          AND code = %s
    """
    
    cursor.execute(my_query, (code, code))

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)
    
@app.route('/orders_balance_add', methods=['POST'])# for +
def orders_balance_add():

    cursor = mysql.cursor()
    
    code = request.args.get('variable1')
    
    # Insert data into the products table
    query2 = "UPDATE products SET stock_temp = stock_temp - 1 WHERE code = %s AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45"
    query3 = "UPDATE products SET stock_temp_time = NOW() WHERE code = %s"
    
    cursor.execute(query2, (code,))
    cursor.execute(query3, (code,))
    
    # Close the cursor
    mysql.commit()
    cursor.close()
    
    return {'message': 'Ok'}

@app.route('/orders_balance_remove', methods=['GET'])# for -
def orders_balance_remove():

    cursor = mysql.cursor()
    
    code = request.args.get('variable1')

    # Insert data into the products table
    query2 = "UPDATE products SET stock_temp = stock_temp + 1 WHERE code = %s AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45"

    cursor.execute(query2, (code,))

    # Close the cursor
    mysql.commit()
    cursor.close()
    
    return {'message': 'Ok'}

@app.route('/check_registration_1', methods=['GET'])
def check_registration_1():
    cursor = mysql.cursor()
    
    code = request.args.get('variable')

    cursor.execute("SELECT stock FROM products WHERE code = \'%s\';"%(code))
    results = cursor.fetchall()

    # Close the cursor
    cursor.close()

    return jsonify(results)
    
@app.route('/check_registration_2', methods=['POST'])
def check_registration_2():

    cursor = mysql.cursor()
    
    my_dict =  request.json
    
    # Insert data into the orders table
    query1 = "INSERT INTO orders (order_num, code, num_order, date_time, image, title, total, color_en, color_fa, id, total_price, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    # Extract the data from the dictionary
    data = (
        my_dict['order_num'], my_dict['code'], my_dict['num_order'], 
        datetime.now(), my_dict['image'], my_dict['title'], 
        my_dict['total'], my_dict['color_en'], my_dict['color_fa'],
        my_dict['id'], my_dict['total_price'], 'سفارش جدید'
    )

    # Execute the SQL query
    cursor.execute(query1, data)

    # Insert data into the orders table
    query2 = "UPDATE products SET stock = stock - %s WHERE code = %s"
    
    # Extract the data from the dictionary
    data = (
            my_dict['num_order'],
            my_dict['code'],
        )

    # Execute the SQL query
    cursor.execute(query2, data)

    # Close the cursor
    mysql.commit()
    cursor.close()
    
    return {'message': 'Ok'}
    
@app.route('/open_category', methods=['GET'])
def open_category():

    cursor = mysql.cursor()

    cat = request.args.get('variable')
    
    my_query = """
        SELECT DKP, MIN(title), MIN(detail_3), MIN(detail_4), MIN(price), MIN(off), MIN(price_off)
        FROM products
        WHERE cat = %s
          AND stock != 0
        GROUP BY DKP
    """
    
    cursor.execute(my_query, (cat,))

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)

@app.route('/open_grouping', methods=['GET'])
def open_grouping():

    cursor = mysql.cursor()

    cat = request.args.get('variable')
    
    my_query = """
        SELECT DISTINCT DKP
        FROM products
        WHERE cat = %s
          AND stock != 0
        LIMIT 5
    """    
    
    cursor.execute(my_query, (cat,))

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)
  
@app.route('/Search_in_search_bar', methods=['GET'])
def Search_in_search_bar():

    cursor = mysql.cursor()

    text_ = request.args.get('variable')
    word = reshape(reshape(text_))

    my_query = "SELECT cat FROM products WHERE title LIKE %s LIMIT 1 "
    cursor.execute(my_query, ('%' + word + '%',))
    #        LIMIT 1    

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)

@app.route('/see_orders', methods=['GET'])
def see_orders():

    cursor = mysql.cursor()

    id = request.args.get('variable')
    
    if id != '1000':
        my_query = """
            SELECT order_num, image, status
            FROM orders
            WHERE id = %s
        """
        cursor.execute(my_query, (id,))
    
        results = cursor.fetchall()
        cursor.close() 

    else:
        my_query = """
            SELECT order_num, image, status
            FROM orders
        """
        cursor.execute(my_query)
        
        results = cursor.fetchall()
        cursor.close()     
    
    return jsonify(results)
    
@app.route('/see_order_detail', methods=['GET'])
def see_order_detail():

    cursor = mysql.cursor()

    order_number = request.args.get('variable1')

    query1 = """
        SELECT *
        FROM orders
        WHERE order_num = %s
    """
    
    cursor.execute(query1, (order_number,))
    order_results = cursor.fetchall()
    
    customer_id =  request.args.get('variable2') if request.args.get('variable2') != '1000' else order_results[0][9]

    query2 = """
        SELECT name, last_name, mobile_num, address, postal_code
        FROM customers
        WHERE id = %s
    """
    
    cursor.execute(query2, (customer_id,))
    customer_results = cursor.fetchall()

    cursor.close() 
    
    return jsonify({'order': order_results, 'customer': customer_results})

@app.route('/sign_up_1')
def sign_up_1():
    cursor = mysql.cursor()

    cursor.execute("SELECT id FROM customers;")
    results = cursor.fetchall()
    
    # Close the cursor
    cursor.close()
    return jsonify(results)
    
@app.route('/sign_up_2', methods=['POST'])
def sign_up_2():
    cursor = mysql.cursor()

    my_dict = request.json

    # Check if the email already exists in the customers table
    check_query = "SELECT COUNT(*) FROM customers WHERE email = %s"
    cursor.execute(check_query, (my_dict['email'],))
    result = cursor.fetchone()

    if result[0] > 0:
        # If the email already exists, return a message indicating the duplication
        return {'message': 'Email already exists'}

    # Insert data into the customers table
    query1 = """
    INSERT INTO customers (name, last_name, mobile_num, home_num, address, postal_code, email, id, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        last_name = VALUES(last_name),
        mobile_num = VALUES(mobile_num),
        home_num = VALUES(home_num),
        address = VALUES(address),
        postal_code = VALUES(postal_code),
        email = IF(VALUES(email) != 'Registered', VALUES(email), email),
        password = IF(VALUES(password) != '', VALUES(password), password)
    """

    # Extract the data from the dictionary
    data = (
        my_dict['name'], my_dict['last_name'], my_dict['mobile_num'],
        my_dict['home_num'], my_dict['address'], my_dict['postal_code'],
        my_dict['email'], my_dict['id'], my_dict['password']
    )

    # Execute the SQL query
    cursor.execute(query1, data)

    # Close the cursor and commit the transaction
    cursor.close()
    mysql.commit()

    return {'message': 'Ok'}


@app.route('/load_account_data', methods=['GET'])
def load_account_data():

    cursor = mysql.cursor()

    id = request.args.get('variable')
    
    my_query =  "SELECT * FROM customers WHERE id = %s"
    
    cursor.execute(my_query, (id,))

    results = cursor.fetchall()
    cursor.close() 
    
    return jsonify(results)

@app.route('/count_files')
def count_files():
    DKP = request.args.get('variable')
    dir_path = '/home/mahdiema/public_html/Products/%s'%(DKP)
    abs_path = os.path.abspath(dir_path)

    if not os.path.exists(abs_path):
        return jsonify({'error': f"Directory {abs_path} does not exist"}), 404

    num_files = len([f for f in os.listdir(abs_path) if os.path.isfile(os.path.join(abs_path, f))]) - 1
    return jsonify(num_files), 200
    
@app.route('/login_check', methods=['GET'])
def login_check():
    cursor = mysql.cursor(buffered=True)

    email = request.args.get('variable1')
    password = request.args.get('variable2')

    # Check if the email exists in the Customers table
    cursor.execute("SELECT COUNT(*) FROM customers WHERE email = %s", (email,))
    result = cursor.fetchone()

    if result[0] == 0:
        # Email does not exist
        cursor.close()
        return jsonify({'email_error': 'Email not found.'})

    # Email exists, check password
    cursor.execute("SELECT id, password, name FROM customers WHERE email = %s", (email,))
    row = cursor.fetchone()

    stored_password = row[1]

    if password == stored_password:
        # Correct password, retrieve the account ID
        account_id = row[0]

        result = {'id': row[0], 'name': row[2]}

    else:
        # Incorrect password
        cursor.close()
        return jsonify({'pass_error': "Incorrect password."})

    # Move to the next result set
    if cursor.nextset():
        # Fetch any remaining result sets
        while cursor.nextset():
            pass

    cursor.close()
    return jsonify(result)

#################################################### Support App APIs
@app.route('/support_update_status', methods=['POST'])
def support_update_status():
    # get variables from form
    order_number = request.form.get('variable1')
    text_item = request.form.get('variable2')

    cursor = mysql.cursor()

    # execute SQL update statement
    update_query = "UPDATE orders SET status = %s WHERE order_num = %s"
    cursor.execute(update_query, (text_item, order_number))
    
    # commit changes to database and close connections
    mysql.commit()
    cursor.close()
    #mysql.close()
    
    # return message with order_number
    message = 'Order status updated successfully for order number: %s'%(order_number)
    return {'message': message}

@app.route('/support_open_category', methods=['GET'])
def support_open_category():

    cursor = mysql.cursor()

    cat = request.args.get('variable')
    
    my_query = """
        SELECT DKP, MIN(title), MIN(code), SUM(stock_temp), MIN(price), MIN(off), MIN(price_off)
        FROM products
        WHERE cat = %s
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) < 45
        GROUP BY DKP
        UNION
        SELECT DKP, MIN(title), MIN(code), SUM(stock), MIN(price), MIN(off), MIN(price_off)
        FROM products
        WHERE cat = %s
          AND TIMESTAMPDIFF(MINUTE, stock_temp_time, NOW()) > 45
        GROUP BY DKP
    """
    
    cursor.execute(my_query, (cat, cat))

    results = cursor.fetchall()
    cursor.close() 

    # Modify titles longer than 30 characters and separate price and discount price
    modified_results = []
    for result in results:
        title = result[1]
        title_length = len(unicodedata.normalize('NFC', title))
        if title_length > 30:
            truncated_title = unicodedata.normalize('NFC', '...' + title[-30:])
        else:
            truncated_title = title#" " * (34 - title_length) + title
        price = result[4]
        discount_price = result[6]
        modified_result = (result[0], truncated_title, result[2], result[3], f"{price:,}", result[5], f"{discount_price:,}")
        modified_results.append(modified_result)

    return jsonify(modified_results)

def normalize_code(code):
    code = code.upper()
    if re.match(r'[A-Za-z]{1,2}d{1,2}-?d{1,2}', code):
        code = re.sub(r'\s+', '-', code)
    return code

@app.route('/search_dkp', methods=['GET'])
def search_dkp():
    variable1 = request.args.get('variable1')

    # Return empty result when variable1 is empty or None
    if not variable1:
        return "[]"

    cursor = mysql.cursor()
    query = """
    SELECT DKP, MIN(title), MIN(code), SUM(stock_temp), MIN(price), MIN(off), MIN(price_off), MIN(cat)
    FROM products WHERE 
    """
    conditions = []

    # Check if variable1 (code) is provided and construct condition
    variable1 = normalize_code(variable1)
    conditions.append(f"code LIKE '{variable1}%' GROUP BY DKP")

    query += ' OR '.join(conditions)

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    # Modify titles longer than 30 characters and separate price and discount price
    modified_results = []
    for result in results:
        title = result[1]
        title_length = len(unicodedata.normalize('NFC', title))
        if title_length > 30:
            truncated_title = unicodedata.normalize('NFC', '...' + title[-30:])
        else:
            truncated_title = title#" " * (34 - title_length) + title
        price = result[4]
        discount_price = result[6]
        modified_result = (result[0], truncated_title, result[2], result[3], f"{price:,}", result[5], f"{discount_price:,}", result[7])
        modified_results.append(modified_result)

    return jsonify(modified_results)

@app.route('/get_items', methods=['GET'])
def get_items():
    code = request.args.get('code') + "%"

    # Execute SQL query
    cursor = mysql.cursor()
    query = "SELECT * FROM products WHERE code LIKE %s"
    cursor.execute(query, (code,))
    results = cursor.fetchall()

    # Close MySQL connection
    cursor.close()

    # Return the result
    return jsonify(results)
    
@app.route('/save_image_to_host', methods=['POST'])
def save_image_to_host():
    # Get the "DKP" string from the request payload
    DKP = request.form.get("DKP")

    # Check if the "DKP" string is present
    if not DKP:
        return "DKP parameter is missing", 400

    # Check if an image file is included in the request
    if 'image' not in request.files:
        return "No image file provided", 400

    # Get the image file from the request
    image_file = request.files['image']

    # Get the last number in the filenames in the folder
    folder_path = os.path.expanduser(f"~/public_html/Products/{DKP}")
    files_in_folder = os.listdir(folder_path)
    last_number = max([int(file.split('-')[1].split('.')[0]) for file in files_in_folder]) if files_in_folder else 0
    next_number = str(last_number + 1)#.zfill(2)

    # Save the image with the name as DKP + "-" + next_number + ".jpg" in the Products/{DKP} folder
    image_filename = f"{DKP}-{next_number}.jpg"
    image_path = os.path.join(folder_path, image_filename)
    image_file.save(image_path)

    return "Image saved successfully"
    
@app.route('/remove_image_from_host', methods=['POST'])
def remove_image_from_host():
    # Get the URL of the image from the request payload
    image_url = request.form.get("image_url")

    # Check if the image URL is present
    if not image_url:
        return "Image URL parameter is missing", 400

    # Extract the DKP and image filename from the URL
    url_parts = image_url.split("/")
    DKP = url_parts[-2]
    image_filename = url_parts[-1]

    # Check if the DKP and image filename are valid
    if not DKP or not image_filename:
        return "Invalid image URL", 400

    # Remove the image file from the server
    folder_path = os.path.expanduser(f"~/public_html/Products/{DKP}")
    image_path = os.path.join(folder_path, image_filename)
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        return "Image file not found", 404
    
    # Remove the image file
    os.remove(image_path)

    return "Image removed successfully"
    
@app.route('/get_image_name', methods=['GET'])
def get_image_name():
    # Get the "DKP" parameter from the request query string
    DKP = request.args.get("DKP")

    # Check if the "DKP" parameter is present
    if not DKP:
        return jsonify(error="DKP parameter is missing"), 400

    # Create the path to the image directory
    folder_path = os.path.expanduser(f"~/public_html/Products/{DKP}")

    # Check if the image directory exists
    if not os.path.exists(folder_path):
        return jsonify(error="Image directory not found"), 404

    # Get the list of image filenames in the directory
    image_files = os.listdir(folder_path)

    return jsonify(image_files=image_files)
    
######################################################
app.logger.debug('Debug message')
app.logger.info('Info message')
app.logger.warning('Warning message')
app.logger.error('Error message')
app.logger.critical('Critical message') 

if __name__ == '__main__':
    app.run()
