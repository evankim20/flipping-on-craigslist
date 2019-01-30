import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import searchprice

zipcode = input("Enter zipcode: ")
while len(zipcode) != 5:
    print("Not a valid zipcode! Try again")
    zipcode = input("Enter zipcode: ")
    
radius = input("Enter radius: ")

# used for searching in NON free section
desired = set(['TV', 'monitor', 'xbox', 'playstation', 'ps4', 'camera',
    'bike', 'nintendo', 'lego', 'ink', 'toner',
    'cartridge', 'curb alert', 'new', 'unopened'])
blacklist = set(['entertainment center', 'box'])

redflags = set(['bundle'])

ignore = set(['free', 'large', 'big', 'great',  'free', 'small', 'new', ' -'  ])

#inititalizing selenium
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome('chromedriver') #, options = options)

#going to the craigslist website
driver.get('https://craigslist.org')
driver.find_element_by_xpath('//*[@id="sss1"]/li[2]/a').click()

#setting options for filter with radius and zipcode
driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[3]/input[1]').send_keys(radius)
driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[3]/input[2]').send_keys(zipcode)
driver.find_element_by_xpath('//*[@id="searchform"]/div[2]/div/div[7]/button').click()

#grabs items and links
item_links = dict()
#looks at all the postings on the page as they all has result-info class name
all_postings = driver.find_elements_by_class_name('result-info')
for post in all_postings:
    item = post.text
    splitted = item.split()
    title = ' '.join(splitted[2:])
    if any(flag1 in title.lower() for flag1 in desired) and not any(flag2 in title.lower() for flag2 in blacklist):
        pass
    else:
        continue
    #date using December setting year back once
    if splitted[0] == "Dec":
        postdate = splitted[0] + splitted[1] + str(datetime.today().year-1)
    else:
        postdate = splitted[0] + splitted[1] + str(datetime.today().year)
    dt_postdate = datetime.strptime(postdate, '%b%d%Y')
    days_avaliable = (datetime.today() - dt_postdate).days
    #checks if days available is within our asking range
    if days_avaliable > 2:
        break
    #setting days avaliable "weight"
    days_weight = .1/(days_avaliable+1)
    link = post.find_element_by_css_selector('a').get_attribute('href')
    item_links[title] = (link, days_weight)
driver.quit()
#if no results the dictionary becomes empty

item_price = []

for item_name in item_links:
    link = item_links[item_name][0]
    days_weight = item_links[item_name][1]
    product = item_name.split('(')[0][:-1]
    temp = product 
    for j in ignore:
        if j in temp.lower():
            temp = temp.lower().replace(j, '')
    print(temp) 
    #check myself for values
    if 'curb alert' in product.lower():
        item_price.append([product, link, None, None, None])
        continue
    appx_prices = searchprice.find_prices(product, zipcode)
    median = appx_prices[1]
    if median != 'N/A':
        weight = median*0.1 + days_weight
    else:
        weight = 'N/A'
    item_price.append([product, link] + appx_prices + [weight])

item_price = sorted(item_price, key=lambda x: (x[4] is None, x[4]))
item_to_df = [['Product', 'Link', '25th Percentile', 'Median', '75th Percentile', 'Weighted Score']] + item_price
df = pd.DataFrame(item_to_df)
df.columns = df.iloc[0]
df.drop(0, inplace = True)

df.to_csv('prices.csv', index = False)

print(item_price)
print("Complete! Found", len(item_price), "results.")





