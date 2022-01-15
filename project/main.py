import torch
from flask import Flask, render_template, request, redirect
import mysql.connector
import tkinter
from tkinter import messagebox
from PIL import Image
from torch import nn
from torchvision import transforms

app = Flask(__name__)

mysql = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ijse",
    database="plant_db"
)

model = nn.Sequential(
    nn.Linear(784, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 10),
    nn.LogSoftmax(dim=1)
)
status_dict = torch.load("model.path")
model.load_state_dict(status_dict)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if request.form['btn'] == 'Login':
            user_details = request.form
            email = user_details['email']
            password = user_details['password']
            cur = mysql.cursor()
            cur.execute("select * from users where email = %s and password = %s", (email, password))
            results = cur.fetchall()
            print(results)
            cur.close()
            if results is None:
                return "User Name And Password incorrect"
            else:
                return redirect('/image-upload')
        elif request.form['btn'] == 'Sing Up':
            return render_template('sing-up.html')
    return render_template('index.html')


@app.route('/sing-up', methods=["GET", "POST"])
def sing_up():
    if request.method == 'POST':
        if request.form['btn'] == 'Sing Up':
            user_details = request.form
            name = user_details['name']
            email = user_details['email']
            password = user_details['password']
            cur = mysql.cursor()
            cur.execute("insert into users(name, email, password) values(%s, %s, %s)", (name, email, password))
            mysql.commit()
            cur.close()
            return redirect('/image-upload', )
        elif request.form['btn'] == 'Login':
            return render_template('index.html')
    return render_template('sing-up.html')


@app.route('/image-upload', methods=["GET", "POST"])
def image_upload():
    if request.method == "POST":
        file = request.files["image"]
        img = Image.open(file)
        img = transforms.ToTensor()(img)
        print(img)
        img = img.view(1, 784)
        pred = model(img)

        return "upload"
    return render_template("imageupload.html")


if __name__ == "__main__":
    app.run(debug=True)
