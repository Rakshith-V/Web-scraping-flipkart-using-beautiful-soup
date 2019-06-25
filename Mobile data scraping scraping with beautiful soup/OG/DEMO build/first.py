#packages imported to help in scraping
import requests
from bs4 import BeautifulSoup
#packages to connect to db and add/remove/update data   
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


#specifying base url to access each page in the list of pages listing phones on flipkart
url = "https://www.flipkart.com/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page="
#connecting to the db with default values and table created
db = MySQLdb.connect("localhost","root","","mobile")
#cursor to read the query results
cur = db.cursor()
cur.execute("DROP TABLE IF EXISTS `demo_details`;")
cur.execute("CREATE TABLE `mobile`.`demo_details` ( `slno` INT(10) NOT NULL AUTO_INCREMENT , `urls` VARCHAR(500) NOT NULL , `status` INT(10) NOT NULL DEFAULT '0' , `price` TEXT NULL DEFAULT NULL , PRIMARY KEY (`slno`)) ENGINE = MyISAM;")
#base url to append specific mobile phone page links
base_url = "https://www.flipkart.com"
#creating url1[] array to store url's
url1=[0]*1000
#x here corresponds to the particular page in the search results eg if x=1,then it is appended to the "url" string to display the first page
x=1
#traversing x number of pages for retreiving all link in the x-th page
while x <= 85:
    query = str(x)
    #Concept used here is simple;The url has the base url of the flipkart mobile section with query having the page number appended in the end. Therefore, we get the display results of the x-th page
    url1[x] = url + query
    source = requests.get(url1[x]).content
    #cooking the soup/parsing html into DOM
    soup = BeautifulSoup(source,'html.parser')	

    #extracting via tags , a function present in "Beautiful soup" 
    links = soup.findAll("a",{"class":"_31qSD5"})
    #links contains all the links present contained in the <a> tag 
    for a in links:
        all_links = base_url+a.get('href')
        print("====links====",a.get('href'))
        phone = requests.get(all_links).content
        soup = BeautifulSoup(phone,'html.parser')
        #link1 = soup.find("img",{"class","_1Nyybr Yun65Y"})
        #print("link========================>",link1['src'])
        price=soup.find("div",{"class":"_1vC4OE _3qQ9m1"})
        if price==None:
            pass
        else:
            price=price.text
            print(price)
        query = "insert into demo_details(urls,price) values('%s','%s')"%(all_links,price)
        print(query)
        cur.execute(query)
        db.commit()
    x =x+1
db.close()
