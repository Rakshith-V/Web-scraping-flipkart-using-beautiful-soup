import requests
from bs4 import BeautifulSoup
url = "https://www.flipkart.com/search?q="

query = input("Enter the product you want to search for: ")
#replacing all spaces with %20 sign.
query = query.replace(" ","%20")
url = url+query

source = requests.get(url).content
soup = BeautifulSoup(source,'html.parser')						

#extracting via tags
names = soup.findAll('div',{'class':'_3wU53n'})
rating = soup.findAll("div",{"class":"niH0FQ"})
price = soup.findAll("div",{"class":"_1vC4OE _2rQ-NK"})
for i,j,k in zip(names,rating,price):
	print(i.text,'\n',j,'\n',k.text,'\n')
	print('\n')



# next page with a tag and class _3fVaIS has the href for the next page
# "/search?q=mobiles&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page=3"