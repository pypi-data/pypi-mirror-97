/*: ---------------------------------------------------------------------------
  * This file was stripped of all comments and exported by snowmobile.

  * The tags above each statement either reflect a user-defined tag
    or a tag that was generated in the absence of one.

  * For more information see: https://github.com/GEM7318/snowmobile
--------------------------------------------------------------------------- :*/

/*-create table~s1-*/
create or replace table sample_table (
	col1 number(18,0),
	col2 number(18,0)
);

/*-insert into~s2-*/
insert into sample_table with
sample_data as (
  select
    uniform(1, 10, random(1)) as rand_int
  from table(generator(rowcount => 3)) v
)
  select
    row_number() over (order by a.rand_int) as col1
    ,(col1 * col1) as col2
  from sample_data a;

/*-select data~s3-*/
select * from sample_table;

/*-select all~sample_table-*/
select * from sample_table;

/*-create table~s5-*/
create or replace table any_other_table clone sample_table;

/*-insert into~s6-*/
insert into any_other_table (
  select
    a.*
    ,tmstmp.tmstmp as insert_tmstmp
  from sample_table a
  cross join (select current_timestamp() as tmstmp)tmstmp
);

/*-drop table~s7-*/
drop table if exists sample_table;
