#create database Inventory;
USE Inventory;
drop table if exists Make, Note, Sold, Stock, Product, Manufacturer;

create table Product(pid int, pname varchar(255) default'Product_name', cost int default 0, price int default 0, primary key (pid), check (cost >= 0 and price >= 0) );
create table Manufacturer(mid int, mname varchar(255) not null, primary key (mid));
create table Make(mid int, pid int default 0, foreign key (pid) references Product(pid), foreign key (mid) references Manufacturer(mid)) ;
create table Note(pid int, note varchar(255), primary key(pid), foreign key (pid) references Product(pid));
create table Sold(pid int, amt int default 0, primary key (pid), foreign key (pid) references Product(pid));
create table Stock(pid int, amt int default 0, primary key (pid), foreign key (pid) references Product(pid));

insert into Product values (1, 'iPhone 11 64g Yellow', 500, 699);
insert into Product values (2, 'iPhone 11 64g Purple', 500, 699);
insert into Product values (3, 'iPhone 11 64g White', 500, 699);
insert into Product values (4, 'Apple Juice', 0.5, 2.99);
insert into Product values (5, 'Apple Pie', 0.2, 1.99);
insert into Product values (6, 'Clark University Mug Cup', 3, 12.99);

insert into Manufacturer values (1, 'Apple Inc.');
insert into Manufacturer values (2, 'My Farm');
insert into Manufacturer values (3, 'Clark University');

insert into Make values (1, 1);
insert into Make values (1, 2);
insert into Make values (1, 3);
insert into Make values (2, 4);
insert into Make values (2, 5);
insert into Make values (3, 6);

insert into Stock values (1, 8);
insert into Stock values (2, 10);
insert into Stock values (3, 10);
insert into Stock values (4, 100);
insert into Stock values (5, 0);
insert into Stock values (6, 10);

insert into Sold values (1, 2);
insert into Sold values (4, 36);
insert into Sold values (6, 2);

insert into Note values (1, 'No discount.');
