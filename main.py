import unittest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import string
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
jobids = []


def jobcloser():
    job = ""
    windows = driver.window_handles
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/span/pre/a[1]')))
    element = driver.find_element(By.XPATH, '/html/body/form/span/pre/a[1]')
    if "A" in element.text or "R" in element.text:
        element.click()
        wait.until(EC.new_window_is_opened(windows))
        windows = driver.window_handles
        driver.switch_to.window(windows[2])
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/span/pre/a')))
        element = driver.find_element(By.XPATH, '/html/body/form/span/pre/a')
        element.click()
        element = driver.find_element(By.XPATH, '/html/body/form/span/pre')
        starting_point = element.text.find("SCHEDULED") + 10
        iterable = 0
        while True:
            character = element.text[starting_point+iterable]
            if character in string.digits:
                iterable += 1
            else:
                jobidee = iterable + starting_point
                job = element.text[starting_point:jobidee]
                break
        driver.close()
        windows = driver.window_handles
        driver.switch_to.window(windows[0])



def main():
    driver.get("https://imds.cce.af.mil/imds/fs/fs000cams.html")
    windownames = driver.window_handles
    elem = driver.find_element(By.ID, "details-button")
    elem.send_keys(Keys.ENTER)
    elem = driver.find_element(By.ID, "proceed-link")
    elem.send_keys(Keys.ENTER)  # New page
    elem = driver.find_element(By.ID, "details-button")
    elem.send_keys(Keys.ENTER)
    elem = driver.find_element(By.ID, "proceed-link")
    elem.send_keys(Keys.ENTER)  # New page
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "button-small")))
    elem = driver.find_element(By.CLASS_NAME, "button-small")
    elem.send_keys(Keys.ENTER)
    elem = driver.find_element(By.NAME, "button")
    elem.send_keys(Keys.ENTER)  # New page
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//*[@id='mainframe']")))
    elem = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/input")
    elem.send_keys(TerminalID)
    elem = driver.find_element(By.XPATH, '//*[@id="TerminalLogon"]')
    elem.send_keys(Keys.ENTER)  # New Page
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div/iframe[3]')))
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/form/div/table[1]/tbody/tr[2]/td[3]/input[1]')))
    elem = driver.find_element(By.XPATH, '/html/body/div/form/div/table[1]/tbody/tr[2]/td[3]/input[1]')
    elem.click()
    elem.send_keys("380")
    elem = driver.find_element(By.XPATH, '//*[@id="div1"]/table[1]/tbody/tr[2]/td[3]/input[4]')
    elem.click()  # New page
    driver.switch_to.default_content()
    wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/iframe[2]')))
    elem = driver.find_element(By.XPATH, '/html/body/div[1]/form/table[4]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[1]')
    elem.send_keys(EquipID)
    elem = driver.find_element(By.XPATH, '/html/body/div[1]/form/table[4]/tbody/tr/td[1]/table/tbody/tr[2]/td[4]/input[1]')
    elem.send_keys("52NO")
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/input[41]')))
    elem = driver.find_element(By.XPATH, '/html/body/div[1]/form/input[41]')
    elem.click()
    driver.switch_to.default_content()
    wait.until(EC.new_window_is_opened(windownames))
    windownames = driver.window_handles
    driver.switch_to.window(windownames[1])
    wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "gagtext")))
    iterjobs = driver.find_elements(By.CLASS_NAME, "gagtext")
    jobcloser()
    print(windownames)
    print(iterjobs)
    input()


if __name__ == '__main__':
    TerminalID = 'M2LDAZ'
    FriendID = 'SACKEYAN'
    EquipID = 'C120T'
    main()
