from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

facilities = {}


class Node:
    def __init__(self, name, age):
        self.name = name
        self.children = []

    def addChild(self, node):
        self.children.append(node)

    def getChildren(self):
        return self.children


def isFacility(node):
    keywords = ["Facilitiy", "Center", "Centre"]
    if any (word in node.name for word in keywords):
        return True
    else:
        return False


def enterTraversal():
    doPreOrder()


def doPreOrder():
    print()


# Uses selenium
# Init with webdriver - Chrome
driver = webdriver.Chrome("C:/Patrick/Programming/dhis2/chromedriver.exe")
# Access url
driver.get('https://dhis2nigeria.org.ng/dhis/dhis-web-dashboard/')

# Authentication
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

# Access Report Form
driver.get(
    "https://dhis2nigeria.org.ng/dhis/dhis-web-reporting/showDataSetReportForm.action")
#assert "No results found." not in driver.page_source
# driver.close()

dataSet = Select(driver.find_element_by_name("dataSetId"))
# dataSet.select_by_index(index)
dataSet.select_by_visible_text("NHMIS Monthly Summary (version 2013)")
# dataSet.select_by_value(value)
periodType = Select(driver.find_element_by_name("periodType"))
periodType.select_by_visible_text("Monthly")

# Necessary time sleeps
time.sleep(3)
main = driver.find_element_by_id("selectionTree")
expandFederalGov = main.find_element_by_xpath(
    "./ul/li[@id='oustOrgUnits5DPBsdoE8b']/span")
expandFederalGov.click()
time.sleep(3)

#lists= main.find_elements_by_xpath("./ul/li[@id='oustOrgUnits5DPBsdoE8b']/*")
# for ele in lists:
#   print (ele)
#   print("La - "+ele.get_attribute("class"))

states = main.find_elements_by_xpath(
    "./ul/li[@id='oustOrgUnits5DPBsdoE8b']/ul/*")
for state in states:

    stateName = state.find_element_by_xpath("./a")
    print(stateName.text)
    print("id - "+state.get_attribute("id"))

# driver.find_elements_by_xpath("//span[@class='toggle']").click()
# federal.click()
# federal.find_elements_by_xpath(".//span[@class='toggle']").click()
# federal.find_elements_by_xpath(".//span[@class='toggle']").click()
