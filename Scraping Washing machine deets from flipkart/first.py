#packages imported to help in scraping
import requests
from bs4 import BeautifulSoup
#packages to connect to db and add/remove/update data
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb


#specifying base url to access each page in the list of pages listing phones on flipkart
url = "https://www.flipkart.com/search?q=washing+machine&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page="
#connecting to the db with default values and table created
db = MySQLdb.connect("localhost","root","","mobile")
#cursor to read the query results
cur = db.cursor()
#base url to append specific mobile phone page links
base_url = "https://www.flipkart.com"
#creating url1[] array to store url's
url1=[0]*1000
#x here corresponds to the particular page in the search results eg if x=1,then it is appended to the "url" string to display the first page
x=1
#traversing x number of pages for retreiving all link in the x-th page
while x <= 42:
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
        query= "insert into washingmachine_details(urls) values('%s')"%(all_links)
        print(query)
        cur.execute(query)
        db.commit()
    x =x+1
db.close()












