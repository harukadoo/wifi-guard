import time
from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

config = dotenv_values(".env")
    
class RouterBot: 
    def __init__(self):
        self.options = Options()
        # self.options.add_argument("--headless") 
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
    
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        print("Browser opened successfully")

    def _login(self):
        self.driver.get(config["ROUTER_URL"])
        time.sleep(5)

        try: 
            password_input = self.driver.find_element(By.ID, "login_password")
            password_input.clear()
            password_input.send_keys(config["ROUTER_PASSWORD"])

            login_btn = self.driver.find_element(By.ID, "login_save")
            login_btn.click()
            
            time.sleep(3)

        except Exception as e:
            print(f"Login error: {e}")
            raise e
        
    def set_wifi_state(self, turn_on=False):
        try:
            self._login()

            wifi_tab = self.driver.find_element(By.ID, "wifiAdvancedTitle_Fav")
            wifi_tab.click()
            time.sleep(5)

            try:
                self.driver.switch_to.frame("iframeapp")
                print("Switched to iframe successfully!")
            except Exception as e:
                print(f"Could not switch to frame! Error: {e}")
                return

            wifi_toggle_btn = self.driver.find_element(By.ID, "wifi_radio_all") 

            aria_status = wifi_toggle_btn.get_attribute("aria-pressed")
            
            print(f"button status: {aria_status}")

            is_wifi_on = (aria_status == "true")

            if turn_on != is_wifi_on:
                action = "ENABLING" if turn_on else "DISABLING"
                print(f"{action} Wi-Fi")

                wifi_toggle_btn.click()
                time.sleep(5)
                
            else:
                print(f"No changes needed")

        except Exception as e:
            print(f"wifi state error: {e}")

if __name__ == "__main__":
    bot = RouterBot()

    bot.set_wifi_state()
    time.sleep(100)