from flask import Flask, request

from queries import SQLQueries

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password123'
app.config['MYSQL_DB'] = 'nanotech'

sql_query = SQLQueries(app)


# @app.route('/', methods=["GET"])
# def index():
#     cursor = sql_query.get_db_connection().cursor()
#     cursor.execute('SELECT DATABASE();')
#     db_name = cursor.fetchone()
#     sql_query.get_cursor(True)
#     return f'Connected to {db_name[0]} database.'


@app.route('/create', methods=["GET"])
def create_table():
    try:
        return sql_query.create_table()
    except Exception as error:
        return f'Sorry an unexpected error occurred as {error}'


@app.route('/insert', methods=["POST"])
def insert_to_db():
    data = {}
    if request.is_json:
        data = request.get_json()
    elif len(request.form) > 0:
        data = request.form

    user_id = data['user_id']
    modes = data['modes']
    deflection = data['deflection']
    frequency = data['frequency']

    try:
        return sql_query.add_to_table(user_id, modes, deflection, frequency)
    except Exception as e:
        return f"Sorry, an error occurred as {e}"


@app.route('/fetch/<user_id>', methods=["GET"])
def fetch_data(user_id):
    try:
        return sql_query.fetch_from_table(user_id)
    except Exception as e:
        return f"Sorry, an error occurred as {e}"


if __name__ == '__main__':
    app.run(debug=True)
