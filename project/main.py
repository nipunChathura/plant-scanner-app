from flask import Flask, render_template, request, redirect
import mysql.connector
import yaml

app = Flask(__name__)
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_root']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ijse",
    database="plant_db"
)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        user_details = request.form
        email = user_details['email']
        password = user_details['password']
        cur = mysql.cursor()
        cur.execute("select * from users where email = %s and password = %s", (email, password))
        results = cur.fetchall()
        print(results)
        cur.close()
        return redirect('/image-upload')
    return render_template('index.html')


@app.route('/sing-up', methods=["GET", "POST"])
def sing_up():
    if request.method == 'POST':
        user_details = request.form
        name = user_details['name']
        email = user_details['email']
        password = user_details['password']
        cur = mysql.cursor()
        cur.execute("insert into users(name, email, password) values(%s, %s, %s)", (name, email, password))
        mysql.commit()
        cur.close()
        return redirect('/image-upload')
    return render_template('sing-up.html')


@app.route('/image-upload', methods=["GET", "POST"])
def image_upload():
    return render_template("imageupload.html")


if __name__ == "__main__":
    app.run(debug=True)
