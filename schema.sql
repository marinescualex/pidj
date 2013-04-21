drop table if exists files;
drop table if exists votes;
create table files (
  id integer primary key autoincrement,
  title text not null,
  path text not null
);
create table votes (
  id integer primary key autoincrement,
  file_id integer not null,
  ip text not null
);