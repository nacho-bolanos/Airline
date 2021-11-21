-- Jose Bolanos
-- Jaeha Huh

create table customer (
    email varchar(100) primary key,
    password varchar(50),
    name varchar(50),
    adrr_building_num int,
    adrr_street varchar(100),
    addr_city varchar(100),
    addr_state varchar(50),
    phone_num int,
    passport_num int,
    passport_exp date,
    passport_country varchar(100),
    date_of_birth date
);

create table airport (
    code varchar(10) primary key,
    name varchar(50),
    city varchar(100)
);

create table airline (
    name varchar(50) primary key
);

create table airline_staff (
    username varchar(50) primary key,
    password varchar(50),
    fname varchar(50),
    lname varchar(50)
);

create table works (
    username varchar(50) primary key,
    airline_name varchar(50), 
    foreign key (airline_name) references airline(name)
);

create table staff_phonenum(
    username varchar(50),
    phone_num int primary key,
    foreign key (username) references airline_staff(username)
);

create table airplane (
    id varchar(50) primary key,
    seats int 
);

create table own (
    airline_name varchar(50), 
    id varchar(50), 
    foreign key (airline_name) references airline(name),
    foreign key (id) references airplane(id)

);

create table flight (
    flight_num int,
    dept_airport varchar(10),
    dept_date_time datetime ,
    arr_airport varchar(10),
    arr_date_time datetime,
    base_price int,
    status varchar(25),
    foreign key (dept_airport) references airport(code),
    foreign key (arr_airport) references airport(code),
    primary key (flight_num, dept_date_time)
);

create table operates (
    airline_name varchar(50),
    flight_num int, 
    foreign key (airline_name) references airline(name),
    foreign key (flight_num) references flight(flight_num)
);

create table use_plane (
    id varchar(50) ,
    flight_num int, 
    foreign key (id) references airplane(id),
    foreign key (flight_num) references flight(flight_num)
);

create table rate (
    flight_num int,
    email varchar(100) ,
    rating int,
    comments varchar(500),
    foreign key (flight_num)  references flight(flight_num),
    foreign key (email ) references customer(email) 
);

create table ticket (
    ticket_id int primary key
);

create table flight_info (
    sold_price int,
    flight_num int ,
    ticket_id int, 
    foreign key (flight_num) references flight(flight_num),
    foreign key (ticket_id) references ticket(ticket_id) 
);

create table purchase (
    email varchar(100) ,
    ticket_id int ,
    card_type varchar(10),
    card_num int,
    card_name varchar(50),
    card_exp date,
    purchase_date_time datetime,
    capacity int,
    foreign key (email) references customer(email),
    foreign key (ticket_id) references ticket(ticket_id)
);
