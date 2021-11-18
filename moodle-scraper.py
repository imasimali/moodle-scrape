import os
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

# ENTER Credentials
userName = "USERNAME"
mypass = "PASSWORD"
courseID = "Enter Your Course ID from URL"

# Enable headless browser
options = Options()
options.headless = True

# disable image loading
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference('permissions.default.image', 2)
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

driver = webdriver.Firefox(options=options,firefox_profile=firefox_profile)

# LOGIN TO MOODLE
driver.get("http://tmoodle.fccollege.edu.pk/moodle/login/index.php")
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userName)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(mypass)
driver.find_element_by_xpath('//*[@id="loginbtn"]').click()

# Goto course participants page with show all enabled
driver.get("http://tmoodle.fccollege.edu.pk/moodle/user/index.php?id="+courseID+
          "&perpage=100")

data = []

peeps_elem = driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div/div/section/div/div/div/div[2]/div[3]/table/tbody/tr/td/a")
for each in peeps_elem:
    url = each.get_attribute("href")
    driver.execute_script('window.open("{}", "_blank");')
    driver.switch_to.window(driver.window_handles[1])
    driver.get(url)

    try:
      name = driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div/div[1]/div[2]/h2').text

      email = driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div/div/section[1]/ul/li/dl/dd/a').text

    except Exception as e:
      email = "N/A"
      print(e)

    print(name, email)

    text = [name,email]

    # Save data to csv
    data.append(text)

    with open('students.csv', 'w') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(data)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
