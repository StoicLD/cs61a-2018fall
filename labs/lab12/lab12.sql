.read fa18data.sql

-- Q2
CREATE TABLE obedience AS
  SELECT seven ,denero from students;

-- Q3
CREATE TABLE smallest_int AS
  SELECT time, smallest from students where smallest > 13
    order by smallest limit 20;

-- Q4
CREATE TABLE matchmaker AS
  select A.pet, A.song, A.color, B.color from
    students as A , students as B where
    A.pet = B.pet and A.song = B.song and A.time < B.time;
