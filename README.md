# GTU-result-web-scraping
- This is python web scraping project which is used to fetch GTU results of any range of students.
- You just have to pass some arguments in terminal and good to go.
- I make as possible as convient to use and as easy to understand.

# Requirement 
- You have to download Chrome, FireFox Driver and just change address of driver in WebScraping.py
- Install pip install -r requirement.txt
- Install Tesseract OCR - To Identify Captcha code.

# What i have done and used ?
- I have used python web scraping concepts, database concepts to store results of range of students.
- Used tesseract, Image library and ByteIO to get location of captcha code, store it then after preprocessing to remove line in center applying tesseract to get text.
- Used Libraries : Selenium, Beautifulsoup, Tesseract, BytesIO and some other useful. 

# How you can use this for your GTU results?
- First download Chrome of firefox driver and change loaction in WebScraping.py
- then change your result link name in field.
- then run following code in terminal after installing requirement.txt
- python3 WebScraping.py 180170107000 156 i temp
- structure : python3 WebScraping.py -starting range enrollment -till how many enrollments -i for Insert or u for Update -Name of database
