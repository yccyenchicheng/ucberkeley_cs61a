-------------------------------------------------------------
                                                   -- DOGS --
-------------------------------------------------------------

create table parents as
  select "abraham" as parent, "barack" as child union
  select "abraham"          , "clinton"         union
  select "delano"           , "herbert"         union
  select "fillmore"         , "abraham"         union
  select "fillmore"         , "delano"          union
  select "fillmore"         , "grover"          union
  select "eisenhower"       , "fillmore";

create table dogs as
  select "abraham" as name, "long" as fur, 26 as height union
  select "barack"         , "short"      , 52           union
  select "clinton"        , "long"       , 47           union
  select "delano"         , "long"       , 46           union
  select "eisenhower"     , "short"      , 35           union
  select "fillmore"       , "curly"      , 32           union
  select "grover"         , "short"      , 28           union
  select "herbert"        , "curly"      , 31;

create table sizes as
  select "toy" as size, 24 as min, 28 as max union
  select "mini",        28,        35        union
  select "medium",      35,        45        union
  select "standard",    45,        60;

-------------------------------------------------------------
    -- PLEASE DO NOT CHANGE ANY DOG TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- The size of each dog
create table size_of_dogs as
  select name, size FROM dogs, sizes WHERE height > min AND height <= max;

-- All dogs with parents ordered by decreasing height of their parent
create table by_height as
  select a.name FROM parents, dogs AS a, dogs AS b 
    WHERE parent = b.name AND child = a.name ORDER BY b.height DESC;

-- Sentences about siblings that are the same size
create table sentences as
  WITH sibling AS (
    SELECT parent, child, size FROM parents, size_of_dogs
    WHERE child = name
    )
    SELECT a.child || " and " || b.child || " are " || a.size || " siblings"
    FROM sibling as a, sibling as b
    WHERE a.parent = b.parent AND a.size = b.size AND a.child < b.child;

-- Heights and names of dogs that are above average in height among
-- dogs whose height has the same first digit.
create table above_average as
  WITH avgs AS (
    WITH digits AS ( 
      SELECT name, height, (height / 10) AS dig FROM dogs
    ) SELECT avg(height) AS avg FROM digits GROUP BY dig
  ) SELECT height, name FROM dogs, avgs
  WHERE (height / 10) = cast(avg / 10 AS INT) AND height > avg;


-------------------------------------------------------------
                                     -- EUCLID CAFE TYCOON --
-------------------------------------------------------------

-- Locations of each cafe
create table cafes as
  select "nefeli" as name, 2 as location union
  select "brewed"        , 8             union
  select "hummingbird"   , 6;

-- Menu items at each cafe
create table menus as
  select "nefeli" as cafe, "espresso" as item union
  select "nefeli"        , "bagels"           union
  select "brewed"        , "coffee"           union
  select "brewed"        , "bagels"           union
  select "brewed"        , "muffins"          union
  select "hummingbird"   , "muffins"          union
  select "hummingbird"   , "eggs";

-- All locations on the block
create table locations as
  select 1 as n union
  select 2      union
  select 3      union
  select 4      union
  select 5      union
  select 6      union
  select 7      union
  select 8      union
  select 9      union
  select 10;

-------------------------------------------------------------
   -- PLEASE DO NOT CHANGE ANY CAFE TABLES ABOVE THIS LINE --
-------------------------------------------------------------

-- Locations without a cafe
create table open_locations as
  select n FROM locations, cafes 
  GROUP BY n HAVING MIN(ABS(n - location) > 0);

-- Items that could be placed on a menu at an open location
create table allowed as
  WITH item_locations(item, location) AS (
    SELECT item, location FROM cafes, menus WHERE name = cafe
  )
    SELECT b.n as n, a.item as item FROM item_locations AS a, locations AS b
    GROUP BY b.n, a.item 
    HAVING MIN(ABS(b.n - a.location) > 2);
