.read lab12.sql

-- Q5
CREATE TABLE fa18favpets AS
  SELECT pet, count(pet)
  from students
  group by pet
  order by count(pet) DESC
  limit 10;


CREATE TABLE fa18dog AS
  SELECT * from fa18favpets where pet = "dog";


CREATE TABLE fa18alldogs AS
  SELECT pet, count(pet) from students where pet like "%dog%";


CREATE TABLE obedienceimages AS
  SELECT seven, denero ,count(*)
  from students
  where seven = '7'
  group by denero;

-- Q6
CREATE TABLE smallest_int_count AS 
  select smallest, count(*)
  from students
  group by smallest;
