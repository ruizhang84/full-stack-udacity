# Logs Analysis

## HOW TO
- Install the virtual machine.
- Navigate to the direcotyr /vagrant, use the command psql -d news -f newsdata.sql to load the data.
- Type in "python3 query.py" to show up the result.

## Q1: What are the most popular three articles of all time?
To answer this question, first select top 3 __path__ entries in __log__ table, and find
the corresponding __slug__ entry in __articles__ table.
Then group up these findings by the __title__ column (in __articles__ table), and count it.

## Q2: Who are the most popular article authors of all time?
To answer this question, simply inner join all three tables, and then count the authors name.

## Q3 On which days did more than 1% of requests lead to errors?
Count the number of the stauts that shows 404 errors versus all the status, and filter the ratio higher than 1%. 
The date format can be handled by to_char function and group by date_trunc function.
