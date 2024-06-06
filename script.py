from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
import pymongo
from datetime import datetime
import uuid

chrome_options = webdriver.ChromeOptions()
path  = "C:/Users/raush\Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(options=chrome_options,service=service)

driver.get("https://x.com/i/flow/login")

# x paths 
email_xpath = '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
nextbuttonforemail_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div'
username_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input'
nextbuttonforusername_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div'
password_xpath = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
login_xpath='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div'


# email entered
email_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, email_xpath))
)
email_element.send_keys("Enter_your_twitter_email")

#click next button after entering email 
emailnext_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, nextbuttonforemail_xpath))
)
emailnext_element.click()

# enter user name  ***************************
userinput_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, username_xpath))
)
userinput_element.send_keys("Enter_your_twitter_userid")

# usernamenext button  *******************
usernext_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, nextbuttonforusername_xpath))
)
usernext_element.click()

#enter password 
passwordinput_element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, password_xpath))
)
passwordinput_element.send_keys("Enter_your_twitter_password")

# click on login button
login_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, login_xpath))
)
login_element.click()

#logged in succcessfully 

heading_item = []

# whatshappening 
base_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[4]/div/section/div/div/div['

for i in range(4,8):
    # Construct the XPath for the current element
    current_xpath = base_xpath + str(i) + ']'
    try:
        # Wait until the element is present (optional, recommended)
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, current_xpath))
        )
        # Interact with the element (for example, print its text

        trendingheading_xpath = current_xpath+'/div/div/div/div[2]'
        headlines_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, trendingheading_xpath))
        )

        heading_item.append(headlines_element.text)

    except Exception as e:
        print(f"Element {i} not found: {e}")

#generating uniqueid get time and data
unique_id = str(uuid.uuid4())
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ip_address = driver.execute_script("return window.navigator.userAgent;")  # Not the actual IP, just an example

# Database setup 
print("connecting to MongoDB")
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")

db = client["Trending_Tweets"]
collection = db["dataitem"]

data = {
    "_id":unique_id,
    "nameoftrend1":heading_item[0],
    "nameoftrend2":heading_item[1],
    "nameoftrend3":heading_item[2],
    "nameoftrend4":heading_item[3],
    "timestamp":timestamp,
    "ip_address":ip_address
}
collection.insert_one(data)
print("Data Inserted")


time.sleep(20)
driver.quit()