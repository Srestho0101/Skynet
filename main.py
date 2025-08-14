from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database setup -------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://skynet.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 🔹 Model (table)
class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    threat_level = db.Column(db.String(20), nullable=False)

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
  return render_template('login.html')

@app.route("/<username>")
def user(username):
  return render_template('user.html', username=username)

if __name__ == '__main__':
  app.run(debug=True)
  
# /data/data/com.termux/files/home/storage/shared/Skynet