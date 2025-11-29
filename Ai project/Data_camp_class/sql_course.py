# Structured query langage (sql)

# keywords
# SELECT => we need this keyword for all the task we want to do (we can use DISTINCT when we want to select some value without any twins)
# FROM => to select the table where the informations we want is
# WHERE => to setup a condition in the selection of something (use multiple criteria with OR, AND, BETWEEN) (filter words with LIKE 'NOT LIKE' and IN) (IS NULL and IS NOT NULL), filter individual records
# LIMIT => to set a limit to the number of element we want from a field
# ORDER BY => to ordered results (DESC for descending order and ASC for ascending order)
# GROUP BY => to group values (all the fields select in the SELECT statement must appear in the GROUP BY statement execpt for aggregate funtions)
# HAVING => filter group records

# Comparaison operator
# > : greater than or after
# < : less than or before
# = : equal to
# <= : less or equal to
# >= : greater or equal to
# <> : not equal to

# Null values is missing values
# COUNT count the number of non null value for the field that we select even whitout the key word "IS NOT NULL"

# Aggregates functions: COUNT() SUM() AVG() MIN() MAX() ROUND()

# Order of the execution :
    # FROM
    # WHERE
    # SELECT
    # LIMIT


# JOIN query exemple
# SELECT 'field'
# FROM 'first table'
# INNER 'second table
# ON 'field we want to match the tables'
# alias can be used with FROM and INNER JOIN
# USING() for fiel who have the same name in both table

# LEFT JOIN join all the element between two table based on the left table and fill the element of the right table that the left table doesn't have by using null value
# RIGHT JOIN inverse of the right join
# FULL JOIN combine LEFT JOIN and RIGHT JOIN
# CROSS JOIN creates all possible combinaitions for two tables
# UNION or UNION ALL (return a table with double value as result of the union of the first two tables)
# INTERSECT work like INNER JOIN but have the same syntaxe than UNION
# EXCEPT return the elements present in one table but not the other 
# CASE statement: WHEN THEN ELSE END

# PostGre

# Relative
# LAG(Column, n) return Column's values at the row n before the current row
# LEAD(Column, n) return Column's values at  the row n after the current row

# Absolute
# FIRST_VALUE(Column) return the first value in the table or partition
# LAST_VALUE(Column) return the last value in the table or partition


# OLTP: Online Transaction Processing
# OLAP: Online Analytical Processing

top_level_domains = [
    ".org",
    ".net",
    ".edu",
    ".ac",
    ".gov",
    ".com",
    ".io"
]

def validate_email(email):
    if '@' in email:
        for i in top_level_domains:
            if i in email:
                print(i)
                return True
    else:
        return False
    return True

print(validate_email('test@.'))
