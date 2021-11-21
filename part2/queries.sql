-- Jose Bolanos
-- Jaeha Huh

select * from flight where dept_date_time > now();

select * from flight where status = 'delayed';

select distinct c.name from customer c, purchase p where p.email = c.email;

select distinct id from own where airline_name = 'China Eastern';
