import time, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup

driver = webdriver.Firefox(executable_path=r'D:\Fight\Downloads\geckodriver.exe')

# username and pass to login to your account

username = <ENTER YOUR USERNAME  - string>
password = <ENTER YOUR PASSWORD - string>

# open the main page

driver.get('https://rabota.ua/')
time.sleep(2) # Let the user actually see something!

# click to login button, filling username and password and click login button

driver.find_element_by_xpath("//div[contains(text(),'Войти')]").click()
time.sleep(2)

driver.find_element_by_xpath('//input[@type=\'password\']').send_keys(password)

actions = ActionChains(driver)
actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
actions.send_keys(username)
actions.perform()
time.sleep(2)

driver.find_element_by_xpath("//span[contains(text(),'Войти')]").click()
time.sleep(4)

# filling the search field with needed vacancy and choosing the city Kiev

vacancy = 'Финансовый аналитик'
driver.find_element_by_xpath("//input[@type='text']").send_keys(vacancy)
time.sleep(2)
driver.find_element_by_xpath("//span[contains(text(),'Вся Украина')]").click()
time.sleep(2)
driver.find_element_by_xpath("//li/span[contains(text(),'Киев')]").click()
time.sleep(2)

# open a file with vacancies from previous mailing list and creating a list

old_links_list = []
f = open('vacancies.txt', 'r')
for row in f:
    old_links_list.append(row.rstrip("\n"))
print("open a file with vacancies from previous mailing list and creating a list")
print(old_links_list)
f.close()

# creating a list with vacancies from a current search

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'lxml')
match = soup.find_all('a', class_='card')

lst_links = []
for link in match:
    x = link['href'].split('?')[0]
    if x not in old_links_list:
        if 'company1450274' not in x:
            lst_links.append(x)

    # if len(x) == 1:
    #     if x[0] not in old_links_list:
    #         lst_links.append(x[0])

print('lst_links: ', lst_links)

# removing duplicates

lst_links = set(lst_links)
print("Number of new vacancies: ", len(lst_links))

# writing current vacancies mailing list to a file

f = open('vacancies.txt', 'a')

# open each vacancy by one and sending cv

excepted_links = []
count_sent = 0
count_not_sent = 0
robotaua_domain = 'https://rabota.ua/'
for link in lst_links:
    driver.get(robotaua_domain + link)
    time.sleep(2)

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')

    try:
        # driver.find_element_by_xpath("//santa-button[@type='primary']").click()
        driver.find_element_by_xpath("//span[contains(text(), 'Откликнуться')]").click()
        time.sleep(2)

        # driver.find_element_by_xpath("//span[contains(text(),'Присылать мне на email похожие вакансии')]").click()
        driver.find_element_by_xpath("//span[contains(text(),'Не присылать мне на email похожие вакансии')]").click()
        time.sleep(1)

        # if vacancy needs an answer of level of English

        if soup.find('app-apply-control-questions'):
            driver.find_element_by_xpath("//span[contains(text(),'Выберите ответ')]").click()
            time.sleep(1)
            driver.find_element_by_xpath("//li[contains(text(),'продвинутый')]").click()
            time.sleep(1)

        driver.find_element_by_xpath("//button[contains(text(),'Отправить резюме')]").click()
        # driver.find_element_by_xpath("//span[contains(text(),'Откликнуться')]").click()
        time.sleep(1)

        # writing just answered vacancy to a file

        f.write(link + '\n')
        count_sent += 1
        print("Отправлено: ", count_sent)
        time.sleep(1)

    except:
        excepted_links.append(link)
        count_not_sent += 1
        print("Не отправлено: ", count_not_sent)




print("ОТПРАВЛЕННЫЕ: ", count_sent)
print("НЕ ОТПРАВЛЕННЫЕ :", count_not_sent)
print(excepted_links)
f.close()
driver.quit()