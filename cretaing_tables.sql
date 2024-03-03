create table files_details(
	id int PRIMARY KEY,
	name varchar(30),
	Type varchar(30),
	size bigint,
	create_time timestamp,
	modified_time timestamp,
	Path varchar(100)
);

create table files_count(
    id int Primary Key,
    count int
);