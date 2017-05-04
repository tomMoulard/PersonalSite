if exists (select * from sysdatabases where name = 'TestLibrary') drop database TestLibrary

create database TestLibrary
go

use TestLibrary
go

/*==============================================================*/
/* Table: Table_Course                                 */
/*==============================================================*/
create table Table_Course(
   ID int not null identity(1, 1) primary key,     --Identity ID, Unique identification, Primary key
   CourseName varchar(32) not null,                --Course name
   CourseID varchar(32) not null,                  --Course number
   Del int not null check(Del in(0,1)) default 0,  --Deleting identification£º0-Not delete,1-Delete
)
go

/*==============================================================*/
/* Table: Table_TestType                                 */
/*==============================================================*/
create table Table_TestType (
   ID int not null identity(1, 1) primary key,		--Identity ID, Unique identification, Primary key
   TypeName varchar(16) not null,				--Test type
   Del int not null check(Del in(0,1)) default 0,	--Deleting identification£º0-Not delete,1-Delete
)
go

/*==============================================================*/
/* Table: Table_TestQuestion                                   */
/*==============================================================*/
create table Table_TestQuestion (
   ID int not null identity(1, 1) primary key,                --Identity ID, Unique identification, Primary key
   Course_ID int not null references Table_Course(ID),        --Course ID£¬The reference table is Table_Course
   Type_ID int not null references Table_TestType(ID),        --Test type ID£¬The reference table is Table_TestType
   Language int not null check(Language in(0,1)),             --Language: 0-Chinese, 1-English
   TestContent text not null,                                 --Question
   Difficulty int not null check(Difficulty between 0 and 2), --Difficulty: 0-Easy, 1-Medium, 2-Difficult
   Analysis text null,                                        --Test analysis
   Del int not null check(Del in(0,1)) default 0,             --Deleting identification£º0-Not delete,1-Delete
)
go

/*==============================================================*/
/* Table: Table_Option                                             */
/*==============================================================*/
create table Table_Option (
   ID int not null identity(1, 1) primary key,              --Identity ID, Unique identification, Primary key
   Test_ID int not null references Table_TestQuestion(ID),  --Test ID£¬The reference table is Table_TestQuestion
   Num int not null check(Num between 0 and 3),             --Option£º0-represent A, 1-represent B, 2-represent C£¬3-represent D
   OptionContent text not null,                             --Option content
   IsTrue int not null check(IsTrue in(0,1)),               --Correct identification: 0-True, 1-False
   Del int not null check(Del in(0,1)) default 0,           --Deleting identification£º0-Not delete,1-Delete
)
go
