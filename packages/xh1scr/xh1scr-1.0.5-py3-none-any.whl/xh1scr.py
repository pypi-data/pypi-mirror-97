import asyncio
import aiohttp
from bs4 import BeautifulSoup
global loop
loop = asyncio.get_event_loop()
class TikTok():
	async def run(acc):
		global accsx
		global soup
		accsx = []
		if type(acc) == list:
			for accs in acc:
				async with aiohttp.ClientSession() as session:
					async with session.get('http://tiktok.com/@%s?lang=en' % accs) as response:
						html = await response.text()
						soup = BeautifulSoup(html,'lxml')
						accsx.append(soup)
			soup = None
			return(accsx)
		else:
			async with aiohttp.ClientSession() as session:
					async with session.get('http://tiktok.com/@%s?lang=en' % acc) as response:
						html = await response.text()
						soup = BeautifulSoup(html,'lxml')
						accsx = None
						return(soup)
	async def status():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('h2','share-desc mt10')
					if parse.text == 'No bio yet.':
						parse = None
					else:
						stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('h2','share-desc mt10')
				if parse.text == 'No bio yet.':
					stats = None
				else:
					stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def nickname():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('h1','share-sub-title')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('h1','share-sub-title')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def following():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Following')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Following')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def followers():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Followers')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Followers')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				
	async def likes():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find('strong',title='Likes')
					stats = parse.text
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find('strong',title='Likes')
				stats = parse.text
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
	async def getavatar():
		global accsx
		global soup
		res = []
		if soup == None:
			for soup in accsx:
				try:
					parse = soup.find_all('img')
					stats = parse[-1].get('src')
					res.append(stats)
				except AttributeError as e:
					raise AttributeError('wrong id')
					
			soup = None
			return(res)
		else:
			try:
				parse = soup.find_all('img')
				stats = parse[-1].get('src')
				return(stats)
			except AttributeError as e:
				raise AttributeError('wrong id')
				

