from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

import time
import os
defaultFileName = "Facility Attendance - A Age(Attendance,Admissions, Deaths) vs Gender.xls"
dontWant = ["Cold", "Store"]
months = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


def isFacility(txt):
    keywords = ["Facility", "Centre", "Clinic", "Disp",
                "Hospital", "Previlage", "School", "Health"]
    if any(word in txt for word in keywords)and not any(w in txt for w in dontWant):
        return True
    else:
        return False


def isState(txt):
    keywords = ["State"]
    if any(word in txt for word in keywords) and not any(w in txt for w in dontWant):
        return True
    else:
        return False


def isLGA(txt):
    keywords = ["Area", "Local", "Government"]
    if any(word in txt for word in keywords) and not any(w in txt for w in dontWant):
        return True
    else:
        return False


def isWard(txt):
    keywords = ["Ward"]
    if any(word in txt for word in keywords) and not any(w in txt for w in dontWant):
        return True
    else:
        return False


def moveToDownloadFolder(downloadPath, newPath, newFileName):
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
    fileDestination = newPath+newFileName
    os.rename(currentFile, fileDestination)



def checkIfFileDownloaded(dlPath, fileName):
    for f in os.listdir(dlPath):
        if f == fileName:
            return True
    return False

def formatFilename(filename):
    filename = filename.replace("/", "~")
    return filename

def logLastWorkedOn(filePath, fileName, fileStage, indices):
    try:
        os.remove(filePath + "log.txt")
    except FileNotFoundError:
        pass
    f = open (filePath +"log.txt", 'w')
    print ("writing")
    #f.write(fileStage + "\r" + fileName+"\n")
    levels = '-'.join(str(x) for x in indices)
    f.write(levels)
    print (levels)
    f.close()


def revertLastWorkedOn(filePath):
    try:
        f = open(filePath + "log.txt", 'r')
        log = f.readlines()
        f.close()
    except FileNotFoundError:
        log =""
    print (log)
    if log == "":
        indices = [36,14,11]
        print(indices)
    else:
        indices = log[0].split("-")
        for index,i in enumerate(indices):
            print (i)
            indices[index] = int(i)
    return indices


def buttonClick(xpath):
    try:
        def find(driver):
            e = driver.find_element_by_xpath(xpath)
            if (e.get_attribute("disabled") == 'true'):
                return False
            return e
        element = wait.until(find)
        element.click()
    finally:
        print("finsihed")


def buttonWait(xpath):
    element_present = None
    try:
        element_present = EC.element_to_be_clickable((By.XPATH, xpath))
        WebDriverWait(driver, 10).until(element_present).click()
    except TimeoutException:
        print("Timed out waiting for page to load")
        buttonWait(xpath)

def buttonWaitByEle(ele):
    element_present = ele
    try:
        WebDriverWait(driver, 10).until(element_present).click()
    except TimeoutException:
        print("Timed out waiting for page to load")

def buttonWaitForClass(browser, total_wait=100):
    try:
        # Give only one class name, if you want to check multiple classes then 'and' will be use in XPATH
        # e.g //*[contains(@class, "class_name") and contains(@class, "second_class_name")]
        elem = browser.find_element_by_xpath('[contains(@class, "selected")]')
        print("a lot")
    except:
        total_wait -= 1
        time.sleep(1)
        if total_wait > 1: buttonWaitForClass(browser, total_wait)
    
    print("yes")
    elem.click()

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
# assert "Python" in driver.title
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
# assert "No results found." not in driver.page_source
# driver.close()
dataSet = Select(driver.find_element_by_name("dataSetId"))
dataSet.select_by_visible_text("NHMIS Monthly Summary (version 2013)")
periodType = Select(driver.find_element_by_name("periodType"))
periodType.select_by_visible_text("Monthly")
periodId = Select(driver.find_element_by_name("periodId"))
periodCounter = 12
prevYearButton = "//input[@type='button' and @value='Prev year']"
nextYearButton = "//input[@type='button' and @value='Next year']"
    
yearCounter = 4


# 4. Necessary time sleeps & xPath set ups for buttons that get disabled
time.sleep(1)
main = driver.find_element_by_id("selectionTree")
root = main.find_element_by_xpath(
    "./ul/li[@id='oustOrgUnits5DPBsdoE8b']")
