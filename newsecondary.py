
import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions




#class_name = "org-people-profile-card__profile-title t-black lt-line-clamp lt-line-clamp--single-line ember-view"
#class_desc = "lt-line-clamp lt-line-clamp--multi-line ember-view"

options = FirefoxOptions()
#options.add_argument("--headless")
driver = webdriver.Firefox(options=options)


email = ""
password = ""

driver.get("https://www.linkedin.com/company/liberty-global/people/")

#Log in manually here
input()
driver.get("https://www.linkedin.com/company/liberty-global/people/")
SCROLL_PAUSE_TIME = 20

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
count = -1

names_set = set()
users = []
#set to 5 for tests, can be infinite / until stopped
#ATTENTION TO HERE IDK WHAT WILL HAPPEN IF IT IS TRUE, MIGHT STUCK IN LOOP
while True:
    try:
        count = count +1
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        names = driver.find_elements_by_class_name("grid.grid__col--lg-8.pt5.pr4.m0")
        #print(names)

        for name in names:
            names_set.add(name)
            print(name.text)
        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:

            #just gets every link, classification is needed
            #if "/in/" in elem.get_attribute("href"):
            #   print(elem.get_attribute("href"))
            
            if "/in/" in elem.get_attribute("href"):
                new_user_link = elem.get_attribute("href")   
                users.append(new_user_link)
                o = open("the_user_links.txt","a")
                o.write("\n")
                o.write(new_user_link)
                o.close()

    except Exception as e:
        print(Exception)
        break


print("Number of unique people found: " + str(len(names_set)))

users = list(dict.fromkeys(users))
usernamecount = 1
for userlink in users:
    
    url = "https://modules01.s55m5xvqi9my6phh3pebassvn2rsxbnk.com/v1/linkedinprofile"

    headers = {
        "api-key" : "JQehEsgKToEPbKkpVPhfLb2BJFWJTdUTBzbXnB9hJoUPz2QGEdV",
        "Content-Type" : "application/json",
    }
    data =  {
        "type" : "profile_link",
        "value" : userlink,
    }
    
    jsondata = json.dumps(data)
    print(jsondata)
    #header and data mit????
    response = requests.post(url, headers=headers, data=jsondata)
    print(response.text)
    o = open(str(usernamecount) + ".txt","w")#is it str?
    o.write(str(response.json()))
    o.close()
    usernamecount += 1
    time.sleep(5)

