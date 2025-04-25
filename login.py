from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(100), unique=True, nullable=False)
   password_hash = db.Column(db.String(100), nullable=False)

def create_tables():
   with app.app_context():
       db.create_all()

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
   username = request.form['username']
   password = request.form['password']
  
   user = User.query.filter_by(username=username).first()
  
   if user and check_password_hash(user.password_hash, password):
       session['username'] = username
       return redirect(url_for('dashboard')) # redirect to dashboard
   else:
       return render_template('login.html', error='Invalid username or password')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(username=session['username']).first()
    return render_template('dashboard.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       username = request.form['username']
       password = request.form['password']

       existing_user = User.query.filter_by(username=username).first() # check if user already exist
       if existing_user:
           return render_template('register.html', error="Username already exists. Please choose a different one.")
      
       password_hash = generate_password_hash(password)
       
       new_user = User(username=username, password_hash=password_hash)
       db.session.add(new_user)
       db.session.commit()
      
       return redirect(url_for('login'))
  
   return render_template('register.html')

create_tables()

if __name__ == "__main__":
   app.run(debug=True)