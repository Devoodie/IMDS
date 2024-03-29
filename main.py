from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import sys
import json
import string
from datetime import datetime
import time
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
jobids = {}
jobsfailed = []
now = datetime.now()
nowdateandtime = now.strftime("%b-%d-%Y-%H-%M")


class Session:
    def __init__(self, name, jobsattempted, badjobs):
        self.sessionname = name
        self.goodjobs = jobsattempted
        self.notgoodjobs = badjobs
    def savejobs(self):
        with open(f'{self.sessionname}-jobs attempted', "w") as file:
            file.write(json.dumps(self.goodjobs))
        with open(f'{self.sessionname}-jobs failed', "w") as file:
            file.write(json.dumps(self.notgoodjobs))


def jobcloser(htmlele, tonumber="123456789123456789", *args, rapidfire=False, omit=None):
    windows = driver.window_handles
    wait.until(EC.element_to_be_clickable(htmlele))
    element = htmlele
    if "A" in element.text or "R" in element.text:
        element.click()
        wait.until(EC.new_window_is_opened(windows))
        windows = driver.window_handles
        driver.switch_to.window(windows[2])
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/form/span/pre/a')))
        element = driver.find_element(By.XPATH, '/html/body/form/span/pre')
        if tonumber in element.text:
            job = findtonumber(driver.find_element(By.XPATH, '/html/body/form/span/pre'))
            try:
                driver.find_element(By.XPATH, '/html/body/form/span/pre/a[2]')
                driver.close()
                windows = driver.window_handles
                driver.switch_to.window(windows[1])
                jobsfailed.append(tonumber)
                print(f'{tonumber} has a double link!')
                return "a"
            except NoSuchElementException:
                element = driver.find_element(By.XPATH, '/html/body/form/span/pre/a')
                element.click()
                driver.close()
                windows = driver.window_handles
                driver.switch_to.window(windows[0])
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/iframe[2]')))
                try:   # time start
                    driver.find_element(By.NAME, 'R7_C29_L4_N').is_displayed()
                    driver.find_element(By.NAME, 'R7_C29_L4_N').send_keys(Timestart)
                except NoSuchElementException:
                    wait.until(EC.element_to_be_clickable((By.NAME, 'R9_C33_L4_N')))
                    driver.find_element(By.NAME, 'R9_C33_L4_N').send_keys(Timestart)
                try:  # time end
                    driver.find_element(By.NAME, 'R9_C45_L4_N').send_keys(Timeend)
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R7_C42_L4_N').send_keys(Timeend)
                try:  # type maintenance # type maintenance
                    element = driver.find_element(By.NAME, 'R12_C18_L60_N')
                    elementval = element.get_property("value")
                    if "PRE-DEPLOYMENT INSPECTION" in elementval or "POST DEPLOYMENT INSPECTION" in elementval:
                        driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("S")
                    else:
                        driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("T")
                except NoSuchElementException:
                    pass
                driver.find_element(By.NAME, 'cs').send_keys("2")  # crew size
                try:  # units produced
                    driver.find_element(By.NAME, 'R7_C25_L2_N').send_keys("1")
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R9_C30_L2_N').send_keys("1")
                driver.find_element(By.NAME, 'cat').send_keys("1")  # category
                try:  # corrected by
                    if driver.find_element(By.NAME, 'R7_C62_L12_N').is_enabled():
                        driver.find_element(By.NAME, 'R7_C62_L12_N').send_keys(FriendID)
                except NoSuchElementException:
                    if driver.find_element(By.NAME, 'R9_C61_L12_N').is_enabled():
                        driver.find_element(By.NAME, 'R9_C61_L12_N').send_keys(FriendID)
                try:  # inspected by
                    driver.find_element(By.NAME, 'R19_C43_L12_N').send_keys(UserID)
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R9_C22_L12_N').send_keys(UserID)
                element = driver.find_element(By.NAME, 'CANarrativeTextarea')  # corrective action
                element.clear()
                element.send_keys(CorrectiveAction)
                try:
                    driver.find_element(By.NAME, 'rad1').click()
                except NoSuchElementException:
                    pass
                driver.find_element(By.NAME, "b1").click()
                driver.switch_to.default_content()
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/iframe[3]')))
                wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div/form/div/table[1]/tbody/tr[1]/td[1]')))
                time.sleep(3)
                element = driver.find_element(By.XPATH, '/html/body/div/form/div/table[1]/tbody/tr[1]/td[1]')
                print(element.text)
                if element.text != "" or element.text == "&nbsp":
                    pass
                else:
                    jobsfailed.append(job)
                    print(f'Job failed: {job}')
                    windows = driver.window_handles
                    driver.switch_to.window(windows[1])
                    return job
                driver.switch_to.default_content()
                try:  # see if error submitting
                    if len(jobsfailed) == 0:
                        driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        jobsfailed.append(job)
                        print(f'Job failed: {job}')
                        windows = driver.window_handles
                        driver.switch_to.window(windows[1])
                        return job
                    else:
                        driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        driver.find_element(element[len(jobsfailed)-1])
                        jobsfailed.append(job)
                        print(f'Job failed: {job}')
                        windows = driver.window_handles
                        driver.switch_to.window(windows[1])
                        return job
                except (NoSuchElementException, IndexError):
                    windows = driver.window_handles
                    driver.switch_to.window(windows[1])
                    return job
        elif rapidfire is True:
            if omit is not None:
                for TO in omit:
                    if f"-{TO}" in element.text:
                        print(f"TO omited: {TO}")
                        windows = driver.window_handles
                        driver.close()
                        driver.switch_to.window(windows[1])
                        return "a"
                    else:
                        job = findtonumber(element)
                        driver.close()
                        windows = driver.window_handles
                        driver.switch_to.window(windows[0])
                        wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/iframe[2]')))
                        try:  # time start
                            driver.find_element(By.NAME, 'R7_C29_L4_N').is_displayed()
                            driver.find_element(By.NAME, 'R7_C29_L4_N').send_keys(Timestart)
                        except NoSuchElementException:
                            wait.until(EC.element_to_be_clickable((By.NAME, 'R9_C33_L4_N')))
                            driver.find_element(By.NAME, 'R9_C33_L4_N').send_keys(Timestart)
                        try:  # time end
                            driver.find_element(By.NAME, 'R9_C45_L4_N').send_keys(Timeend)
                        except NoSuchElementException:
                            driver.find_element(By.NAME, 'R7_C42_L4_N').send_keys(Timeend)
                        try:  # type maintenance # type maintenance
                            element = driver.find_element(By.NAME, 'R12_C18_L60_N')
                            elementval = element.get_property("value")
                            if "PRE-DEPLOYMENT INSPECTION" in elementval or "POST DEPLOYMENT INSPECTION" in elementval:
                                driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("S")
                            else:
                                driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("T")
                        except NoSuchElementException:
                            pass
                        driver.find_element(By.NAME, 'cs').send_keys("2")  # crew size
                        try:  # units produced
                            driver.find_element(By.NAME, 'R7_C25_L2_N').send_keys("1")
                        except NoSuchElementException:
                            driver.find_element(By.NAME, 'R9_C30_L2_N').send_keys("1")
                        driver.find_element(By.NAME, 'cat').send_keys("1")  # category
                        try:  # corrected by
                            if driver.find_element(By.NAME, 'R7_C62_L12_N').is_enabled():
                                driver.find_element(By.NAME, 'R7_C62_L12_N').send_keys(FriendID)
                        except NoSuchElementException:
                            if driver.find_element(By.NAME, 'R9_C61_L12_N').is_enabled():
                                driver.find_element(By.NAME, 'R9_C61_L12_N').send_keys(FriendID)
                        try:  # inspected by
                            driver.find_element(By.NAME, 'R19_C43_L12_N').send_keys(UserID)
                        except NoSuchElementException:
                            driver.find_element(By.NAME, 'R9_C22_L12_N').send_keys(UserID)
                        element = driver.find_element(By.NAME, 'CANarrativeTextarea')  # corrective action
                        element.clear()
                        element.send_keys(CorrectiveAction)
                        try:
                            driver.find_element(By.NAME, 'rad1').click()
                        except NoSuchElementException:
                            pass
                        driver.switch_to.default_content()
                        try:  # see if error submitting
                            if len(jobsfailed) == 0:
                                driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                                element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                                jobsfailed.append(job)
                                print(f'Job failed: {job}')
                                windows = driver.window_handles
                                driver.switch_to.window(windows[1])
                                return job
                            else:
                                driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                                element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                                driver.find_element(element[len(jobsfailed) - 1])
                                jobsfailed.append(job)
                                print(f'Job failed: {job}')
                                windows = driver.window_handles
                                driver.switch_to.window(windows[1])
                                return job
                        except (NoSuchElementException, IndexError):
                            windows = driver.window_handles
                            driver.switch_to.window(windows[1])
                            return job
            else:
                if "STARTED" in element.text:
                    starting_point = element.text.find("STARTED") + 8
                else:
                    starting_point = element.text.find("SCHEDULED") + 10
                iterable = 0
                while True:
                    character = element.text[starting_point + iterable]
                    if character in string.digits:
                        iterable += 1
                    else:
                        jobidee = iterable + starting_point
                        job = element.text[starting_point:jobidee]
                        break
                driver.close()
                windows = driver.window_handles
                driver.switch_to.window(windows[0])
                wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[1]/iframe[2]')))
                try:  # time start
                    driver.find_element(By.NAME, 'R7_C29_L4_N').is_displayed()
                    driver.find_element(By.NAME, 'R7_C29_L4_N').send_keys(Timestart)
                except NoSuchElementException:
                    wait.until(EC.element_to_be_clickable((By.NAME, 'R9_C33_L4_N')))
                    driver.find_element(By.NAME, 'R9_C33_L4_N').send_keys(Timestart)
                try:  # time end
                    driver.find_element(By.NAME, 'R9_C45_L4_N').send_keys(Timeend)
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R7_C42_L4_N').send_keys(Timeend)
                try:  # type maintenance # type maintenance
                    element = driver.find_element(By.NAME, 'R12_C18_L60_N')
                    elementval = element.get_property("value")
                    if "PRE-DEPLOYMENT INSPECTION" in elementval or "POST DEPLOYMENT INSPECTION" in elementval:
                        driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("S")
                    else:
                        driver.find_element(By.NAME, 'R7_C1_L1_N').send_keys("T")
                except NoSuchElementException:
                    pass
                driver.find_element(By.NAME, 'cs').send_keys("2")  # crew size
                try:  # units produced
                    driver.find_element(By.NAME, 'R7_C25_L2_N').send_keys("1")
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R9_C30_L2_N').send_keys("1")
                driver.find_element(By.NAME, 'cat').send_keys("1")  # category
                try:  # corrected by
                    if driver.find_element(By.NAME, 'R7_C62_L12_N').is_enabled():
                        driver.find_element(By.NAME, 'R7_C62_L12_N').send_keys(FriendID)
                except NoSuchElementException:
                    if driver.find_element(By.NAME, 'R9_C61_L12_N').is_enabled():
                        driver.find_element(By.NAME, 'R9_C61_L12_N').send_keys(FriendID)
                try:  # inspected by
                    driver.find_element(By.NAME, 'R19_C43_L12_N').send_keys(UserID)
                except NoSuchElementException:
                    driver.find_element(By.NAME, 'R9_C22_L12_N').send_keys(UserID)
                element = driver.find_element(By.NAME, 'CANarrativeTextarea')  # corrective action
                element.clear()
                element.send_keys(CorrectiveAction)
                try:
                    driver.find_element(By.NAME, 'rad1').click()
                except NoSuchElementException:
                    pass
                driver.switch_to.default_content()
                try:  # see if error submitting
                    if len(jobsfailed) == 0:
                        driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        jobsfailed.append(job)
                        print(f'Job failed: {job}')
                        windows = driver.window_handles
                        driver.switch_to.window(windows[1])
                        return job
                    else:
                        driver.find_element(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        element = driver.find_elements(By.CLASS_NAME, "ui-dialog imdsalert ui-widget ui-widget-content ui-front ui-dialog-buttons ui-draggable")
                        driver.find_element(element[len(jobsfailed)-1])
                        jobsfailed.append(job)
                        print(f'Job failed: {job}')
                        windows = driver.window_handles
                        driver.switch_to.window(windows[1])
                        return job
                except (NoSuchElementException, IndexError):
                    windows = driver.window_handles
                    driver.switch_to.window(windows[1])
                    return job
        else:
            driver.close()
            windows = driver.window_handles
            driver.switch_to.window(windows[1])
            return "a"
    else:
        print("job is not Red or Amber")
        return "a"


def findtonumber(elyment):
    if "SCHEDULED" in elyment.text:
        starting_point = elyment.text.find("SCHEDULED") + 10
        iterable = 0
        while True:
            character = elyment.text[starting_point+iterable]
            if character in string.digits:
                iterable += 1
            else:
                jobidee = iterable + starting_point
                return elyment.text[starting_point:jobidee]
    else:
        starting_point = elyment.text.find("STARTED") + 10
        iterable = 0
        while True:
            character = elyment.text[starting_point+iterable]
            if character in string.digits:
                iterable += 1
            else:
                jobidee = iterable + starting_point
                return elyment.text[starting_point:jobidee]

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
    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/form/table[4]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/input[1]')))
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
    iterations = 0
    for count, eluhment in enumerate(iterjobs):
        if count == 0:
            continue
        if iterations >= len(jobstoautomate):
            break
        else:
            placeholderstring = jobcloser(eluhment, jobstoautomate[iterations])
            if placeholderstring.isdigit():
                jobids[jobstoautomate[iterations]] = placeholderstring
                iterations += 1
    print(jobids)
    print(jobsfailed)
    saveresult = Session(nowdateandtime, jobids, jobsfailed)
    saveresult.savejobs()
    input()


if __name__ == '__main__':
    TerminalID = input("Enter the Terminal ID!")
    UserID = input("Enter your User ID!")
    FriendID = input("Enter your coworkers ID!")
    EquipID = input("Enter the equipment ID!")
    Timestart = input("Enter the start Time!")
    Timeend = input("Enter the end Time!")
    CorrectiveAction = input("Enter the corrective action")
    jobstoautomate = []
    amountofjobs = 0
    while True:
        try:
            amountofjobs = int(input("How many jobs do you want to automate?"))
            break
        except ValueError:
            print("Wrong Value. Enter an integer!")
            continue
    i = 0
    while i < amountofjobs:
        try:
            append = str(int(input("Enter the TO number that you want to automate!")))
            jobstoautomate.append(append)
            i += 1
        except ValueError:
            print("Wrong Value. Enter an integer!")
            continue
    main()