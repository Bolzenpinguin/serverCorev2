from flask import Blueprint, jsonify, request
from .db import get_db_connection, close_db_connection

bp = Blueprint('main', __name__)


@bp.route('/<string:table>/data', methods=['GET'])
def get_data(table):
    connection = get_db_connection()
    dynamic_query = f"SELECT * FROM {table}"
    data = connection.execute(dynamic_query).fetchall()
    close_db_connection()
    return jsonify([dict(row) for row in data])


@bp.route('/<string:table>/delete/<int:id_remove>', methods=['DELETE'])
def delete_entry(table, id_remove):
    connection = get_db_connection()
    dynamic_query = f"DELETE FROM {table} WHERE id = ?"
    connection.execute(dynamic_query, (id_remove,))
    connection.commit()
    close_db_connection()
    return jsonify({'message': f'Removed entry with id {id_remove} from {table}'})


@bp.route('/user/post', methods=['POST'])
def user_post():
    data = request.get_json()
    name = data.get('name')
    color = data.get('color')

    connection = get_db_connection()
    connection.execute('INSERT INTO user (name, color) VALUES (?, ?)', (name, color))
    connection.commit()
    close_db_connection()

    return jsonify({'message': 'User created successfully!', 'name': name, 'color': color})


@bp.route('/location/post', methods=['POST'])
def location_post():
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


@bp.route('/time/post', methods=['POST'])
def time_post():
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


@bp.route('/user/update', methods=['PUT'])
def user_update():
    data = request.get_json()

    user_id = data.get('id')
    name = data.get('name')
    color = data.get('color')

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE user SET name = ?, color = ? WHERE id = ?',
                   (name, color, user_id))

    connection.commit()
    connection.close()

    return jsonify({'message': 'User updated successfully!', 'id': user_id, 'name': name, 'color': color})


@bp.route('/time/update', methods=['PUT'])
def time_update():
    data = request.get_json()

    time_id = data.get('id')
    id_user = data.get('id_user')
    start = data.get('start')
    end = data.get('end')

    if not time_id:
        return jsonify({'error': 'Time ID is required to update record'}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('UPDATE time SET id_user = ?, start = ?, end = ? WHERE id = ?',
                   (id_user, start, end, time_id))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Updated Time successfully!', 'Time ID': time_id, 'Id User': id_user, 'Start': start, 'End': end})

