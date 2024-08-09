from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect('db/calender.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/<string:table>/data', methods=['GET'])
def get(table):
    connection = get_db_connection()
    # How to: /data/user and so one
    dynamic_query = f"SELECT * FROM {table}"
    data = connection.execute(dynamic_query).fetchall()
    connection.close()
    return jsonify([dict(row) for row in data])


@app.route('/<string:table>/delete/<int:id_remove>', methods=['DELETE'])
def delete(table, id_remove):
    connection = get_db_connection()

    dynamic_query = f"DELETE FROM {table} WHERE id = ?"

    cursor = connection.cursor()
    cursor.execute(dynamic_query, (id_remove,))
    connection.commit()
    connection.close()

    return jsonify({'message': f'Removed entry with id {id_remove} from {table}'})


@app.route('/user/post', methods=['POST'])
def post_user():
    data = request.get_json()

    name = data.get('name')
    color = data.get('color')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO user ( name, color) VALUES ( ?, ?)',
                   (name, color))

    connection.commit()
    connection.close()

    return jsonify({'message': 'User created successfully!', 'name': name, 'color': color})


@app.route('/location/post', methods=['POST'])
def post_location():
    data = request.get_json()

    id_user = data.get('id_user')
    lat = data.get('lat')
    long = data.get('long')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO location (id_user, lat, long) VALUES ( ?, ?, ?)',
                   (id_user, lat, long))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Saved Location successfully!', 'Id User': id_user, 'lat': lat, 'long': long})


@app.route('/time/post', methods=['POST'])
def post_time():
    data = request.get_json()

    id_user = data.get('id_user')
    start = data.get('start')
    end = data.get('end')

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('INSERT INTO time (id_user, start, end) VALUES ( ?, ?, ?)',
                   (id_user, start, end))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Saved Timeslot successfully!', 'Id User': id_user, 'Start': start, 'Ende': end})


if __name__ == '__main__':
    app.run(debug=True)
