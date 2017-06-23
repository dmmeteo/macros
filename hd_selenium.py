# -*- coding: utf-8 -*-
'''
reuqirements:
brew install geckodriver
brew install chromedriver
'''

import sys
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# check if using python 3
print('python', sys.version)
if sys.version_info[0] == 3:
    xrange = range
    raw_input = input

user, pasw = raw_input('Username:'), getpass()
spam = ['example@spam.com']
base_url = 'https://example.com/'
driver = webdriver.Chrome()
driver.get(base_url)


def elements():
    res = [e for e in driver.find_elements_by_tag_name('td') if e.text in spam]
    return {'len': len(res),
            'elm': res}

try:
    driver.find_element_by_id('id_username').send_keys(user)
    driver.find_element_by_id('id_password').send_keys(pasw + Keys.RETURN)
    counter = elements()['len']
    if counter != 0:
        print('Spam mails: %s' % counter)

        for i in xrange(counter):
            element = elements()['elm']
            element[-1].click()
            driver.find_element_by_link_text(u'Редактировать').click()
            driver.find_element_by_id('id_closed').click()
            print('kill %s' % str(i+1))
            driver.find_element_by_xpath('//input[@type="submit"]').click()
            driver.get(base_url)
finally:
    print('fin!')
    driver.quit()
