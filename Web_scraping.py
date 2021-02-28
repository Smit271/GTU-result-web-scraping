# Importing Useful libraries
from selenium import webdriver
from PIL import Image
import pytesseract
from io import BytesIO
import cv2
import numpy as np
import time
from bs4 import BeautifulSoup as Soup
import sqlite3

# Method to store data in local database
def store_in_db(database_path, enrollment, name, CPI, SPI, current_block, Total_back):
    conn = sqlite3.connect(database_path)

    c = conn.cursor()

    # creating table if not exist
    c.execute('''CREATE TABLE IF NOT EXISTS results (enrollment real, name text,
               CPI real, SPI real, Current_Backlog real, Total Backlog real)''')

    # Insert a row of data
    insert_query = f"INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)"
    c.execute(insert_query, (enrollment, name, CPI, SPI, current_block, Total_back))

    conn.commit()
    conn.close()

# Method To take screenshot of captcha code box for further processing
def screenshot():
    element = driver.find_element_by_id('imgCaptcha')  # find part of the page you want image of
    location = element.location
    size = element.size
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page

    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    im = im.crop((left, top, right, bottom))  # defines crop points
    #im.save('captcha/{}.png'.format((enrollment + no)))  # saves new cropped image
    #im = Image.open('captcha/{}.png'.format((enrollment + no)))  # opening image into memory
    return im

# img = cv2.imread('{}.png'.format(enrollment[0]), 0)

# Method for converting image into thresholding image
def binirize(image_to_transform, threshold):
    image = image_to_transform.convert("L")
    w = image.width
    h = image.height
    for x in range(w):
        for y in range(h):
            if image.getpixel((x, y)) < threshold:
                image.putpixel((x, y), 0)
            else:
                image.putpixel((x, y), 255)
    return image

# Method for removing horizontal line from Captcha of thresholded image and applying OCR
def text_captcha(captcha_image):
    new_size = (captcha_image.width * 3, captcha_image.height * 3)
    bigcaptcha = captcha_image.resize(new_size)
    img = binirize(bigcaptcha, 150)
    w = img.width
    h = img.height
    # remove black line from captcha(which lie on pixel 52 to 58 in vertical direction)
    for y in range(67, 72):
        for x in range(0, w):
            if img.getpixel((x, y - 1)) < 100:
                continue
            img.putpixel((x, y), 255)
    # display(img)
    return pytesseract.image_to_string(img)

# Chrome Driver for selenium
driver = webdriver.Chrome("/home/smit/Downloads/chromedriver_linux64/chromedriver")
# Accessing gtu result web site
driver.get("https://www.gturesults.in/Default.aspx?ext=archive")

# Entering BE Sem-4 Regular batch
batch = driver.find_element_by_id('ddlbatch')
batch.send_keys('.....BE SEM 4 - Regular (MAY 2020)')
with open("data.csv", 'w') as f:
    f.write("Enrollment, Name, CPI, SPI\n")
# defining enrollment range
enrollment  = 180170107000
# {no} represents total number of students
no = 81
# count for invalid captcha code trials
count = 0

# Extract data of all students untill enrollment reaches to 00
while (no > 0):
    # Find enrollment box by its attribute id
    enroll = driver.find_element_by_id('txtenroll')
    # clear if any previous value is in the box
    enroll.clear()
    enroll.send_keys(str(enrollment + no))

    im = screenshot()
    text = text_captcha(im)
    #print(text)
    # entering captcha into box and hit search
    capEnter = driver.find_element_by_id('CodeNumberTextBox')
    #clear if any previous value is in the box
    capEnter.clear()
    # sleep for 2 second
    time.sleep(2)

    capEnter.send_keys(text)
    search = driver.find_element_by_id('btnSearch')
    #search.click()

    # store html in content
    content = driver.page_source
    soup = Soup(content, 'html5lib')
    #Extracting msg process status
    msg = soup.find('span', attrs={'id': 'lblmsg'}).text.strip()
    # If data of student is not available then skip to next enrollment
    if msg == "Oppssss! Data not available.":
        print('Data is not available for Enrollment no:', (enrollment + no))
        no = no - 1
        continue
    # if captcha is wrong then it will run same loop and increase count of wronged attempts
    elif msg == "ERROR: Incorrect captcha code, try again.":
        count += 1
        print(f"Incorrect captcha code count {count}")
        continue
    time.sleep(1)
    name = soup.find('span', attrs={'id': 'lblName'}).text.strip()
    #print(f"Name : {name}")
    current_block = soup.find('span', attrs={'id': 'lblCUPBack'}).text
    #print(f"Current Backlog : {current_block}")
    Total_back = soup.find('span', attrs={'id': 'lblTotalBack'}).text
    #print(f"Total Backlog : {Total_back}")
    SPI = soup.find('span', attrs={'id': 'lblSPI'}).text
    #print(f"SPI : {SPI}")
    CPI = soup.find('span', attrs={'id': 'lblCPI'}).text
    #print(f"CPI : {CPI}")

    #with open("data.csv", 'a') as f:
        #f.write(f"{(enrollment+no)}, {name}, {CPI}, {SPI}\n")
    store_in_db("data.db", enrollment + no, name, CPI, SPI, current_block, Total_back)

    no = no - 1
# Closing driver automatically
driver.close()