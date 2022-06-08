from bs4 import BeautifulSoup
from selenium import webdriver



#PATH = r'/usercode/chromedriver'
driver = webdriver.Edge(executable_path="D:\Development\Python\drivers\msedgedriver.exe")
driver.get("https://www.ornament-shop.com/star-wars-s129.html")
#h2 title
#span price-original

soup = BeautifulSoup(driver.page_source,'html.parser')
response = soup.find_all("article",class_ = "card")
data = []
ornaments = []
for item in response:
    data.append(item)
for item in data:
    #print(item)
    if item['data-name'].find('Storyteller')>0:
        continue
    else:
        ornaments.append(item['data-name'])
#desc = (first_ornament['data-name'])
#price = (first_ornament['data-product-price'])
print(ornaments)
#print (desc, price)

driver.quit()
