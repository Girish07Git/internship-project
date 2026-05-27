from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import pymysql

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "secretkey"
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    database='user_auth_db'
)
@app.route('/')
def home():
    return redirect('/register')


# Registration Page
@app.route('/register', methods=['GET', 'POST'])

def register():

    if request.method == 'POST':

        full_name = request.form['full_name']
        email = request.form['email']

        password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        role = request.form['role']

        cursor = connection.cursor()

        # Check duplicate email
        check_sql = "SELECT * FROM users WHERE email=%s"

        cursor.execute(check_sql, (email,))

        existing_user = cursor.fetchone()

        if existing_user:

            return "Email already registered"

        sql = """
        INSERT INTO users(full_name,email,password_hash,role)
        VALUES(%s,%s,%s,%s)
        """

        cursor.execute(sql, (full_name, email, password, role))

        connection.commit()

        return redirect('/login')

    return render_template('register.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])

def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor()

        sql = "SELECT * FROM users WHERE email=%s"

        cursor.execute(sql, (email,))

        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[3], password):

            session['user'] = user[1]

            session['role'] = user[4]

            return redirect('/dashboard')

        else:

            return "Invalid Email or Password"

    return render_template('login.html')

# Dashboard
#s
@app.route('/dashboard')
def dashboard():

    if 'user' in session:

        return render_template('dashboard.html')

    return redirect('/login')
# Forgot Password
@app.route('/forgot-password', methods=['GET', 'POST'])

def forgot_password():

    if request.method == 'POST':

        email = request.form['email']

        password = bcrypt.generate_password_hash(
            request.form['password']
        ).decode('utf-8')

        cursor = connection.cursor()

        sql = """
        UPDATE users
        SET password_hash=%s
        WHERE email=%s
        """

        cursor.execute(sql, (password, email))

        connection.commit()

        return redirect('/login')

    return render_template('forgot_password.html')
# Logout
@app.route('/logout')

def logout():

    session.pop('user', None)

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
   
   