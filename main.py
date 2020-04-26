# import pdfkit
# pdfkit.from_url('https://twitter.com/filgmartin', 'filipe.pdf')

# import weasyprint
# pdf = weasyprint.HTML('https://twitter.com/filgmartin').write_pdf()
# open('filipe.pdf', 'wb').write(pdf)

# import time

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# driver = webdriver.Firefox()
# time.sleep(5)

# def save_screenshot(driver: webdriver.Firefox, path: str = '.screenshot.png'):
#     # Ref: https://stackoverflow.com/a/52572919/
#     original_size = driver.get_window_size()
#     print('part1: ',original_size)
#     required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
#     required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
#     print('part2: ', required_height, required_width)
#     driver.set_window_size(required_width, required_height)
#     driver.get("https://twitter.com/filgmartin")
#     # driver.save_screenshot(path)  # has scrollbar
#     driver.find_element_by_tag_name('body').screenshot(path)  # avoids scrollbar
#     # driver.set_window_size(original_size['width'], original_size['height'])
#     driver.quit()

# save_screenshot(driver, 'filipe.png')

# from selenium import webdriver
# import json

# chrome_options = webdriver.ChromeOptions()
# settings = {
#        "recentDestinations": [{
#             "id": "Save as PDF",
#             "origin": "local",
#             "account": "",
#         }],
#         "selectedDestinationId": "Save as PDF",
#         "version": 2
#     }
# prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
# chrome_options.add_experimental_option('prefs', prefs)
# chrome_options.add_argument('--kiosk-printing')
# CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
# driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=CHROMEDRIVER_PATH)
# driver.get("https://google.com")
# driver.execute_script('window.print();')
# driver.quit()

# from selenium import webdriver
# from io import BytesIO
# from PIL import Image

# driver = webdriver.Chrome(executable_path='path to your driver')
# driver.get('your url here')
# img = Image.open(BytesIO(driver.find_element_by_tag_name('body').screenshot_as_png))
# img.save('filename.pdf', "PDF", quality=100)

# import asyncio
# from pyppeteer import launch

# async def main():
#     browser = await launch(headless=True)
#     page = await browser.newPage()

#     await page.goto('https://twitter.com/filgmartin')
#     await page.screenshot({'path': 'scasdreen.png', 'fullPage': True})
#     await browser.close()


# asyncio.get_event_loop().run_until_complete(main())
# import imgkit

# imgkit.from_url('https://twitter.com/filgmartin', 'out1232.jpg')
import time, datetime, os
from os import listdir
from os.path import isfile, join

import requests, bs4

main_folder = 'html'
if not os.path.exists(main_folder):
    print('Creating folder: ', main_folder)
    os.makedirs(main_folder)

accounts = [
    'filgmartin',
    'CarlosBolsonaro'
    ]

for account in accounts:
    account_folder = '{}/{}'.format(main_folder, account)
    if not os.path.exists(account_folder):
        print('Creating folder: ', account_folder)
        os.makedirs(account_folder)

log_file = 'main_log.txt'

def log(message):
    fh = open(log_file, 'a')
    fh.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ': ' + message + '\n')
    fh.close()
    print(message)


while True:
    for account in accounts:
        response = requests.get('https://twitter.com/'+account)
        html_code = response.text
        instant = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
        date_nums = instant.split('_')
        account_folder = '{}/{}'.format(main_folder, account)
        path = account_folder + '/'
        for date_num in date_nums:
            path += date_num + '/'
            if not os.path.exists(path):
                log('Creating folder: ' + path)
                os.makedirs(path)
        soup = bs4.BeautifulSoup(html_code, 'html.parser')
        # tweets = soup.find_all(attrs={'class': 'js-tweet-text-container'})
        # print(len(html_code), len(tweets), html_code.count('js-tweet-text-container'))
        # for tweet in tweets:
        #     print(tweet.get_text())

        # saving screenshot to account folder
        fh = open('{}/{}.html'.format(account_folder, instant),'w')
        fh.write(html_code)
        fh.close()

        # saving screenshot to date folder
        fh = open('{}/index.html'.format(path),'w')
        fh.write(html_code)
        fh.close()

        # making index.html to account folder
        html_code = '<html><body><ol>{}</ol></body></html>'
        onlyfiles = [f for f in listdir(account_folder) if isfile(join(account_folder, f))]
        onlyfiles_code = ''
        for file in onlyfiles:
            onlyfiles_code += '<li><a href=\'{}\'>{}</a></li>'.format(file, file)
        html_code = html_code.format(onlyfiles_code)
        fh = open('{}/index.html'.format(account_folder, instant),'w')
        fh.write(html_code)
        fh.close()

    time.sleep(60)