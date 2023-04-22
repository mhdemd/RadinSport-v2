from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)


# Configuration settings for MySQL database
app.config['MYSQL_HOST'] = '217.182.208.105' # Replace with your MySQL host name or IP address
app.config['MYSQL_USER'] = 'mahdiema_digi' # Replace with your MySQL database username
app.config['MYSQL_PASSWORD'] = '[O&Q8uJ)NSoY' # Replace with your MySQL database password
app.config['MYSQL_DB'] = 'mahdiema_digi' # Replace with your MySQL database name

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

cursor = mysql.cursor()









# Open a transaction in api_5
mysql.start_transaction()

@app.route('/api_5', methods=['POST'])
def api_5():
    try:
        stock = int(request.args.get('variable1'))
        code = request.args.get('variable2')

        # Update the stock of the specified product
        cursor.execute("UPDATE products SET stock = stock - %s WHERE code = %s", (stock, code))

        # Update the transaction in api_3
        session['transaction'].add(cursor.statement, cursor.params)

        # Return a success response
        return 'Stock updated successfully'

    except Exception as e:
        # Rollback the transaction if an exception occurred
        mysql.rollback()

        # Return an error response
        return f"Error updating stock: {str(e)}"


@app.route('/api_3', methods=['GET'])
def api_3():
    DKP = request.args.get('variable')

    # Execute a SELECT query to retrieve products with the specified DKP and non-zero stock
    cursor.execute("SELECT * FROM products WHERE DKP = %s AND stock != 0", (DKP,))
    results = cursor.fetchall()

    # Update the transaction
    session['transaction'].add(cursor.statement, cursor.params)

    # Return the results as a JSON response
    return jsonify(results)


# Commit the transaction in another API
@app.route('/api_commit', methods=['POST'])
def api_commit():
    try:
        session['transaction'].commit()
        return 'Transaction committed successfully'

    except Exception as e:
        # Rollback the transaction if an exception occurred
        session['transaction'].rollback()
        return f"Error committing transaction: {str(e)}"

