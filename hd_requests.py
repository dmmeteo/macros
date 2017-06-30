# -*- coding: utf-8 -*-
import sys
import requests
import grequests
from bs4 import BeautifulSoup
from getpass import getpass


# check if using python 3
print('python', sys.version)
if sys.version_info[0] == 3:
    xrange = range
    raw_input = input

# Main vars
USER, PASW = raw_input('Username:'), getpass()
SPAM = ['example@spam.com']
BASE_URL = 'https://example.com/'
SECONDARY_URL = 'https://example.com/something/%s/edit/'
rs = []  # AsyncRequests list
count = len(rs)  # AsyncRequests counter


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
        'subject': e.parent.select('td[title]')[0].get_text(),
        'url': SECONDARY_URL % ''.join([e for e in e.parent['onclick'] if e.isdigit()]),
    } for e in BeautifulSoup(resp.text, 'lxml').select('td') if e.get_text() in SPAM]
    
    print('Spam mails: %s' % len(spam_list))
    
    if spam_list:
        # Create prep_data from spamHTML inputs
        # TODO prep_data not only by inputs,
        prep = s.get(spam_list[0]['url'])
        prep_data = {f.get('name'): f.get('value') for f in BeautifulSoup(prep.text, 'lxml').select('input')
                     if f.get('name') and f.get('value')}
        
        # Do something with data
        prep_data.update({
            'priority': 'normal'
        })
        
        for t in spam_list:
            # Do something with data
            prep_data.update({
                'email': t['mail'],
                'subject': t['subject'],
            })

            # Aggregated AsyncRequest
            rs.append(
                grequests.post(t['url'], data=prep_data, session=s, headers=dict(Referer=t['url']))
            )
            
            # Print ready requests
            if count % 10 == 0:
                print('ready %s reuqests' % count)

        # Send them all at the same time
        grequests.map(rs)
    
    print('fin!')
