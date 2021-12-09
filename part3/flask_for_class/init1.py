#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

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

#Define route for rating
@app.route('/rating')
def rating():
    username = session['username']
    cursor = conn.cursor()
    query = 'select distinct flight_num, rating, comments from rate where email = %s'
    cursor.execute(query, (username))
    rates = cursor.fetchall()
    for line in rates:
        print(line)
    return render_template('rating.html', rates=rates)

@app.route('/pushRating', methods=['GET', "POST"])
def pushRate():
    username = session['username']
    flight_num = request.form['flight_num']
    num_rate = request.form['rating']
    comment = request.form['comment']
    cursor = conn.cursor()
    query = 'select * from purchase where flight_num = %s and email = %s'
    cursor.execute(query, (flight_num, username))
    onthisflight = cursor.fetchall()
    error = None
    print(onthisflight)
    if not onthisflight:
        error = "Customer did not take this flight, can't rate."
        return render_template('rating.html', error=error)
    query = 'select * from flight where flight_num = %s and dept_date_time < SYSDATE()'
    cursor.execute(query, (flight_num))
    tookflight = cursor.fetchall()
    error = None
    if not tookflight:
        error = "Flight has not yet passed, can't rate."
        return render_template('rating.html', error=error)
    query  = 'insert into rate values( '
    query += '%s, %s, %s, %s)'
    cursor.execute(query, (flight_num, username, num_rate, comment))
    print(cursor.fetchall())
    conn.commit()
    cursor.close()
    return redirect(url_for('rating'))

# Define route for history
@app.route('/history')
def history():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    username = session['username']
    cursor = conn.cursor()
    query = 'select sum(fi.sold_price) from flight_info fi, purchase p where p.email = %s and p.purchase_date_time between date_sub(now(), interval 1 year) and now() and fi.ticket_id = p.ticket_id'
    cursor.execute(query, (username))
    total_spent = cursor.fetchone()
    total_spent = total_spent.get('sum(fi.sold_price)')
    curr_month = datetime.today().month - 1
    past_six = {}
    rest = 0
    if curr_month - 6 < 0:
        rest = (curr_month - 6) * -1
        for i in range(6 - rest):
            past_six[months[curr_month - i]] = 0
        for i in range(rest):
            past_six[months[i]] = 0
    else:
        for i in range(6):
            past_six[months[curr_month - i]] = 0
    for month in past_six:
        query = 'select sum(fi.sold_price) from flight_info fi, purchase p where p.email = %s and monthname(p.purchase_date_time) = %s and fi.ticket_id = p.ticket_id'
        cursor.execute(query, (username, month))
        total_spent_month = cursor.fetchone()
        total_spent_month = total_spent_month.get('sum(fi.sold_price)')
        if total_spent_month:
            past_six[month] = total_spent_month
    query = 'select o.airline_name, f.flight_num, a1.name as arr_name, f.arr_date_time, a2.name as dept_name, f.dept_date_time from flight f, operates o, purchase p, airport a1, airport a2 where f.flight_num = o.flight_num and f.flight_num = p.flight_num and p.email = %s and a1.code = f.arr_airport and a2.code = f.dept_airport'
    cursor.execute(query, (username))
    bought_flights = cursor.fetchall()
    return render_template('history_cst.html', total_spent=total_spent, past_six=past_six, bought_flights=bought_flights)

@app.route('/gethistorybydate', methods=['GET', 'POST'])
def gethistorybydate():
    username = session['username']
    cursor = conn.cursor()
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    start_month = start_date.split('-')[2] + ' ' + datetime.strptime(start_date.split('-')[1], '%m').strftime('%B')
    end_month = end_date.split('-')[2] + ' ' + datetime.strptime(end_date.split('-')[1], '%m').strftime('%B')

    print(start_date, end_date)
    if start_date > end_date:
        return redirect(url_for('history'))
    query = 'select sum(fi.sold_price) from flight_info fi, purchase p where p.email = %s and p.purchase_date_time between date(%s) and date(%s) and fi.ticket_id = p.ticket_id'
    cursor.execute(query, (username, start_date, end_date))
    total_spent = cursor.fetchone()['sum(fi.sold_price)']
    query = 'select date(p.purchase_date_time), p.ticket_id, fi.sold_price as sale_price from purchase p, flight_info fi where p.email = %s and date(p.purchase_date_time) between date(%s) and date(%s) and fi.ticket_id = p.ticket_id'
    cursor.execute(query, (username, start_date, end_date))
    history_date = cursor.fetchall()
    for line in history_date:
        print(line)
    return render_template('history_cst.html', total_spent_interval=total_spent, start_month=start_month, end_month=end_month, history_date=history_date)

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
        print(query)
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
        if loginType == 'customer':
            return redirect(url_for('home_cst'))
        elif loginType == 'works':
            return redirect(url_for('home_stf'))
    else:
        # returns an error message to the html page
        error = 'Invalid login or username'
        #To display errors
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
        ins     = 'insert into customer values('
        ins += '%s, md5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
        ins += '%s, md5(%s), %s, %s)'
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
    
    username = session['username']
    print(username)
    cursor = conn.cursor();
    query = 'select name from customer where email = %s'
    cursor.execute(query, (username))
    cst_name = cursor.fetchone() 
    return render_template('home_cst.html', name=cst_name['name'])

@app.route('/getflightsbydatecst', methods=['GET', 'POST'])
def search_flights_date_cst():
    cursor = conn.cursor();
    username = session['username']
    source = request.form['source']
    dest = request.form['destination']
    dept_date = request.form['dept_date']
    query =  'select distinct o.airline_name, f.flight_num, a1.name '
    query += 'as arr_name, f.dept_date_time, a2.name as dept_name, f.new_price, f.arr_date_time from flight f, operates o, airport a1, airport a2 '
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
    query = 'select name from customer where email = %s'
    cursor.execute(query, (username))
    cst_name = cursor.fetchone() 
    cursor.close()
    return render_template('home_cst.html', flights_by_date=data1, name=cst_name['name'])

