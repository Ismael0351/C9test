'''
Auto login code to keep a c9 workspace up
@author Sercrash
@date 18/05/2016
'''
# Imports
import sys, time, threading, random, datetime, timeout, os.path
from random import randint
global ejecuciones
ejecuciones = 0

# Class definition
class KeepUp:

    def __init__(self): # Constructor
        self.version = "v1.0.1"
        self.author = "SerCrAsH"
        self.directory = "keepUp/"
        self.directory_img = self.directory + "img/"
        self.file_result_html = "login_result.html"
        self.file_log = "log.txt"
        
        # Create dir if not exist
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if not os.path.exists(self.directory_img):
            os.makedirs(self.directory_img)
        
        print "[KeepUp] Initialization - @" , self.author , " - Version KeepUp : " , self.version
        
    def __getattr__(self, var): # Gets
        return self.__dict__[var] if  var in self.__dict__ else "["+str(var)+"] var does not exist."
        
    def __str__(self): # To String
        pass
    
    ##### Methods #####
    # Main Method
    def loadTask(self, user="default" , password="default", target_workspace="https://ide.c9.io/user-default/workspace-default"):
        self.user = user
        self.password = password
        self.target_workspace = target_workspace
        self.load()
    
    # Load method
    def load(self):
        min_time = 3600 # 1 hour in seconds
        max_time = 7179 # 2 hours in seconds (less 21)
        tasktime = randint(min_time, max_time)
        global ejecuciones
        if ejecuciones<1:
            tasktime = 180
        if ejecuciones==1:
            tasktime=tasktime-180
        ejecuciones = 1
        threading.Timer(tasktime, self.load).start()
        print "[KeepUp] Load execution at ", time.ctime(), " waiting ", tasktime , "seconds for the next time."
        
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as ec
        from selenium.webdriver.common.keys import Keys
        from pyvirtualdisplay import Display
        
        # Initial
        display = Display(visible=0, size=(1600, 900))
        display.start()
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.cache.disk.enable", False)
        profile.set_preference("browser.cache.memory.enable", False)
        profile.set_preference("browser.cache.offline.enable", False)
        profile.set_preference("network.http.use-cache", False)
        driver = webdriver.Firefox()
        driver.get("https://c9.io/dashboard.html")
        driver.save_screenshot(self.directory_img + 'login.png')
        #Username
        username = driver.find_element_by_id("id-username")
        username.click()
        username.clear()
        username.send_keys(self.user, Keys.ARROW_DOWN)
        
        #Password
        password = driver.find_element_by_id("id-password")
        password.click()
        password.clear()
        password.send_keys(self.password, Keys.ARROW_DOWN)
        
        #Submit
        submit_button = driver.find_element_by_css_selector("button[type=submit]")
        # print submit_button.text
        
        # Click submition
        submit_button.click();
        time.sleep(5)
        driver.save_screenshot(self.directory_img + 'user_profile.png')
        # Target dir
        driver.get(self.target_workspace)
        time.sleep(10)
        
        self.log(driver.page_source) #make log
        driver.save_screenshot(self.directory_img + 'final_workspace.png')
        # End
        driver.quit()
        display.stop()

    # Log method
    def log(self, content = ""):
        log_html = self.directory + self.file_result_html
        log_file = self.directory + self.file_log
        f = open( log_html , 'w')
        f.write(content)
        f.close()
        f = open( log_file , 'a')
        f.write("[" + str(time.ctime()) + "] Log execution\n")
        f.close()
        print "[KeepUp] Log volcado"
            