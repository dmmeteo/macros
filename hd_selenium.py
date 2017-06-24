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

USER, PASW = raw_input('Username:'), getpass()
SPAM = ['example@spam.com']
BASE_URL = 'https://example.com/'
browser = webdriver.Chrome()
browser.get(BASE_URL)


def elements():
    res = [e for e in browser.find_elements_by_tag_name('td') if e.text in SPAM]
    return {'len': len(res),
            'elm': res}

try:
    browser.find_element_by_id('id_username').send_keys(USER)
    browser.find_element_by_id('id_password').send_keys(PASW + Keys.RETURN)
    counter = elements()['len']
    if counter != 0:
        print('Spam mails: %s' % counter)

        for i in xrange(counter):
            element = elements()['elm']
            element[-1].click()
            browser.find_element_by_link_text(u'Редактировать').click()
            browser.find_element_by_id('id_closed').click()
            print('kill %s' % str(i+1))
            browser.find_element_by_xpath('//input[@type="submit"]').click()
            browser.get(BASE_URL)
finally:
    print('fin!')
    browser.quit()
