# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='1234',
                       db='travel',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


# Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')


# Define route for login
@app.route('/login')
def login():
    return render_template('login.html')


# Define route for register
@app.route('/register')
def register():
    return render_template('register.html')


# Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    loginType = request.form['type']
    print(loginType)
    # cursor used to send queries
    cursor = conn.cursor()
    query =''
    # executes query

    #The sql statement changes according to the radio button(html).
    #Since the PW is md5 encrypted, it will be accurately authenticated by md5(%s) when it is retrieved.
    if loginType == 'customer':
        query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
    elif loginType == 'works':
        query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'

    print(query)
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        # creates a session for the the user
        # session is a built in
        session['username'] = username
        #This is the part that goes to @app.route('/home').
        return redirect(url_for('home'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        #To display errors
        return render_template('login.html', error=error)


# Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    type_user = request.form['type_user']
    phone_nums = request.form['phone_nums']

    print(type_user)
    print(phone_nums)
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    if (type_user == 'cst'):
        query = ""
    query = 'SELECT * FROM customer where email = %s'
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if (data):
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s)'
        cursor.execute(ins, (username, password))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/home')
def home():
    # 2가지의 home.html로 나누어야합니다.
    # @app.route('/home-customer')
    # @app.route('/home-workds') 따로 만들어서 작업하시길 바랍니다.
    '''
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall()
    for each in data1:
        print(each['blog_post'])
    cursor.close()

    return render_template('home.html', username=username, posts=data1)
    '''
    return render_template('home.html')


@app.route('/getflightsbydate', methods=['GET', 'POST'])
def search_flights_date():
    cursor = conn.cursor();
    source = request.form['source']
    dest = request.form['destination']
    dept_date = request.form['dept_date']
    query = 'select distinct o.airline_name, f.flight_num, a1.name '
    query += 'as arr_name, f.dept_date_time, a2.name as dept_name, f.arr_date_time from flight f, operates o, airport a1, airport a2 '
    query += 'where ((f.flight_num = o.flight_num and a1.code = f.arr_airport '
    query += 'and a2.code = f.dept_airport '
    query += 'and ("{}" = a1.city or "{}" = a1.name or "{}" = a1.code) '.format(dest, dest, dest)
    query += 'and ("{}" = a2.city or "{}" = a2.name or "{}" = a2.code) '.format(source, source, source)
    query += 'and (date(f.dept_date_time) = "{}"))'.format(dept_date)
    if "return_date" in request.form:
        return_date = request.form['return_date']
        query += 'or ((f.flight_num = o.flight_num and a1.code = f.arr_airport '
        query += 'and a2.code = f.dept_airport '
        query += 'and ("{}" = a2.city or "{}" = a2.name or "{}" = a2.code) '.format(dest, dest, dest)
        query += 'and ("{}" = a1.city or "{}" = a1.name or "{}" = a1.code) '.format(source, source, source)
        query += 'and (date(f.dept_date_time) = "{}")))'.format(return_date)
    query += ')'
    # print(query)
    cursor.execute(query)
    conn.commit()
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('index.html', flights_by_date=data1)


@app.route('/getflightsbynum', methods=['GET', 'POST'])
def search_flights_num():
    cursor = conn.cursor();
    airline = request.form['airline']
    flight_num = request.form['flight_num']
    arr_dept = request.form['arr_dept']
    query = 'select distinct f.status, f.flight_num, o.airline_name from flight f, airport a, operates o '
    query += 'where f.flight_num = "{}" '.format(flight_num)
    query += 'and o.flight_num = f.flight_num '
    query += 'and o.airline_name = "{}" '.format(airline)
    query += 'and (f.arr_airport = a.code or f.dept_airport = a.code) '
    query += 'and (a.code = "{}" or a.name = "{}" or a.city = "{}") '.format(arr_dept, arr_dept, arr_dept)
    print(query)
    cursor.execute(query)
    conn.commit()
    data1 = cursor.fetchall()
    for each in data1:
        print(each)
    cursor.close()
    return render_template('index.html', flights_by_num=data1)


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


app.secret_key = 'some key that you will never guess'

# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
