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
    <html>

    <head>

        <title>Home Page</title>

        <style>

            *{
                margin:0;
                padding:0;
                box-sizing:border-box;
            }

            body{
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                font-family:Arial;
                background:linear-gradient(135deg,#74ebd5,#ACB6E5);
                overflow:hidden;
            }

            .box{
                background:white;
                padding:50px;
                border-radius:20px;
                text-align:center;
                box-shadow:0px 0px 20px rgba(0,0,0,0.3);
                animation:zoom 1s ease;
            }

            h1{
                margin-bottom:30px;
                color:#333;
            }

            a{
                text-decoration:none;
                background:#007bff;
                color:white;
                padding:12px 25px;
                border-radius:8px;
                display:inline-block;
                transition:0.4s;
            }

            a:hover{
                background:#0056b3;
                transform:scale(1.1);
            }

            @keyframes zoom{

                from{
                    transform:scale(0);
                    opacity:0;
                }

                to{
                    transform:scale(1);
                    opacity:1;
                }

            }

        </style>

    </head>

    <body>

        <div class="box">

            <h1>Welcome</h1>

            <a href="/register">Register</a>

            <br><br><br>

            <a href="/login">Login</a>

        </div>

    </body>

    </html>
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
    <html>

    <head>

        <title>Register</title>

        <style>

            body{
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:linear-gradient(135deg,#ff9a9e,#fad0c4);
                font-family:Arial;
            }

            .box{
                background:white;
                padding:40px;
                border-radius:20px;
                width:350px;
                text-align:center;
                box-shadow:0px 0px 20px rgba(0,0,0,0.3);
                animation:slide 1s ease;
            }

            h2{
                margin-bottom:20px;
            }

            input{
                width:100%;
                padding:12px;
                margin:10px 0;
                border:1px solid gray;
                border-radius:8px;
                outline:none;
            }

            .btn{
                background:green;
                color:white;
                border:none;
                cursor:pointer;
                transition:0.4s;
            }

            .btn:hover{
                background:darkgreen;
                transform:scale(1.05);
            }

            @keyframes slide{

                from{
                    transform:translateY(-100px);
                    opacity:0;
                }

                to{
                    transform:translateY(0);
                    opacity:1;
                }

            }

        </style>

    </head>

    <body>

        <div class="box">

            <h2>Register Form</h2>

            <form method="POST">

                <input type="text"
                name="name"
                placeholder="Enter Name"
                required>

                <input type="email"
                name="email"
                placeholder="Enter Email"
                required>

                <input type="password"
                name="password"
                placeholder="Enter Password"
                required>

                <input type="submit"
                value="Register"
                class="btn">

            </form>

        </div>

    </body>

    </html>
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
            <html>

            <head>

            <style>

                body{
                    height:100vh;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    background:linear-gradient(135deg,#89f7fe,#66a6ff);
                    font-family:Arial;
                }

                .success-box{
                    background:white;
                    padding:50px;
                    border-radius:20px;
                    text-align:center;
                    box-shadow:0px 0px 20px rgba(0,0,0,0.3);
                    animation:pop 1s ease;
                }

                h1{
                    color:green;
                    margin-bottom:20px;
                }

                h2{
                    color:#333;
                    margin-bottom:30px;
                }

                a{
                    text-decoration:none;
                    background:red;
                    color:white;
                    padding:12px 25px;
                    border-radius:8px;
                    transition:0.4s;
                    display:inline-block;
                }

                a:hover{
                    background:darkred;
                    transform:scale(1.1);
                }

                @keyframes pop{

                    0%{
                        transform:scale(0);
                        opacity:0;
                    }

                    100%{
                        transform:scale(1);
                        opacity:1;
                    }

                }

            </style>

            </head>

            <body>

                <div class="success-box">

                    <h1>Login Successful</h1>

                    <h2>Welcome ''' + name + '''</h2>

                    <a href="/logout">Logout</a>

                </div>

            </body>

            </html>
            '''

        else:

            return '''
            <html>

            <head>

            <style>

                body{
                    height:100vh;
                    display:flex;
                    justify-content:center;
                    align-items:center;
                    background:#ffe6e6;
                    font-family:Arial;
                }

                .error{
                    color:red;
                    font-size:30px;
                    animation:shake 0.5s;
                }

                @keyframes shake{

                    0%{transform:translateX(0);}
                    25%{transform:translateX(-10px);}
                    50%{transform:translateX(10px);}
                    75%{transform:translateX(-10px);}
                    100%{transform:translateX(0);}

                }

            </style>

            </head>

            <body>

                <div class="error">
                    Wrong Username or Password
                </div>

            </body>

            </html>
            '''

    return '''
    <html>

    <head>

        <title>Login</title>

        <style>

            body{
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:linear-gradient(135deg,#89f7fe,#66a6ff);
                font-family:Arial;
            }

            .box{
                background:white;
                padding:40px;
                border-radius:20px;
                width:320px;
                text-align:center;
                box-shadow:0px 0px 20px rgba(0,0,0,0.3);
                animation:slide 1s ease;
            }

            h2{
                margin-bottom:20px;
            }

            input{
                width:100%;
                padding:12px;
                margin:10px 0;
                border:1px solid gray;
                border-radius:8px;
                outline:none;
            }

            .btn{
                background:#007bff;
                color:white;
                border:none;
                cursor:pointer;
                transition:0.4s;
            }

            .btn:hover{
                background:#0056b3;
                transform:scale(1.05);
            }

            @keyframes slide{

                from{
                    transform:translateY(-100px);
                    opacity:0;
                }

                to{
                    transform:translateY(0);
                    opacity:1;
                }

            }

        </style>

    </head>

    <body>

        <div class="box">

            <h2>Login Form</h2>

            <form method="POST">

                <input type="text"
                name="name"
                placeholder="Enter Name"
                required>

                <input type="password"
                name="password"
                placeholder="Enter Password"
                required>

                <input type="submit"
                value="Login"
                class="btn">

            </form>

        </div>

    </body>

    </html>
    '''


# Logout Page
@app.route('/logout')
def logout():

    return redirect('/')


# Run App
app.run(debug=True)