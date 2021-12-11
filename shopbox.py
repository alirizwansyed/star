from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys
import csv
from datetime import datetime
import os 

URL='https://www.amazon.in/dp/B08V99QQ47'
driverpath = r"C:\ProgramData\Chrome_driver_84\chromedriver.exe"
chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_experimental_option('useAutomationExtension', True) 
driver = webdriver.Chrome(executable_path=driverpath,chrome_options=chromeOptions)
driver.get(URL)
driver.maximize_window()
pg_src=driver.page_source
driver.close()
sold_by_start=pg_src.find('Sold by')
end=pg_src.find('.',sold_by_start)
content=pg_src[sold_by_start:end]
if ('star enterprise services' in content.lower()):
  pass
else:
  ### Code to insert notification email
