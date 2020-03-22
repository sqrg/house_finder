import json
import os
import requests
import sqlite3

from time import sleep

import credentials

def generate_request_payload(page):

    with open(os.path.join(PROJECT_PATH, 'request_payload.json')) as json_file:
        data = json.load(json_file)

    if page != 1:
        data['pagina'] = page

    return json.dumps(data)

def make_postings_request(page):

    r = requests.post(
        f'{BASE_URL}{API_URL}',
        headers = {'Content-Type': 'application/json'},
        data    = generate_request_payload(page)
        )

    return r.json()

def send_message(url, message):

    payload = {
        'chat_id'   : credentials.CHAT_ID,
        'text'      : message,
        'parse_mode': 'MarkdownV2'
    }

    r = requests.get(url, params=payload)
    response = r.json()

    if response['ok'] is not True:
        error_code = response['error_code']
        error_description = response['description']

        send_message(url, f'*ERROR*: {error_code}\. See log for details')

        print(error_code)
        print(error_description)
        print(payload)
        print()

def send_listing(title, price, expenses, url):

    message = f'*{title}*\n*Alquiler*: {price}\n*Expensas*: {expenses}\n\n[Link]({url})'
    
    send_message(f'https://api.telegram.org/bot{credentials.BOT_TOKEN}/sendMessage', message)

# Constants
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_URL     = 'https://www.zonaprop.com.ar'
API_URL      = '/rplis-api/postings'

if __name__ == '__main__':

    conn = sqlite3.connect(os.path.join(PROJECT_PATH, 'database.db'))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS postings (id text, url text, title text)''')

    response = make_postings_request(1)

    for page in range(1, int(response['paging']['totalPages']) + 1):

        if page == 1:
            current_response = response
        else:
            current_response = make_postings_request(page)

        for post in current_response['listPostings']:
            
            # Check if already notified
            id = (post['postingId'], )
            c.execute('SELECT * FROM postings WHERE id=?', id)
            row = c.fetchone()

            if row is None:

                title = str(post['title']).replace('-', '\-').replace('.', '\.')

                price = post['priceOperationTypes'][0]['prices'][0]['amount']

                try:
                    expenses = post['expenses']['amount']
                except:
                    expenses = ''

                url = '{}{}'.format(BASE_URL, post['url'])

                # Send message
                send_listing(title, price, expenses, url)

                # Add to notified list
                row_to_save = (post['postingId'], post['url'], post['generatedTitle'])
                c.execute('INSERT INTO postings VALUES (?, ?, ?)', row_to_save)
                conn.commit()

                sleep(10)

    conn.close()