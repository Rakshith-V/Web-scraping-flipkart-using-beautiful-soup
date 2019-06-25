#packages imported to help in scraping
import requests
from bs4 import BeautifulSoup
#packages to connect to db and add/remove/update data
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


#connecting to the db with default values and table created
db = MySQLdb.connect(host="localhost", user='root', passwd='', db='mobile')
#cursor to read the query results
cur = db.cursor()
#this is the format of forming and executing queries using mySQLdb , see documentation in 'readme' file for further knowledge
query="select urls,status from mobiles_details where status='0'"
#executing query with the cursor
cur.execute(query)
a=cur.fetchall()
for row in a:
    #URLs being stored in the first column of the table is being fetched
    link=row[0]
    #stautus =1/0 , where flag 1 means it has been crawled for data and 0 flag means its yet to be checked;Default value in DB is 0
    status=row[1] 
    print("\nlink=%s\nstatus=%s\n"%(link,status))
    #creating arrays
    column_name = []
    #displaying the already present columns in the table
    cur.execute("SHOW COLUMNS FROM mobiles_details")
    b=cur.fetchall()
    for row in b:
        column_name.append(row[0])
    #print(column_name)
    #obtaining each links and crawling specs only if status is 0
    if( status == 0):
        phone = requests.get(link).content
        soup = BeautifulSoup(phone,'html.parser')
        column = soup.findAll("td",{"class":"_3-wDH3 col col-3-12"})
        row = soup.findAll("li",{"class":"_3YhLQA"})
        for i,j in zip(column,row):
            #sanitizing 'column' and 'value' to remove special characters  
            column = i.text
            values = j.text
            #sanitizing column input values to remove un-necessary spaces and other charecters
            column = column.strip()
            column = column.rstrip()
            column = column.lstrip()
            values = values.strip()
            values = values.rstrip()
            values = values.lstrip()
            
            column = column.replace(" ","_")
            column = column.replace("-","_")
            column = column.replace("/","_")
            column = column.replace("'","")
            column = column.replace("(","")
            column = column.replace(")","")
            column = column.lower()

            #values.decode("utf-8")
            #values = values.replace(" ","_")
            #values = values.replace("/","_")
            '''values = values.replace("\\","_")
            values = values.replace("//","_")
            values = values.replace("\\\\","_")'''
            values = values.replace("'","")
            values = values.replace('"','')
            
            
            if column in column_name:
                pass
            else:
                cur.execute("ALTER table mobiles_details ADD %s text"%(column))
                db.commit()
            cur.execute("UPDATE mobiles_details SET %s='%s' where urls='%s' "%(column,values,link))
            db.commit()
            print(column,"================>",values)
            cur.execute("UPDATE mobiles_details SET status='1' where urls='%s' "%(link))
            db.commit()
            #set status=1 after working              
db.close()
