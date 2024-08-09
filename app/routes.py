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

