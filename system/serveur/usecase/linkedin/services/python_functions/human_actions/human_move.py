import random
import time

from selenium.webdriver.common.action_chains import ActionChains

def human_move(driver):
    action = ActionChains(driver)

    action.move_by_offset(random.randint(10, 100), random.randint(10, 100)).perform()
    time.sleep(random.uniform(0.5, 2.0))
