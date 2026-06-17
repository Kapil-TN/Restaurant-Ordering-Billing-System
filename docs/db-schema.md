# Database Schema

User
----
id
name
email
password
role

Category
--------
id
name

MenuItem
--------
id
category_id
name
price

Table
-----
id
table_number

Order
-----
id
customer_id
table_id

OrderItem
---------
id
order_id

Bill
----
id
order_id
