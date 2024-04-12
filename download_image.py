import os
import time
from datetime import date
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import requests



class AmazonProductScraper:

    driver = None

    def __init__(self, parent = None):

        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--log-level=OFF')
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])

        url = input("Input URL: ")
        folder_name = input("Input Folder name to save images: ")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=opt)
        self.driver.get(url)
        time.sleep(3)
        self.scroll_to_bottom()
        time.sleep(3)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        images = soup.find_all('img')
        for i in range(0, len(images)):
            img_src = images[i].get('src')
            self.download_image(folder_name, '{}'.format(i+1), img_src)
        

    def scroll_to_bottom(self):
        scroll_pause_time = 1 
        screen_height = self.driver.execute_script("return window.screen.height;")   
        i = 1
        while True:
            self.driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            time.sleep(scroll_pause_time)
            scroll_height = self.driver.execute_script("return document.body.scrollHeight;")  
            if (screen_height) * i > scroll_height:
                break 



    def download_image(self, folder_name, image_name, image_link):
            if not os.path.isdir(folder_name):
                os.makedirs(folder_name)
            try:
                r = requests.get(image_link).content
                try:

                    # possibility of decode
                    r = str(r, 'utf-8')

                except UnicodeDecodeError:

                    # After checking above condition, Image Download start
                    with open("{}/{}.jpg".format(folder_name, image_name), "wb+") as f:
                        f.write(r)
            except:
                pass

if __name__ == "__main__":
    
    # app = QApplication(sys.argv)
    # win = AmazonProductScraper()
    # win.show()
    # sys.exit(app.exec())

    AmazonProductScraper()