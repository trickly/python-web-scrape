from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import os
defaultFileName = "Facility Attendance - A Age(Attendance,Admissions, Deaths) vs Gender.xls"

months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


def isFacility(txt):
    keywords = ["Facility", "Centre", "Clinic", "Disp",
                "Hospital", "Previlage", "School", "Health"]
    if any(word in txt for word in keywords):
        return True
    else:
        return False


def isState(txt):
    keywords = ["State"]
    if any(word in txt for word in keywords):
        return True
    else:
        return False


def isLGA(txt):
    keywords = ["Area", "Local", "Government"]
    if any(word in txt for word in keywords):
        return True
    else:
        return False


def isWard(txt):
    keywords = ["Ward"]
    if any(word in txt for word in keywords):
        return True
    else:
        return False


def moveToDownloadFolder(downloadPath, newPath, newFileName, fileExtension):
    got_file = False
    # Grab current file name.
    print(newFileName)
    while got_file == False:
        try:
            for f in os.listdir(downloadPath):
                if f == defaultFileName:
                    currentFile = os.path.join(downloadPath, defaultFileName)
                    got_file = True

        except:
            print("File has not finished downloading")
            time.sleep(2)

    # Create new file name
    fileDestination = newPath+newFileName+fileExtension

    os.rename(currentFile, fileDestination)

    return


def checkIfFileDownloaded(dlPath, fileName):
    for f in os.listdir(dlPath):
        if f == fileName:
            return True
    return False


def buttonClick(xpath):
    try:
        def find(driver):
            e = driver.find_element_by_xpath(xpath)
            if (e.get_attribute("disabled") == 'true'):
                return False
            return e
        element = wait.until(find)
    finally:
        element.click()
        print("finsihed")


# Uses selenium
# 1. Init with webdriver - Chrome
driver = webdriver.Chrome("C:/Patrick/Programming/dhis2/chromedriver.exe")
# dlPth will be the path to the download directory of the current user (on the system)
dlPth = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
# destPth will just be a directory where I'll put all my (renamed) files in.
destPth = dlPth+"\\dhis2data\\"

wait = WebDriverWait(driver, 10)

# Access url
driver.get('https://dhis2nigeria.org.ng/dhis/dhis-web-dashboard/')

# 2. Authentication
#assert "Python" in driver.title
username = driver.find_element_by_name("j_username")
username.clear()
username.send_keys("uikenyei")
# username.send_keys(Keys.RETURN)

password = driver.find_element_by_name("j_password")
password.clear()
password.send_keys("!OURrock123")
# password.send_keys(Keys.RETURN)
driver.find_element_by_id("submit").click()

# 3. Access Report Form
driver.get(
    "https://dhis2nigeria.org.ng/dhis/dhis-web-reporting/showDataSetReportForm.action")
#assert "No results found." not in driver.page_source
# driver.close()
dataSet = Select(driver.find_element_by_name("dataSetId"))
dataSet.select_by_visible_text("NHMIS Monthly Summary (version 2013)")
periodType = Select(driver.find_element_by_name("periodType"))
periodType.select_by_visible_text("Monthly")
periodId = Select(driver.find_element_by_name("periodId"))
periodCounter = 12
prevYearButton = driver.find_element_by_xpath(
    "//input[@type='button' and @value='Prev year']")
nextYearButton = driver.find_element_by_xpath(
    "//input[@type='button' and @value='Next year']")
yearCounter = 5


# 4. Necessary time sleeps & xPath set ups for buttons that get disabled
time.sleep(1)
main = driver.find_element_by_id("selectionTree")
root = main.find_element_by_xpath(
    "./ul/li[@id='oustOrgUnits5DPBsdoE8b']")
getReportButton = "//input[@type='button' and @value='Get report']"
dataCriteriaButton = "//input[@type='button' and @id='dataButton']"
downloadButton = "//input[@type='button' and @value='Download as Excel']"

currentState = ""
currentLGA = ""
currentWard = ""

# 5. Traverse Tree
nodes = []
stack = [root]
while(stack):
    current = stack[0]
    stack = stack[1:]
    name = current.find_element_by_xpath("./a")
    if(isFacility(name.text)):
        newFName = name.text
        print("$ " + newFName)
        # do something if facilitiy
        nodes.append(current)
        current.click()
        time.sleep(1)

        for year in range(2019, 2014, -1):
            yr = str(year)
            for month in range(periodCounter, 0, -1):
                mo = str(month)
                if not checkIfFileDownloaded(destPth, currentState + "-"+currentLGA + "-"+currentWard + "-"+newFName + "-"+yr + "-"+mo + ".xls"):
                    buttonClick(getReportButton)
                    time.sleep(4)
                    buttonClick(downloadButton)
                    time.sleep(6)
                    moveToDownloadFolder(
                        dlPth, destPth, currentState + "-"+currentLGA + "-"+currentWard + "-"+newFName + "-"+yr + "-"+mo, ".xls")
                    buttonClick(dataCriteriaButton)
                    time.sleep(1)
                if month is not 1:
                    periodId.select_by_index(months[month-1])

            periodId.select_by_index(0)  # resets select(month)
            prevYearButton.click()

        for year in range(0, yearCounter):  # resets year
            nextYearButton.click()

    # do file getting shit
    else:
        # check what lvl (fed/state/lga/ward) of current node
        if isState(name.text):
            currentState = name.text
        elif isLGA(name.text):
            currentLGA = name.text
        elif isWard(name.text):
            currentWard = name.text
        # find children
        # expand
        print("- " + name.text)
        expand = current.find_element_by_xpath("./span")
        expand.click()
        time.sleep(1)
        children = current.find_elements_by_xpath("./ul/*")
        for child in children:
            stack.insert(0, child)

print("_____")
