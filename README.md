## Prerequisites
- Python 3
- Flask
- Flask-CORS
- Flask-MySQLdb
- PyTorch
- Numpy
- Sklearn
- MySQL 

## System Setup
1. Checkout our master branch by running 
```
git clone https://github.com/Dongaiqing/CS510-Literature-Search-Engine.git
```
2. Change your current folder to ·search_engine/·
3. Run `create_schema.sql` to create needed database schema. A sample command to run the SQL script is:
```
mysql -u <username> -p<password> < create_schema.sql
```
4. Put your MySQL database credential in `searchengine/__init__.py` by changing the these three configs:
```python
app.config['MYSQL_HOST']
app.config['MYSQL_USER']
app.config['MYSQL_PASSWORD']
```
5. Run `python3 run.py` to start the flask server and run the system
6. Visit http://127.0.0.1:5000 to access the website

## Usage
- Log in to the system by entering an arbitrary user name at the top right corner and hitting enter
- Perform the search by entering the query and hitting enter
- Click on any result link to view the paper’s original PDF file, click the “x” button on the top left corner to return to search results
- Click on the up/down arrow at the left side of a result to select the corresponding paper as relevant/irrelevant to the query

## Caveats
- Please log in before performing any search or no results will appear
- Due to limited amount of training data we only support up to 20 users at this time. If there are already 20 users in the database, you will not be able to add more new users.

