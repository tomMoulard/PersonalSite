
drop database StuInfoManager_db
go

create database StuInfoManager_db
go

use StuInfoManager_db
go

/*==============================================================*/
/* Table: t_dean                                                  */
/*==============================================================*/
create table t_dean (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   dean_id              int                  not null,--Dean number, unique identify a dean
   name                 varchar(50)          not null,--Name
   responsibility       text                 null,--Duty description
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_department                                            */
/*==============================================================*/
create table t_department (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   dea_id int not null references t_dean(id),--Dean number, quote t_dean table
   department_id        int                  not null,--Faculty number, unique identify a faculty
   name                 varchar(50)          not null,--Faculty name
   description          text                 null,--Description
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted 
)
go

/*==============================================================*/
/* Table: t_class                                                 */
/*==============================================================*/
create table t_class (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   dep_id int not null references t_department(id),--Faculty number, quote t_department table
   class_id             int                  not null,--Class number, unique identify a class
   name                 varchar(50)          not null,--Class name
   description          text                 null,--Class description
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_student                                               */
/*==============================================================*/
create table t_student (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   cla_id int not null references t_class(id),--Class number, quote t_class table
   student_id           int                  not null,--Student number, unique identify a student
   name                 varchar(20)          not null,--Name
   gender               int                  not null,--Gender: 1-male, 2-female
   politics_status      int                  not null,--Politics status: 1-folks, 2-league member, 3-party member
   address              varchar(100)         null,--address
   birthday             varchar(50)          not null,--Date of birth
   tel                  varchar(20)          null,--Class name
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_course                                                */
/*==============================================================*/
create table t_course (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   course_id            int                  not null,--Course number, unique identify a course
   name                 varchar(20)          not null,--Course name
   credit               float(5)             not null,--Course credit
   period               int                  not null,--Course period
   type                 int                  not null,--Course type
   description          text                 null,--Course description
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_course_selecting                                    */
/*==============================================================*/
create table t_course_selecting (
   stu_id int not null references t_student(id),--Student number, quote t_student table
   cou_id int not null references t_course(id),--Course number, quote t_course table
   score                float(5)             null,--Score
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
   constraint "PK_COURSE-SELECTING" primary key (stu_id, cou_id),--Combined primary key
)
go

/*==============================================================*/
/* Table: t_teacher                                               */
/*==============================================================*/
create table t_teacher (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   teacher_id           int                  not null,--Teacher number, unique identify a teacher
   dep_id int not null references t_department(id),--Faculty number, quote t_department table
   name                 varchar(20)          not null,--Name
   gender               int                  not null,--Gender: 1-male, 2-female
   politics_status      int                  not null,--Politics status: 1-folks, 2-league member, 3-party member
   birthday             varchar(50)          not null,--Date of birth
   tel                  varchar(20)          null,--Telephone
   position             int                  not null,--Title: 1-primary, 2-middle, 3-vice-senior, 4-senior
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_teaching                                              */
/*==============================================================*/
create table t_teaching (
   tea_id int not null references t_teacher(id),--Teacher number, quote t_teacher table
   cla_id int not null references t_class(id),--Class number, quote t_class table
   cou_id int not null references t_course(id),--Course number, quote t_course table
   arrangement          varchar(50)          null,--The teaching schedule
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
   constraint PK_TEACHING primary key (tea_id, cla_id, cou_id),--Combined primary key
)
go

/*==============================================================*/
/* Table: t_test_question                                       */
/*==============================================================*/
create table t_test_question (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   cou_id int not null references t_course(id),--Course number, quote t_course table
   test_question_id   int                  not null,--Test question number, unique identify a test question
   type                 int                  not null,--Type: 0-single answer, 1-multiple choice answers, 2-Short answer questions
   itemContent          text                 not null,--Title
   analysis             text                 null,--Analysis
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_option                                              */
/*==============================================================*/
create table t_option (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   tes_id int not null references t_test_question(id),--Test question number, quote t_test_question table
   option_id            int                  not null,--Option number, unique identify a option
   num                  int                  not null,--Option: 0-represent A, 1-represent B, 2-represent C, 3-represent D
   optionContent        text                 not null,--Option content
   isTrue               int                  not null,--Identify whether the correct option: 1-yes, 2-not
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go

/*==============================================================*/
/* Table: t_user                                                */
/*==============================================================*/
create table t_user (
   id int not null identity(1, 1) primary key, --Auto-increase ID, a unique identifier, primary key
   name                 varchar(10)          not null,--Username
   password             varchar(20)          not null,--Password
   level                int                  not null,--role (level): 1-administrator, 2-teacher, 3-student
   del                  int                  not null,--Delete mark: 0-Deleted not,1-Deleted
)
go
