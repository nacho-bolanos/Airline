-- Jose Bolanos
-- Jaeha Huh

insert into airline (name) values ("China Eastern");

insert into airport (code, name, city) values ("JFK", "John F. Kennedy International Airport", "NYC");
insert into airport (code, name, city) values ("PVG", "Shanghai Pudong International Airport", "Shanghai");

insert into customer (email, password, name, adrr_building_num, adrr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("jose@gmail.com", md5("himynameisjose"), "Jose Bolanos", 6, "Metrotech", "Brooklyn", "New York", 1234567, 111111, '2024-12-20', "Guatemala", '2000-09-21');

insert into customer (email, password, name, adrr_building_num, adrr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("jaeha@gmail.com", md5("himynameisjaeha"), "Jaeha Huh", 6, "Metrotech", "Brooklyn", "New York", 128723947, 112344, '2024-04-12', "United States", '2000-04-15');    

insert into customer (email, password, name, adrr_building_num, adrr_street, addr_city, addr_state, phone_num, passport_num, passport_exp, passport_country, date_of_birth) 
values ("mat@gmail.com", md5("himynameismat"), "Mat Brown", 6, "Metrotech", "Brooklyn", "New York", 29759472, 1287398, '2023-11-16', "United States", '1999-12-30');

insert into airplane (id, seats) values ("Boeing 737-800", 160);
insert into airplane (id, seats) values ("Boeing 737-700", 143);
insert into airplane (id, seats) values ("Airbus A320ceo", 168);

insert into own (airline_name, id) values ('China Eastern', 'Boeing 737-800');
insert into own (airline_name, id) values ('China Eastern', 'Boeing 737-700');
insert into own (airline_name, id) values ('China Eastern', 'Airbus A320ceo');

insert into airline_staff (username, password, fname, lname) 
values ("john@gmail.com", md5("youcantseeme"), "John", "Cena");

insert into works (username, airline_name) values ("john@gmail.com", "China Eastern");

insert into flight (flight_num, dept_airport, dept_date_time, arr_airport, arr_date_time, base_price, new_price, status, capacity)
values (123, "JFK", "2021-11-11 13:45:00", "PVG", '2021-11-12 01:00:00', 240, 240, "ontime", 0);

insert into flight (flight_num, dept_airport, dept_date_time, arr_airport, arr_date_time, base_price, new_price, status, capacity)
values (234, "JFK", '2021-09-11 16:30:00', "PVG", '2021-09-12 04:00:00', 540, 540, "delayed", 0);

insert into flight (flight_num, dept_airport, dept_date_time, arr_airport, arr_date_time, base_price, new_price, status, capacity)
values (124, "PVG", '2021-12-04 09:15:00', "JFK", '2021-12-05 23:00:00', 375, 375, "ontime", 0);

insert into operates (airline_name, flight_num, id) values ('China Eastern', 123, 'Boeing 737-800' );
insert into operates (airline_name, flight_num, id) values ('China Eastern', 234, 'Airbus A320ceo');
insert into operates (airline_name, flight_num, id) values ('China Eastern', 124, 'Boeing 737-800');

insert into ticket (ticket_id) values (1);
insert into ticket (ticket_id) values (2);
insert into ticket (ticket_id) values (3);
insert into ticket (ticket_id) values (4);
insert into ticket (ticket_id) values (5);
insert into ticket (ticket_id) values (8);

insert into flight_info (flight_num, ticket_id, sold_price) values (123, 1, 240);
insert into flight_info (flight_num, ticket_id, sold_price) values (123, 2, 240);
insert into flight_info (flight_num, ticket_id, sold_price) values (123, 1, 240);
insert into flight_info (flight_num, ticket_id, sold_price) values (234, 4, 540);
insert into flight_info (flight_num, ticket_id, sold_price) values (234, 5, 540);
insert into flight_info (flight_num, ticket_id, sold_price) values (124, 8, 375);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num) 
values ("jaeha@gmail.com", 1, "credit", 1234566787, "Jaeha Huh", '2024-09-01', '2021-11-10 11:00:00', 123);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num ) 
values ("jose@gmail.com", 2, "credit", 1234566787, "Jose Bolanos", '2024-10-01', '2021-09-10 14:00:00', 123);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num ) 
values ("mat@gmail.com", 3, "debit", 1234566787, "Mat Brown", '2024-01-01', '2021-11-10 18:00:00', 124);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num ) 
values ("jaeha@gmail.com", 4, "credit", 1234566787, "Jaeha Huh", '2024-09-01', '2021-08-10 12:00:00', 234);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num) 
values ("jose@gmail.com", 5, "credit", 1234566787, "Jose Bolanos", '2024-10-01', '2021-09-10 14:00:00', 124);

insert into purchase (email, ticket_id, card_type, card_num, card_name, card_exp, purchase_date_time, flight_num) 
values ("mat@gmail.com", 8, "debit", 1234566787, "Mat Brown", '2024-01-01', '2021-11-18 20:00:00', 234);

