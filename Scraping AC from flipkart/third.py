import requests
from bs4 import BeautifulSoup
#from bs4 import BeautifulSoup as BSHTML
#packages to connect to db and add/remove/update data
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


#connecting to the db with default values and table created
db = MySQLdb.connect(host="localhost", user='root', passwd='', db='mobile')
#cursor to read the query results
cur = db.cursor()
#this is the format of forming and executing queries using mySQLdb , see documentation in 'readme' file for further knowledge
query="select urls,status from ac_details"
#executing query with the cursor
cur.execute(query)
a=cur.fetchall()
passvar = 1
#creating price column once
#cur.execute("ALTER table ac_details ADD price text")
#db.commit()

for row in a:
    print("AC",passvar,"\n")
    passvar=passvar+1
    #URLs being stored in the first column of the table is being fetched
    link=row[0]
    #stautus =1/0 , where flag 1 means it has been crawled for data and 0 flag means its yet to be checked;Default value in DB is 0
    status=row[1] 
    print("\nlink=%s\nstatus=%s\n"%(link,status))
    #creating arrays
    column_name = []
     #displaying the already present columns in the table
    cur.execute("SHOW COLUMNS FROM ac_details")
    b=cur.fetchall()
    for row in b:
        column_name.append(row[0])
    phone = requests.get(link).content
    soup = BeautifulSoup(phone,'html.parser')
    #link1 = soup.find("img",{"class","_1Nyybr Yun65Y"})
    #print("link========================>",link1['src'])
    price=soup.find("div",{"class":"_1vC4OE _3qQ9m1"})
    price=price.text
    if price==None:
        pass
    else:
        print(price)
    cur.execute("UPDATE ac_details SET price='%s' where urls='%s' "%(price,link))
    db.commit()
    link2 = soup.findAll("div",{"class":"_2_AcLJ"})
    x=1
    '''for a in link2:
        string=str(x)
        x=x+1
        column = 'image' + string
        src=a['style']
        src=src.strip()
        src=src.replace("background-image:url(","")
        src=src.replace(")","")
        src=src.replace("128","500")
        src=src.replace("70","100")
        print(column,"======================>",src)
        if column in column_name:
            pass
        else:
            cur.execute("ALTER table ac_details ADD %s text"%(column))
            db.commit()
        cur.execute("UPDATE ac_details SET %s='%s' where urls='%s' "%(column,src,link))
        db.commit()'''
    print("\n")
db.close()            
    
    

