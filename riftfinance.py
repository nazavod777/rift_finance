from requests import Session
from random import choice, randint
from pyuseragents import random as random_useragent
from bs4 import BeautifulSoup
from names import get_first_name, get_last_name
from web3.auto import w3
from threading import Thread, Lock, active_count
from os import system
from ctypes import windll
from sys import stderr
from loguru import logger
from urllib3 import disable_warnings
from time import sleep
from gc import collect
from json import loads


disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
def clear(): return system('cls')
clear()
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('RiftFinance Auto Reger | by NAZAVOD')
lock = Lock()

threads = int(input('Threads: '))
use_proxy = str(input('Use Tor proxies? (y/N): '))


def get_tor_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return (proxies)


def createwallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)


def mainth():
	while True:
		try:
			wallet_data = createwallet()
			session = Session()

			if use_proxy in ('y', 'Y'):
				session.proxies.update(get_tor_proxy())


			mail_session = Session()
			mail_session.headers.update({'User-Agent': random_useragent(), 'Accept': 'application/json, text/plain, */*', 'Referer': 'https://temprmail.com/'})

			r = mail_session.post('https://api.temprmail.com/v1/emails')
			email = loads(r.text)['email']
			checkmailsurl = loads(r.text)['emails_json_url']
			logger.info(f'Email {email} successfully received')
			

			session.headers.update({'user-agent': random_useragent(), 'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'accept-language': 'ru,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://i.prefinery.com', 'referer': 'https://i.prefinery.com/projects/ansk9w4w/users/instant'})
			r = session.get('https://i.prefinery.com/projects/ansk9w4w/users/instant')
			request_param = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'new-password'}).get('name')
			csrf = BeautifulSoup(r.text, 'lxml').find('meta', {'name': 'csrf-token'}).get('content')
			firstname_data = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'given-name'}).get('name')
			lastname_data = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'family-name'}).get('name')
			address_data = BeautifulSoup(r.text, 'lxml').find('input', {'placeholder': 'ETH Address'}).get('name')

			first_name = get_first_name()
			last_name = get_last_name()
			data = f'utf8=✓&display=inline&creation_location=&creation_location_title=&referrer=&referral_token=&utm_source=&utm_medium=&utm_campaign=&utm_term=&utm_content=&{request_param}=&{firstname_data}={first_name}&{lastname_data}={last_name}&tester[profile][email]={email}&{address_data}={wallet_data[0]}&commit=Register+for+the+Whitelist'.encode('utf-8')

			r = session.post('https://i.prefinery.com/projects/ansk9w4w/users', data=data, headers={'x-csrf-token': csrf})


			if 'We have added you to the' not in r.text:
				raise Exception('wrong_response')
			else:
				logger.info(f'Waiting for confirmation by email {email}')


			for i in range(13):
				r = mail_session.get(checkmailsurl)
				if 'Please Confirm Your Rift Finance Subscription' in r.text:
					msgid = str(loads(r.text)[0]['hash_id'])
					r = mail_session.get(f'https://tempremail-assets.s3.us-east-1.amazonaws.com/emails/{msgid}.json')
					verify_link = r.text.split('By confirming your email address you consent to receive updates from the Rift via email')[-1].split('<a href=\\"')[1].split('\\" target=\\"_blank\\"')[0].replace('\\/', '/')
					logger.success(f'The code was successfully received for {email}')
					break
				else:
					if i == 12:
						raise Exception('email_timeout')
					else:
						sleep(5)


			r = session.get(verify_link)


			if 'You have been successfully subscribed.' not in r.text:
				raise Exception('wrong_response')


		except Exception as error:
			if str(error) == 'mail_insufficiency':
				logger.success('All emails have been successfully processed')
				break
			elif str(error) == 'wrong_response':
				logger.error(f'Wrong response, code: {str(r.status_code)}')
			elif str(error) == 'email_timeout':
				logger.error(f'{email} email timeout')
			else:
				logger.error(f'Unexpected error: {str(error)}')
		else:
			with open('emails.txt', 'a') as file:
				file.write(f'{email}:{wallet_data[0]}:{wallet_data[1]}\n')
			logger.success(f'Email {email} successfully registered')


def cleaner():
	while True:
		clear()
		collect()
		sleep(60)


if __name__ == '__main__':
	Thread(target=cleaner, daemon=True).start()
	while True:
		if active_count()-1 <= threads:
			Thread(target=mainth).start()
