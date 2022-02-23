from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import csv
import time
import threading

# Environmental Paths
WEBDRIVER = "C:/Seleium/chromedriver_win32/chromedriver.exe"
CSVPATH = "C:\Seleium\Data\Aviator.csv"

# Webdriver Options
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = webdriver.Chrome(executable_path=WEBDRIVER)
driver.set_page_load_timeout(120)
# driver.maximize_window()
driver.get("https://casino.bet9ja.com/casino/category/new")
driver.implicitly_wait(30)
winHandleBefore = driver.window_handles[0]

# Data
data_date = [0]
data_players = [0]
data_odd = [0]
odd_per_sec = ['null']
game_status = 'running'
headers = ['Date', 'Players', 'Odd', 'Odd_Per_Sec']


class DataModel:
    def __init__(self, no_of_players, final_odd, odds_per_sec):
        self.Date = str(datetime.datetime.now())
        self.Players = no_of_players
        self.Odd = final_odd
        self.Odd_Per_sec = odds_per_sec


#   Exports
dataCount = 5000
first_count = 1


# Utilities
def sleep(seconds):
    time.sleep(seconds)


def enter_key():
    action = ActionChains(driver)
    action.send_keys(Keys.ENTER).perform()


def hover(element):
    action = ActionChains(driver)
    action.move_to_element(element)


def wait_find_iframe(by, value):
    return WebDriverWait(driver, 30).until(EC.frame_to_be_available_and_switch_to_it((by, value)))


def wait_find_element(value):
    return WebDriverWait(driver, 120,
                         ignored_exceptions=(NoSuchElementException, StaleElementReferenceException)).until(
        EC.presence_of_element_located((By.XPATH, value)))


def write_into_db(value):
    with open(CSVPATH, "a", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(value)


def get_final_odd():
    print('Thread 2 is running ')
    try:
        global first_count
        global game_status
        global odd_per_sec
        while first_count < dataCount:
            if wait_find_element("//div[contains(text(), 'FLEW AWAY')]"):
                players = wait_find_element("//div[@class='total-bets']/span[3]")
                odd = wait_find_element("//*[contains(@class,'flew-coefficient')]")
                game_status = "running"
                if players.text != data_players[-1] and odd.text != data_odd[-1]:
                    data_players.append(players.text)
                    data_odd.append(odd.text)
                    print(list(DataModel(players.text, odd.text, ','.join(odd_per_sec)).__dict__.values()))
                    write_into_db(list(DataModel(players.text, odd.text, ','.join(odd_per_sec)).__dict__.values()))
                    odd_per_sec.clear()
                    odd_per_sec.append('null')
                    first_count += 1
                else:
                    sleep(3)
    finally:
        print("Time to go")
        game_status = "finished"
        sleep(10)
        driver.close()


def get_odd_per_seconds():
    print('Thread 1 is running ')
    global game_status
    while game_status == 'running':
        if odd_per_sec[-1] != wait_find_element("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div/app-payout-coefficient/div").text:
            odd_per_sec.append(wait_find_element("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div/app-payout-coefficient/div").text)
            print(wait_find_element("/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[2]/app-play-board/div/div[2]/app-dom-container/div/div/app-payout-coefficient/div").text)


# Credentials
userName = 'folarin4live'
password = 'oladi5top'
game = 'aviato'

# Sore data in databsee

scrap_group_name = str(datetime.datetime.now())
path_to_csv = "C:/Selenium/Data/{}.csv".format(scrap_group_name)

wait_find_element("//input[@name='username']").send_keys(userName)
driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
enter_key()
driver.implicitly_wait(5)
driver.find_element(By.CLASS_NAME, 'search__input').send_keys(game)
sleep(2)
driver.find_element(By.CLASS_NAME, 'search__input').send_keys("r")
sleep(2)
driver.implicitly_wait(5)
aviator = wait_find_element("//*[@id='2301001']/div")
sleep(10)
driver.implicitly_wait(5)
aviator.click()
wait_find_element("//button[@title='Play Now']").click()

sleep(10)
winHandleAfter = driver.window_handles[1]
driver.switch_to.window(driver.window_handles[1])


# Multiprocessing
if __name__ == '__main__':
    # t1 = threading.Thread(target=get_odd_per_seconds())
    t2 = threading.Thread(target=get_final_odd())
    # t1.join()
    t2.join()
    print('success')


