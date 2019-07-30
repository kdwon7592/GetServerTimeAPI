# -- coding: utf-8 --

from flask import Flask, request, send_from_directory
from flaskext.mysql import MySQL
from app.api import config

app = Flask(__name__)
mysql = MySQL();

app.config['MYSQL_DATABASE_USER'] = config.DATABASE_CONFIG['user']
app.config['MYSQL_DATABASE_PASSWORD'] = config.DATABASE_CONFIG['password']
app.config['MYSQL_DATABASE_DB'] = config.DATABASE_CONFIG['db']
app.config['MYSQL_DATABASE_HOST'] = config.DATABASE_CONFIG['host']

mysql.init_app(app)


@app.route('/')
def root():
    return '현희야 사랑해'


@app.route('/robots.txt')
def robot_to_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.route('/select_data', methods=["GET", "POST"])
def select_data():
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT UniversityName FROM GST_UNIVERSITY_DATA ORDER BY IdIndex")

    result = ''
    count = 0;

    for row in cursor:
        if count == 0:
            result += row[0]
            count = count + 1
        else:
            result += ',' + row[0]
            count = count + 1

    print(result)

    return result


@app.route('/insert_data', methods=['GET', 'POST'])
def insert_data():
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO test_table(name) VALUES (%s)"
    cursor.execute(sql, 'test')
    connection.commit()

    return "insert Data!!"


@app.route('/insert_search_data', methods=['GET', 'POST'])
def insert_search_data():
    data = request.args.get('keyword')
    print(data)
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO GST_SEARCH_HISTORY(SearchLog) VALUES (%s)"
    cursor.execute(sql, data)
    connection.commit()

    return '', 204


@app.route('/select_url', methods=['GET', 'POST'])
def select_url():
    data = request.args.get('keyword')
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "SELECT UniversityServerUrl FROM GST_UNIVERSITY_DATA WHERE UniversityName LIKE %s LIMIT 1"
    cursor.execute(sql, '%' + data + '%')

    result = ''

    for row in cursor:
        result = row[0]

    return result


@app.route('/insert_request', methods=['GET', 'POST'])
def insert_request():
    name = request.values.get('name')
    url = request.values.get('url')
    req = request.values.get('request')

    print(name)
    print(url)
    print(req)
    connection = mysql.connect()
    cursor = connection.cursor()
    sql = "INSERT INTO GST_REQUEST(UniversityName, UniversityServerUrl, Request) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, url, req))
    connection.commit()

    return '', 204


if __name__ == '__main__':
    app.run(localhost='0.0.0.0')
