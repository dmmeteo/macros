# -*- coding: utf-8 -*-
import requests
import grequests
from bs4 import BeautifulSoup
from getpass import getpass

USER, PASW = raw_input('Username:'), getpass()
SPAM = ['example@spam.com']
BASE_URL = 'https://example.com/'
SECONDARY_URL = 'https://example.com/something/%s/edit/'

with requests.session() as s:
    # Retrieve the CSRF token first
    req = s.get(BASE_URL)  # sets cookie
    csrftoken = s.cookies['csrftoken']
    
    # Auth
    login_data = dict(username=USER, password=PASW, csrfmiddlewaretoken=csrftoken)
    resp = s.post(req.url, data=login_data, headers=dict(Referer=BASE_URL))
    
    # Aggregated spam urls & mails
    spam_list = [{
        'mail': e.get_text(),
        'url': SECONDARY_URL % ''.join([e for e in e.parent['onclick'] if e.isdigit()]),
    } for e in BeautifulSoup(resp.text, 'lxml').select('td') if e.get_text() in SPAM]
    
    print('Spam mails: %s' % len(spam_list))

    count = 0
    if spam_list:
        for t in spam_list:
            # Create data from spamHTML inputs
            prep = s.get(t['url'])
            data_dict = {f.get('name'): f.get('value') for f in BeautifulSoup(prep.text, 'lxml').select('input')
                         if f.get('name') and f.get('value')}
        
            # Do something with data
            data_dict.update({
                'source': 'email',
                'closed': 'on',
                'department': 'd_tehnicheskaya-podderzhka',
                'priority': 'normal'
            })
            # r = grequests.post(t['url'], data=data_dict, cookies=prep.cookies, headers=dict(Referer=SECONDARY_URL)) # TODO not working async
            r = s.post(t['url'], data=data_dict, cookies=prep.cookies, headers=dict(Referer=t['url']))
        
            if count is not 0 and count % 10 == 0:
                print('ready %s reuqests' % count)
            count += 1

    print('fin!')