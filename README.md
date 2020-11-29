# InventoryManager
This application is designed as a lite inventory management solution for small retail business.
The main users are inventory managers who work for small business starters that have relatively low variety of products. 
Application runs on Python and MySQL, both dependencies are easy to install and configure.

Be very careful when taking raw input from user. Raw inputs usually include ‘\n’ (the new line character).
Be very careful when writing SQL strings. Most IDEs does not provide auto-corrections for SQL statements (because they are usually stored as strings in the main language).
The data type that function cursor.fetchall() returns is a 2D tuple. If nothing is returned by the database, it is a tuple with a length of zero.
The function mydbconn.commit() is the call that makes the changes happen, so use carefully.
