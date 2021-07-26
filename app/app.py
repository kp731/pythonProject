from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'airtravel'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': "Kartavya's Project"}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, travels=result)


@app.route('/view/<int:travel_id>', methods=['GET'])
def record_view(travel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', travel=result[0])


@app.route('/edit/<int:travel_id>', methods=['GET'])
def form_edit_get(travel_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', travel=result[0])


@app.route('/edit/<int:travel_id>', methods=['POST'])
def form_update_post(travel_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Month'), request.form.get('Column_1958'), request.form.get('Column_1959'),
                 request.form.get('Column_1960'), travel_id)
    sql_update_query = """UPDATE airtravel t SET t.Month = %s, t.Column_1958 = %s, t.Column_1959 = %s, t.Column_1960 = 
    %s  WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/travel/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Person Form')


@app.route('/travel/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Month'), request.form.get('Column_1958'), request.form.get('Column_1959'),
                 request.form.get('Column_1960'))
    sql_insert_query = """INSERT INTO airtravel (Month,Column_1958,Column_1959,Column_1960) VALUES (%s, %s,%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:airtravel_id>', methods=['POST'])
def form_delete_post(airtravel_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravel WHERE id = %s """
    cursor.execute(sql_delete_query, airtravel_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/travel', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/travel/<int:travel_id>', methods=['GET'])
def api_retrieve(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM airtravel WHERE id=%s', travel_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/travel/', methods=['POST'])
def api_add() -> str:
    content = request.json
    cursor = mysql.get_db().cursor()
    inputData = (content['Month'], content['Column_1958'], content['Column_1959'], content['Column_1960'])
    sql_insert_query = """INSERT INTO airtravel(Month,Column_1958,Column_1959,Column_1960) VALUES (%s, %s,%s, %s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/travel/<int:travel_id>', methods=['PUT'])
def api_edit(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Month'], content['Column_1958'], content['Column_1959'], content['Column_1960'], travel_id)
    sql_update_query = """UPDATE airtravel t SET t.Month=%s, t.Column_1958=%s, t.Column_1959=%s, t.Column_1960=%s WHERE t.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/travel/<int:travel_id>', methods=['DELETE'])
def api_delete(travel_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM airtravel WHERE id=%s"""
    cursor.execute(sql_delete_query, travel_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)