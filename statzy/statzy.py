from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import secrets

statzy = Flask(__name__)
conn = None
cursor = None
statzy.secret_key = secrets.token_hex(16)


@statzy.route('/')
def index():
    title = 'Statzy'
    return render_template('login.html', title=title)


@statzy.route('/start')
def start():
    return render_template('index.html')


@statzy.route('/fachverfahren')
def fachverfahren():
    return render_template('fachverfahren.html')


@statzy.route('/server')
def server():
    return render_template('server.html')


@statzy.route('/komponenteServer')
def komponenteServer():
    return render_template('komponenteServer.html')


@statzy.route('/login', methods=['POST'])
def login():
    global conn, cursor
    username = request.form['username']
    password = request.form['password']

    print("Username:", username)
    print("Password:", password)

    try:
        conn = psycopg2.connect(
            dbname='statzy',
            user=username,
            password=password,
            host='localhost',
            port='5432'
        )

        cursor = conn.cursor()

        # Get the list of tables in the database
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        tables = [table[0] for table in cursor.fetchall()]

        # Store the username and password in the session
        session['username'] = username
        session['password'] = password
        print("Session:", session['username'])
        print("Session:", session['password'])
        # Redirect to the datenbanken page with the dropdown menu
        return redirect(url_for('start'))

    except Exception as e:
        print("Exception:", e)
        return 'Database connection failed! Login'


@statzy.route('/query', methods=['POST'])
def query():
    global conn, cursor
    table_name = request.form['table']
    try:
        # Execute the SELECT * query on the selected table
        cursor.execute(
            f"SELECT * FROM {table_name}")
        results = cursor.fetchall()

        # Render the template with the query results
        return render_template('query.html', table_name=table_name, results=results)
    except:
        return 'Database connection failed! Query'


@statzy.route('/datenbanken')
def datenbanken():
    global conn, cursor
    try:
        # Get the username and password from the session
        username = session.get('username', None)
        password = session.get('password', None)

        conn = psycopg2.connect(
            dbname='statzy',
            user=username,
            password=password,
            host='localhost',
            port='5432'
        )
        cursor = conn.cursor()

        # Get the list of tables in the database
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        tables = [table[0] for table in cursor.fetchall()]

        return render_template('datenbanken.html', tables=tables)

    except Exception as e:
        print("Exception:", e)
        return 'Database connection failed! Datenbanken'


if __name__ == '__main__':
    statzy.run(debug=True)