@app.route('/getflightsbynumcst', methods=['GET', 'POST'])
def search_flights_num_cst():
    cursor = conn.cursor();
    username = session['username']
    airline = request.form['airline']
    flight_num = request.form['flight_num']
    arr_dept = request.form['arr_dept']
    query =  'select distinct f.status, f.flight_num, o.airline_name, f.new_price, f.dept_date_time from flight f, airport a, operates o '
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
        if each['dept_date_time'] <= datetime.now():
            each['passed'] = 1
        print(each)
    query = 'select name from customer where email = %s'
    cursor.execute(query, (username))
    cst_name = cursor.fetchone() 
    cursor.close()
    return render_template('home_cst.html', flights_by_num=data1, name=cst_name['name'])
       
@app.route('/getflightsbydate', methods=['GET', 'POST'])
def search_flights_date():
    cursor = conn.cursor();
    source = request.form['source']
    dest = request.form['destination']
    dept_date = request.form['dept_date']
    query =  'select distinct o.airline_name, f.flight_num, a1.name, f.new_price '
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

@app.route('/buyhome/<flight_num>/<airline>', methods=['GET', 'POST'])
def buyhome(flight_num, airline):
    print(flight_num, airline)
    return render_template('buyticket.html', flight_num=flight_num, airline=airline)

@app.route('/buyticket/<flight_num>/<airline>', methods=['GET', 'POST'])
def buyticket(flight_num, airline):
    cursor = conn.cursor()
    username = session['username']
    card_type = request.form['card_type']
    card_name = request.form['card_name']
    card_num = request.form['card_num']
    card_exp = request.form['card_exp']
    query = 'select max(ticket_id) from ticket'
    cursor.execute(query)
    ticket_id = cursor.fetchone()['max(ticket_id)'] + 1
    query = 'select * from flight where flight_num = %s'
    cursor.execute(query, (flight_num))
    flight_info = cursor.fetchone()
    if flight_info['dept_date_time'] <= datetime.now():
        return render_template('home_cst.html')
    query = 'select ap.seats from operates o, airplane ap where flight_num = %s and o.id = ap.id'
    cursor.execute(query, (flight_num))
    seats = cursor.fetchone()['seats']
    per_seat = 1 / seats
    new_price = flight_info['base_price']
    flight_info['capacity'] += per_seat
    if flight_info['capacity'] >= 0.75:
        query = 'update flight set new_price = %s where flight_num = %s'
        new_price *= 1.25
        cursor.execute(query, (new_price, flight_num))
    query = 'insert into ticket values(%s)'
    cursor.execute(query, (ticket_id))
    query = 'insert into purchase values(%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (username, ticket_id, card_type, card_num, card_name, card_exp, datetime.now(), flight_num))
    query = 'update flight set capacity = % where flight_num = %s'
    print(flight_info['capacity'])
    cursor.execute(query, (flight_info['capacity'], flight_num))
    query = 'insert into flight_info values(%s, %s, %s)'
    cursor.execute(query, (new_price, flight_num, ticket_id))
    return render_template('buyticket.html')



#Staff
@app.route('/home_stf')
def home_stf():
    username = session['username']
    print(username)
    cursor = conn.cursor()
    query = 'select fname from airline_staff where email = %s'
    cursor.execute(query, (username))
    stf_name = cursor.fetchone()
    return render_template('home_stf.html', name=stf_name['fname'])

@app.route('/view_flights_stf', methods=['GET','POST'])
def view_flights_stf():
    cursor = conn.cursor()
    username = session['username']
    query = 'SELECT * FROM flight, works where dept_date_time >= NOW() AND dept_date_time < NOW() + INTERVAL 1 MONTH'

    cursor.execute(query)
    conn.commit()
    cursor.fetchall()
    cursor.close()

    return render_template('view_flights_stf.html')

@app.route('/manage_flights', methods=['GET','POST'])
def create_flight():
    cursor = conn.cursor()
    username = session['username']
    flight_num = request.form['flight_num']
    dept_airport = request.form['dept_airport']
    dept_date_time = request.form['dept_date_time']
    arr_airport = request.form['arr_airport']
    arr_date_time = request.form['arr_date_time']
    base_price = request.form['base_price']
    new_price = request.form['new_price']
    status = request.form['status']
    capacity = request.form['capacity']
    query = 'insert into flight values(%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(query, (flight_num, dept_airport, dept_date_time, arr_airport, arr_date_time, base_price, new_price, status, capacity))

    return render_template('manage_flights.html')

@app.route('/manage_flights/<flight_num>/<airline>', methods=['GET','POST'])
def status_flight(flight_num, airline):
    cursor = conn.cursor()
    username = session['username']
    status = request.form['status']
    query = 'Update flight SET status'
    cursor.execute(query, (status, flight_num))
    cursor.fetchall()
    cursor.close()
    return render_template('manage_flights.html')

@app.route('/manage_airplane', methods=['GET','POST'])
def add_airplane():
    cursor = conn.cursor()
    username = session['username']
    id = request.form['id']
    seats = request.form['seats']
    query = 'insert into airplane values(%s, %s)'
    cursor.excute(query, (id, seats))

    return render_template('manage_airplane.html')

@app.route('/manage_airport', methods=['GET','POST'])
def add_airport():
    cursor = conn.cursor()
    username = session['username']
    code = request.form['code']
    name = request.form['name']
    query = 'insert into airplane values(%s, %s)'
    cursor.excute(query, (code, name))
    return render_template('manage_airport.html')


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
