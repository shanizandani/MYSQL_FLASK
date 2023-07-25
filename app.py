import pymysql
from flask import Flask, request, jsonify

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = 'Shanizandani8876'
app.config['MYSQL_DB'] = 'cars'

mysql = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/cars', methods=['GET'])
def get_cars():
    cursor = mysql.cursor()
    query = "SELECT * FROM my_car"  # Update the table name to "my_car"
    cursor.execute(query)
    cars = cursor.fetchall()
    cursor.close()

    # Convert the result to a list of dictionaries for JSON response
    cars_data = []
    columns = [col[0] for col in cursor.description]
    for row in cars:
        cars_data.append(dict(zip(columns, row)))

    return jsonify(cars_data)


@app.route('/cars', methods=['POST'])
def add_car():
    data = request.get_json()  # Use request.get_json() instead of request.json
    cursor = mysql.cursor()
    query = "INSERT INTO my_car (MODEL, COLOR) VALUES (%s, %s)"
    values = (data['model'], data['color'])
    cursor.execute(query, values)
    mysql.commit()
    cursor.close()
    return jsonify({'message': 'Car added successfully'})


@app.route('/cars/<int:id>', methods=['PUT'])
def update_car(id):
    data = request.json
    cursor = mysql.cursor()
    query = "UPDATE my_car SET MODEL = %s, COLOR = %s WHERE ID = %s"
    values = (data['model'], data['color'], id)
    cursor.execute(query, values)
    mysql.commit()
    cursor.close()
    return jsonify({'message': 'Car updated successfully'})

@app.route('/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    cursor = mysql.cursor()
    query = "DELETE FROM my_car WHERE ID = %s"
    cursor.execute(query, (id,))
    mysql.commit()
    cursor.close()
    return jsonify({'message': 'Car deleted successfully'})

@app.route('/')
def index():
    return "welcome"


if __name__ == '__main__':
    app.run(debug=True)