getReportButton = "//input[@type='button' and @value='Get report']"
dataCriteriaButton = "//input[@type='button' and @id='dataButton']"
downloadButton = "//input[@type='button' and @value='Download as Excel']"
buttonWait(prevYearButton)

currentState = ("", 0)
currentLGA = ("", 0)
currentWard = ("", 0)
lastWorkedOn = revertLastWorkedOn(destPth)
# 5. Traverse Tree
stack = [(root, 0)]
while(stack):
    # Set current Node
    current = stack[0]
    stack = stack[1:]
    name = current[0].find_element_by_xpath("./a")

    # check if current node is what was last worked on
    currentLevel = currentState[1], currentLGA[1], currentWard[1]

    # if node is facility
    if(isFacility(name.text)):
        currentFacility = (name.text, current[1])
        print("$ " + currentFacility[0] + "... " + str(currentFacility[1]) + " - "+ str(name) + " // " + str(current[0]))
        #buttonWaitForClass(current[0])
        #buttonWaitByEle(name)
        name.click()
        time.sleep(2)
        for year in range(2018, 2014, -1):#4
            yr = str(year)
            for month in range(periodCounter, 0, -1):
                mo = str(month)
                extension = ".xls"
                filename = currentState[0] + "-"+currentLGA[0] + "-" + \
                    currentWard[0] + "-"+currentFacility[0] + "-"+yr + "-"+mo
                filename = formatFilename(filename)
                if not checkIfFileDownloaded(destPth, filename+extension):
                    logLastWorkedOn(destPth, filename, "PRE", currentLevel)
                    buttonWait(getReportButton)
                    time.sleep(2)
                    buttonWait(downloadButton)
                    time.sleep(2)
                    moveToDownloadFolder(dlPth, destPth, filename+extension)
                    buttonWait(dataCriteriaButton)
                    logLastWorkedOn(destPth, filename, "PST", currentLevel)
                    time.sleep(1)
                if month is not 1:
                    periodId.select_by_index(months[month-1])

            periodId.select_by_index(0)  # resets select(month)
            buttonWait(prevYearButton)


        for year in range(0, yearCounter):  # resets year
            buttonWait(nextYearButton)

    # if not facility, continue to traverse tree
    else:

        # find children
        # expand
        print("- " + name.text)
        expand = current[0].find_element_by_xpath("./span")
        expand.click()
        time.sleep(1)
        children = current[0].find_elements_by_xpath("./ul/*")

        if name.text == "ng Federal Government":
            for index, child in enumerate(children, start=0):
                if(index <= lastWorkedOn[0]):
                    # saves html element & index of current level of tree into tuple
                    # 0->bc it pust the most recent child the start of the stack
                    stack.insert(0, (child, index))
                    print("inserting states: " + child.text + "....."+ str(index))
        # check what lvl (fed/state/lga/ward) of current node & save position of node
        elif isState(name.text):
            currentState = (name.text, current[1])
            for index, child in enumerate(children, start=0):
                if((index <= lastWorkedOn[1]) and currentState[1] == lastWorkedOn[0]) or (currentState[1] < lastWorkedOn[0]):
                    # second clause = last logged state
                    # saves html element & index of current level of tree into tuple
                    # 0->bc it pust the most recent child the start of the stack
                    stack.insert(0, (child, index))
                    print("inserting LGAS: " + child.text + "....."+ str(index))
        elif isLGA(name.text):
            currentLGA = (name.text, current[1])
            for index, child in enumerate(children, start=0):
                if((index <= lastWorkedOn[2] and currentLGA[1] == lastWorkedOn[1]) or (currentLGA[1]< lastWorkedOn[1])):
                    # saves html element & index of current level of tree into tuple
                    # 0->bc it pust the most recent child the start of the stack
                    stack.insert(0, (child, index))
                    print("inserting wards: " + child.text + "....." + str(index))

        elif isWard(name.text):
            currentWard = (name.text, current[1])
            for index, child in enumerate(children, start=0):
                # saves html element & index of current level of tree into tuple
                # 0->bc it pust the most recent child the start of the stack
                stack.insert(0, (child, index))
        for i in stack:
            print (i[0].text + "...." + str(i[1]))

print("_____")
