from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml, secrets
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
Bootstrap(app)
secret = secrets.token_urlsafe(32)

#DB configuration
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = secret
mysql = MySQL(app)

#app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cursor = mysql.connection.cursor()
            # кеширование
            #  name = generate_password_hash(name)
            cursor.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
            mysql.connection.commit()
            flash('OK', 'success')
        except:
            flash('NOT!!!!', 'danger')
    return render_template('index1.html')

@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM employee")
    if result>0:
        employees = cursor.fetchall()
        session['username'] = employees[0]['name']
        #return str(check_password_hash(employees[11]['name'],'password'))
        return render_template('employees.html', employees=employees)

if __name__ =='__main__':
    app.run(debug=True, port=5000)