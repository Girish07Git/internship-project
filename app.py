from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.secret_key = "secretkey"
# SQLite Database
connection = sqlite3.connect(
    'users.db',
    check_same_thread=False
)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT,
    email TEXT UNIQUE,
    password_hash TEXT,
    role TEXT
)
""")

connection.commit()
@app.route('/')
def home():
    return render_template('home.html')


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
        check_sql = "SELECT * FROM users WHERE email=?"

        cursor.execute(check_sql, (email,))

        existing_user = cursor.fetchone()

        if existing_user:

            return "Email already registered"

        sql = """
        INSERT INTO users(full_name,email,password_hash,role)
        VALUES(?,?,?,?)
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

        sql = "SELECT * FROM users WHERE email=?"

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
SET password_hash=?
WHERE email=?
"""

        cursor.execute(sql, (password, email))

        connection.commit()

        return redirect('/login')

    return render_template('forgot_password.html')
@app.route('/budget')
def budget():

    if 'user' in session:
        return render_template('budget.html')

    return redirect('/login')


@app.route('/budget-result', methods=['POST'])
def budget_result():

    income = float(request.form['income'])
    rent = float(request.form['rent'])
    food = float(request.form['food'])
    transport = float(request.form['transport'])
    shopping = float(request.form['shopping'])

    total_expense = rent + food + transport + shopping

    savings = income - total_expense

    if savings < 0:
        advice = "Your expenses are higher than income."
    elif savings < income * 0.2:
        advice = "Try to save at least 20% of your income."
    else:
        advice = "Excellent savings habit."

    return render_template(
        'budget_result.html',
        income=income,
        expense=total_expense,
        savings=savings,
        advice=advice
    )
@app.route('/manage-home')
def manage_home():

    if 'user' in session:
        return render_template('manage_home.html')

    return redirect('/login')


@app.route('/manage-features', methods=['GET', 'POST'])
def manage_features():

    if request.method == 'POST':

        feature_name = request.form['feature_name']
        icon = request.form['icon']

        return f"Feature Added Successfully : {feature_name}"

    return render_template('manage_features.html')


@app.route('/manage-statistics')
def manage_statistics():

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")

    total_users = cursor.fetchone()[0]

    return render_template(
        'manage_statistics.html',
        total_users=total_users
    )

@app.route('/manage-about')
def manage_about():

    if 'user' in session:
        return render_template('manage_about.html')

    return redirect('/login')


@app.route('/manage-slider')
def manage_slider():

    if 'user' in session:
        return render_template('manage_slider.html')

    return redirect('/login')
# Logout
@app.route('/logout')

def logout():

    session.pop('user', None)

    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
   
   