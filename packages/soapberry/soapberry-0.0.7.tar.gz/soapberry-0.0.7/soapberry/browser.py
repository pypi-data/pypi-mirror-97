import soapberry.helpers
import soapberry.classes
import sys 
from datetime import datetime
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display

class browser:
    
    logs = []
    display = ""
    driver = ""
    wait_timeout = 30

    def create(self, page_load_timeout, wait_timeout, add_log = True):
        if not sys.platform == 'win32':
            self.add_and_print_log('Creating display', add_log)
            self.display = Display(visible=0, size=(1920, 768))
            self.display.start()

        self.add_and_print_log('Creating browser', add_log)
        self.driver = webdriver.Firefox()
        self.driver.set_page_load_timeout(page_load_timeout)
        self.wait_timeout = wait_timeout

    def close(self, add_log = True):
        if not sys.platform == 'win32':
            self.add_and_print_log('Closing display', add_log)
            self.display.stop()

        self.add_and_print_log('Closing browser', add_log)
        self.driver.close()

    def go_to(self, url, add_log = True):
        if (add_log):
            self.add_and_print_log('Loading url ' + url, add_log)
        try:
            self.driver.get(url)
        except:
            pass

    def find_element_and_click(self, by, identifier, add_log = True):
        element = self.find_element(by, identifier)
        if (add_log):
            self.add_and_print_log('Clicking on element ' + identifier, add_log)
        element.click()

    def find_element_and_settext(self, by, identifier, text, add_log = True):
        element = self.find_element(by, identifier)
        if (add_log):
            self.add_and_print_log('Setting text on element ' + identifier, add_log)
        element.send_keys(text)

    def find_element(self, by, identifier, add_log = True):
        self.wait_visible_element(by, identifier)
        return self.driver.find_element(by, identifier)

    def wait_visible_element(self, by, identifier, add_log = True):
        self.add_and_print_log('Waiting for element ' + identifier, add_log)
        WebDriverWait(self.driver, self.wait_timeout).until(EC.visibility_of_element_located((by, identifier)))

    def get_request(self, extension):
        foundUrl = ''
        for request in self.driver.requests:
            if request.response and extension in request.url:
                foundUrl = request.url
        if foundUrl:        
            return foundUrl
        raise Exception('No '+ extension +' file found')
    
    def add_and_print_log(self, message, add_log = True):
        if (add_log):
            log = classes.soapberry_log()
            log.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            log.message = message
            helpers.print_log(log)
            self.logs.append(log)