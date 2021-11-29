#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='travel',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']


    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM user WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('home'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username  = request.form['username']
    password  = request.form['password']
    type_user = request.form['type_user']
    cursor = conn.cursor()
    if (type_user == 'cst'):
        query = "select * from customer where email = %s"
        cursor.execute(query, (username))
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('register.html', error = error)
        name = request.form['name']
        adrr_building_num = request.form['adrr_building_num']
        adrr_street = request.form['adrr_street']
        addr_city = request.form['addr_city']
        addr_state = request.form['addr_state']
        phone_num = request.form['phone_num']
        passport_num = request.form['passport_num']
        passport_exp = request.form['exp_date']
        passport_country = request.form['passport_country']
        date_of_birth = request.form['date_of_birth']
        ins  = 'insert into customer values('
        ins += '%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, name, adrr_building_num, adrr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth))
    elif (type_user == 'stf'):
        query = "select * from airline_staff where username = %s"
        cursor.execute(query, (username))
        #stores the results in a variable
        data = cursor.fetchone()
        #use fetchall() if you are expecting more than 1 data row
        error = None
        if(data):
            #If the previous query returns data, then user exists
            error = "This user already exists"
            return render_template('register.html', error = error)
        works = request.form['works']
        query = "select * from airline where name = %s"
        cursor.execute(query, (works))
        if not cursor.fetchone():
            error = "This company does not exists"
            return render_template('register.html', error = error)
        fname = request.form['fname']
        lname = request.form['lname']
        date_of_birth = request.form['date_of_birth']
        phone_nums = request.form['phone_nums'].split(', ')
        ins  = 'insert into airline_staff values ('
        ins += '%s, %s, %s, %s)'
        cursor.execute(ins, (username, password, fname, lname))
        for num in phone_nums:
            ins  = 'insert into staff_phonenum values ('
            ins += '%s, %s)'
            cursor.execute(ins, (username, num))
        query  = 'insert into works values ('
        query += '%s, %s)'
        cursor.execute(query, (username, works))
    conn.commit()
    cursor.close()
    return render_template('index.html')

@app.route('/home_cst')
def home_cst():
    
    # username = session['username']
    # cursor = conn.cursor();
    # query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    # cursor.execute(query, (username))
    # data1 = cursor.fetchall() 
    # for each in data1:
    #     print(each['blog_post'])
    # cursor.close()
    return render_template('home_cst.html')

@app.route('/getflightsbydatecst', methods=['GET', 'POST'])
def search_flights_date_cst():
    cursor = conn.cursor();
    source = request.form['source']
    dest = request.form['destination']
    dept_date = request.form['dept_date']
    query =  'select distinct o.airline_name, f.flight_num, a1.name '
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
    return render_template('home_cst.html', flights_by_date=data1)

@app.route('/getflightsbynumcst', methods=['GET', 'POST'])
def search_flights_num_cst():
    cursor = conn.cursor();
    airline = request.form['airline']
    flight_num = request.form['flight_num']
    arr_dept = request.form['arr_dept']
    query =  'select distinct f.status, f.flight_num, o.airline_name, f.base_price from flight f, airport a, operates o '
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
    return render_template('home_cst.html', flights_by_num=data1)
       
@app.route('/getflightsbydate', methods=['GET', 'POST'])
def search_flights_date():
    cursor = conn.cursor();
    source = request.form['source']
    dest = request.form['destination']
    dept_date = request.form['dept_date']
    query =  'select distinct o.airline_name, f.flight_num, a1.name, f.base_price '
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
    query =  'select distinct f.status, f.flight_num, o.airline_name from flight f, airport a, operates o '
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

@app.route('/buyhome')
def buyhome():
    return render_template('buyticket.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True) 
