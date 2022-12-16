from flask import Flask, render_template, url_for, redirect, request
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
import yaml 

app = Flask(__name__)
Bootstrap(app)

#DB configuration
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


#@app.route('/')
#def index():
    
    #cursor.execute('DELETE FROM user WHERE user_name="John"')
    #mysql.connection.commit()
    #resut = cursor.execute('SELECT*FROM user')
    #if resut>0:
    #    users = cursor.fetchall()
    #    return str(users)
    #cursor = mysql.connection.cursor()
    #if cursor.execute("INSERT INTO user(user_name) VALUES ('PITER')"):
    #    mysql.connection.commit()
    #    return 'Success!', 201
    #return render_template('index.html')

#@app.route('/about')
#def about():
#    return render_template('about.html')
#@app.errorhandler(404)
#def page_not_found(e):
    #return 'OOps This page was not found :('
#    return render_template('error.html')

#@app.route('/css')
#def css():
#    return render_template('css.html')

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        age = form['age']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employee(name, age) VALUES(%s, %s)", (name, age))
        mysql.connection.commit()
    return render_template('index1.html')

@app.route('/employees')
def employees():
    cursor = mysql.connection.cursor()
    result = cursor.execute("SELECT * FROM employee")
    if result>0:
        employees = cursor.fetchall()
        return render_template('employees.html', employees=employees)

if __name__ =='__main__':
    app.run(debug=True, port=5000)