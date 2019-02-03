from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time;


driver = webdriver.Chrome("C:/Patrick/Programming/dhis2/chromedriver.exe")
driver.get('https://dhis2nigeria.org.ng/dhis/dhis-web-dashboard/')
#assert "Python" in driver.title
username = driver.find_element_by_name("j_username")
username.clear()
username.send_keys("uikenyei")
#username.send_keys(Keys.RETURN)


password = driver.find_element_by_name("j_password")
password.clear()
password.send_keys("!OURrock123")
#password.send_keys(Keys.RETURN)
driver.find_element_by_id("submit").click()

driver.get("https://dhis2nigeria.org.ng/dhis/dhis-web-reporting/showDataSetReportForm.action")
#assert "No results found." not in driver.page_source
#driver.close()

dataSet = Select(driver.find_element_by_name("dataSetId"))
#dataSet.select_by_index(index)
dataSet.select_by_visible_text("NHMIS Monthly Summary (version 2013)")
#dataSet.select_by_value(value)
periodType = Select(driver.find_element_by_name("periodType"))
periodType.select_by_visible_text("Monthly")

#federal = driver.find_element_by_id("oustOrgUnits5DPBsdoE8b")
#federal = driver.find_element_by_xpath("oustOrgUnits5DPBsdoE8b")


time.sleep(10)
main = driver.find_element_by_id("selectionTree")
expand= main.find_element_by_xpath("./ul/li[@id='oustOrgUnits5DPBsdoE8b']/span")
expand.click()
time.sleep(10)

#lists= main.find_elements_by_xpath("./ul/li[@id='oustOrgUnits5DPBsdoE8b']/*")
#for ele in lists:
 #   print (ele)
 #   print("La - "+ele.get_attribute("class"))

lists2 = main.find_elements_by_xpath("./ul/li[@id='oustOrgUnits5DPBsdoE8b']/ul/*")
for ele in lists2:
    print (ele)
    print("id - "+ele.get_attribute("id"))

#driver.find_elements_by_xpath("//span[@class='toggle']").click()
#federal.click()
#federal.find_elements_by_xpath(".//span[@class='toggle']").click()
#federal.find_elements_by_xpath(".//span[@class='toggle']").click()
