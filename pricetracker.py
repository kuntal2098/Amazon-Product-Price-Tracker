import requests
from bs4 import BeautifulSoup
from smtplib import SMTP

URL = "https://www.amazon.in/LG-Full-Monitor-Borderless-Design/dp/B08CF2VYB6/ref=sr_1_16?crid=ZLY6DIUVZRQ0&keywords=monitor&qid=1655619970&sprefix=monitor%2Caps%2C256&sr=8-16&th=1"
headers = {
    'Accept-Language': 'en-US',
    'User-Agent': 'Chrome/102.0.0.0'
}
response = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(response.content, features="lxml")

price = soup.find('span', attrs={'class': 'a-price-whole'})
price_list = price.text.split('.')[0].split(',')
price_num = int(''.join(price_list))

if price_num < 16000:
    product_title = soup.find('span', attrs={'id': 'productTitle'}).text.strip()
    message = f'Subject:Amazon Price Alert!\n\n{product_title} is now at ₹{str(price_num)}\nClick the below link:\n{URL}'
    message = u''.join(message).encode('utf-8').strip()

    FROM = '<Your Email>'
    PASS = '<Your Email Pass>'
    TO = ['Recipient Email1', 'Recipient Email2']

    with SMTP('smtp.gmail.com') as server:
        server.starttls()
        server.login(FROM, PASS)
        for mailID in TO:
            server.sendmail(FROM, mailID, message)
        server.quit()
        print("Email sent successfully!")