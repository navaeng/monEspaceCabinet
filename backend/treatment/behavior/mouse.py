import random

from selenium.webdriver.common.action_chains import ActionChains


def human_mouse_move(driver):
    try:
        actions = ActionChains(driver)
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)
        actions.move_by_offset(x, y).perform()
    except:
        pass
