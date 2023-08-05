## (1) create table~s1

```sql
create or replace table sample_table (
	col1 number(18,0),
	col2 number(18,0)
);
```

## (2) insert into~s2

```sql
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
```

## (3) select data~s3

```sql
select * from sample_table;
```

## (4) select all~sample_table

```sql
select * from sample_table;
```

## (5) create table~s5

```sql
create or replace table any_other_table clone sample_table;
```

## (6) insert into~s6

```sql
insert into any_other_table (
  select
    a.*
    ,tmstmp.tmstmp as insert_tmstmp
  from sample_table a
  cross join (select current_timestamp() as tmstmp)tmstmp
);
```

## (7) drop table~s7

```sql
drop table if exists sample_table;
```
