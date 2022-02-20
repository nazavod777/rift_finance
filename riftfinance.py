from requests import Session
from random import choice, randint
from pyuseragents import random as random_useragent
from bs4 import BeautifulSoup
from names import get_first_name, get_last_name
from web3.auto import w3
from threading import Thread, Lock, active_count
from os import system
from ctypes import windll
from sys import stderr, exit
from loguru import logger
from urllib3 import disable_warnings
from time import sleep
from gc import collect
from msvcrt import getch


disable_warnings()
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
def clear(): return system('cls')
clear()
print('Telegram Channel - https://t.me/n4z4v0d\n')
windll.kernel32.SetConsoleTitleW('RiftFinance Auto Reger | by NAZAVOD')
lock = Lock()

mail_choice = int(input('Take mail type (1 - generate gmail from your mail; 2 - generate random mail; 3 - take mail from txt file): '))
if mail_choice == 1:
	user_mail = str(input('Enter your Gmail: '))
elif mail_choice == 3:
	mail_folder = str(input('Drop TXT with mails: '))
threads = int(input('Threads: '))
use_proxy = str(input('Use Tor proxies? (y/N): '))


def get_tor_proxy():
	proxy_auth = str(randint(1, 0x7fffffff)) + ':' + str(randint(1, 0x7fffffff))
	proxies = {'http': 'socks5://{}@localhost:9150'.format(proxy_auth), 'https': 'socks5://{}@localhost:9150'.format(proxy_auth)}
	return (proxies)


def random_mail_from_user(user_mail):
	randstring = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' if i != 15 else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(15)])
	email = user_mail.split('@')[0]+'+'+randstring+'@'+user_mail.split('@')[1]
	return (email)


def random_mail_absolute():
	randstring = ''.join([choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' if i != 25 else 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(25)])
	email = randstring+choice(['@yandex.ru', '@ya.ru', '@yandex.kz', '@ya.kz', '@yahoo.com', '@gmail.com', '@mail.ru', '@rambler.ru'])
	return (email)


def mail_from_file():
	with open(mail_folder, 'a') as file:
		email_massive = [row.strip() for row in file]
	return (email_massive)


def createwallet():
	account = w3.eth.account.create()
	privatekey = str(account.privateKey.hex())
	address = str(account.address)
	return(address, privatekey)


def mainth():
	while True:
		try:
			if mail_choice == 1:
				email = random_mail_from_user(user_mail)
			elif mail_choice == 2:
				email = random_mail_absolute()
			elif mail_choice == 3:
				global email_massive
				if 'email_massive' not in globals():
					email_massive = mail_from_file()
				if len(email_massive) < 1:
					raise Exception('mail_insufficiency')
				else:
					lock.acquire()
					email = email_massive.pop(0)
					lock.release()

			wallet_data = createwallet()
			session = Session()


			if use_proxy in ('y', 'Y'):
				session.proxies.update(get_tor_proxy())


			session.headers.update({'user-agent': random_useragent(), 'accept': '*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript', 'accept-language': 'ru,en;q=0.9', 'content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'origin': 'https://i.prefinery.com', 'referer': 'https://i.prefinery.com/projects/ansk9w4w/users/instant'})
			r = session.get('https://i.prefinery.com/projects/ansk9w4w/users/instant')
			request_param = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'new-password'}).get('name')
			csrf = BeautifulSoup(r.text, 'lxml').find('meta', {'name': 'csrf-token'}).get('content')
			firstname_data = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'given-name'}).get('name')
			lastname_data = BeautifulSoup(r.text, 'lxml').find('input', {'autocomplete': 'family-name'}).get('name')
			address_data = BeautifulSoup(r.text, 'lxml').find('input', {'placeholder': 'ETH Address'}).get('name')

			first_name = get_first_name()
			last_name = get_last_name()
			data = f'utf8=✓&display=inline&creation_location=&creation_location_title=&referrer=&referral_token=&utm_source=&utm_medium=&utm_campaign=&utm_term=&utm_content=&{request_param}=&{firstname_data}={first_name}&{lastname_data}={last_name}&tester[profile][email]=sdg346b3@ya.ru&{address_data}={wallet_data[0]}&commit=Register+for+the+Whitelist'.encode('utf-8')

			r = session.post('https://i.prefinery.com/projects/ansk9w4w/users', data=data, headers={'x-csrf-token': csrf})
			if 'We have added you to the' not in r.text:
				raise Exception('wrong_response')
		except Exception as error:
			if str(error) == 'mail_insufficiency':
				logger.success('All emails have been successfully processed')
				break
			elif str(error) == 'wrong_response':
				logger.error(f'Wrong response, code: {str(r.status_code)}')
			else:
				logger.error(f'Unexpected error: {str(error)}')
		else:
			with open('emails.txt', 'a') as file:
				file.write(f'{email}:{wallet_data[0]}:{wallet_data[1]}\n')
			logger.success(f'Email {email} successfully registered')


	print('\nPress any key to exit...')
	getch()
	exit()

def cleaner():
	while True:
		sleep(60)
		clear()
		collect()


if __name__ == '__main__':
	clear()
	Thread(target=cleaner).start()
	while True:
		if active_count() <= threads:
			Thread(target=mainth).start()