from flask import Flask, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database
conn = sqlite3.connect("users.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()


# Home Page
@app.route('/')
def home():

    return '''
    <h1 style="text-align:center;">Welcome</h1>

    <div style="text-align:center; margin-top:50px;">

        <a href="/register">Register</a>

        <br><br>

        <a href="/login">Login</a>

    </div>
    '''


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("users.db")

        conn.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return '''

    <h1>Register</h1>

    <form method="POST">

        <input type="text"
        name="name"
        placeholder="Enter Name"
        required>

        <br><br>

        <input type="email"
        name="email"
        placeholder="Enter Email"
        required>

        <br><br>

        <input type="password"
        name="password"
        placeholder="Enter Password"
        required>

        <br><br>

        <input type="submit"
        value="Register">

    </form>
    '''


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        name = request.form['name']
        password = request.form['password']

        conn = sqlite3.connect("users.db")

        cursor = conn.execute(
            "SELECT * FROM users WHERE name=? AND password=?",
            (name, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            return '''

            <h1 style="color:green;">
            Login Successful
            </h1>

            <h2>
            Welcome ''' + name + '''
            </h2>

            <a href="/logout">Logout</a>

            '''

        else:

            return '''

            <h1 style="color:red;">
            Wrong Username or Password
            </h1>

            '''

    return '''

    <h1>Login</h1>

    <form method="POST">

        <input type="text"
        name="name"
        placeholder="Enter Name"
        required>

        <br><br>

        <input type="password"
        name="password"
        placeholder="Enter Password"
        required>

        <br><br>

        <input type="submit"
        value="Login">

    </form>
    '''


# Logout
@app.route('/logout')
def logout():

    return redirect('/')


# Run App
app.run(debug=True)