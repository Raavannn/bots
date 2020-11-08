import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep


class Insta :
    def __init__(self, path) :
        self.element = None
        self.path = path
        self.browser = None
        self.password = None
        self.ID = None

    ### Starting Script
    def start(self) :
        self.open_browser()
        self.open_insta()
        self.login_insta()
        self.open_inbox()

    #### Start Browser
    def open_browser(self) :
        try :
            self.browser = webdriver.Chrome(self.path)
            self.browser.maximize_window()
        except Exception as e :
            print("Exception Occured, please mention the correct path of webdriver, {}\nExiting now".format(e))
            raise SystemExit

    #### Open www.instagram.com
    def open_insta(self) :
        url = "https://www.instagram.com/"
        try :
            self.browser.get(url)
        except Exception as e :
            print("Unable to open the page got error\n{}\nExiting Now..".format(e))
            raise SystemExit

    ### Checking whether element is present or not
    def Wait(self, method, body, time=10, info='') :
        try :
            wait = WebDriverWait(self.browser, time).until(EC.presence_of_element_located((method, body)))
        except Exception as w :
            if info is True :
                print("Failed to find element {0}, waited for 10 seconds. Got below Error\n{1}".format(body, w))
                self.browser.quit()
                raise SystemExit
            return False
        else :
            return wait

    ### Clearing Text Field, in case of Wrong ID & password
    def clear_field(self, method, body) :
        self.Wait(method, body, info=False).send_keys(Keys.CONTROL+"a", Keys.DELETE)

    ### Checking whether user has logged
    def check_login(self) :
        if self.Wait("xpath", "//button[text()='Not Now']", time=4, info=False) is False :
            # Log In Failed
            print("Not Logged In\n{}".format(self.Wait("id", "slfErrorAlert", info=False).text))
            if raw_input("Do you wish to retry? (y/n): ") == "y" :
                self.clear_field("name", "username")
                self.clear_field("name", "password")
                self.login_insta()
            else :
                self.browser.quit()
                raise SystemExit

    ### Logging on Insta
    def login_insta(self) :
        User = self.Wait("name", "username", info=True)
        Pass = self.Wait("name", "password", info=True)
        self.ID = raw_input("User ID: ")
        User.send_keys(self.ID)
        self.password = getpass.getpass(prompt="Password: ", stream=None)
        Pass.send_keys(self.password)
        enter = self.Wait(By.XPATH, "//button[@type='submit']", info=False)
        enter.click()
        self.check_login()
        try:
            for i in xrange(2) :
                info = self.Wait("xpath", "//button[text()='Not Now']")
                info.click()
        except Exception as i:
            print("\nUnable to locate element, can be ignored.")

    ### Logging Out from Insta
    def logout(self, quit=False) :
        open_profile = self.browser.get("https://www.instagram.com/{}".format(self.ID))
        discovery = self.Wait("xpath", "//a[@href='/accounts/edit/']")
        sleep(1.5)
        options = self.Wait(By.CSS_SELECTOR, "svg", info=False)
        options.click()
        log_out = self.Wait(By.XPATH, "//button[text()='Log Out']", info=False)
        log_out.click()
        print("\nLogging Out, Please wait....")
        discover = self.Wait("name", "username", time=15, info=True)
        if quit is False :
            print("Now we Will re-log in on insta\n")
            self.login_insta()
        else :
            self.browser.quit()

    ### Opening Insta
    def open_inbox(self) :
        inbox = self.Wait("xpath", "//input[@placeholder='Search']", info=True)
        To = raw_input("\nEnter the Insta ID: ")
        inbox.send_keys(To)
        inbox = self.Wait("xpath", "//span[text()=\'{}\']".format(To), info=True)
        inbox.click()
        msg = self.Wait("xpath", "//button[text()='Message']")
        msg.click()
        self.type_message()

    ### Typing Message
    def type_message(self) :
        text = self.Wait("xpath", "//textarea[@placeholder='Message...']", info=True)
        text.send_keys(raw_input("\nEnter the message which is to be sent to this user: "))

        """Comment next two line, for testing purpose, as it will not hit the send button in Inbox"""
        # send = self.Wait("xpath", "//button[text()='Send']")
        # send.click()
        self.now_what()

    ### After sending Message
    def now_what(self) :
        feedback = raw_input("\nType 'Y' to send more message to same friend\
                                 \nType 'N' to send message to a New Friend\
                                 \nType 'LO' to logout & Quit\
                                 \nType 'LI' to log out and log in with new/same Insta ID\
                                 \nType 'Q' to directly quit without logging out\
                                 \nthe input is case-sensitive: ")
        if feedback == "Y" :
            self.type_message()
        elif feedback == "N" :
            self.open_inbox()
        elif feedback == "LO" :
            self.logout(quit=True)
        elif feedback == "LI" :
            self.logout(quit=False)
        else :
            self.browser.quit()
            raise SystemExit


if __name__ == '__main__' :
    path = '/home/vishal.k/Desktop/chromedriver'
    bot = Insta(path)
    bot.start()
