#ENG
## How to use
IMPORT TikTok module
```sh
from xh1scr import TikTok
```
Make task in asynchronous func
```sh
async def func():
	await TikTok.run('xh1c2')
	status = await TikTok.status()
	likes = await TikTok.likes()
	followers = await TikTok.followers()
	following = await TikTok.following()
	nickname = await TikTok.nickname()
	avatar = await TikTok.getavatar()
```
btw u can get list in run
```sh
from xh1scr import TikTok
async def func2():
	await TikTok.run(['xh1c2','example','example2','and','more'])
	status = await TikTok.status()
	likes = await TikTok.likes()
	followers = await TikTok.followers()
	following = await TikTok.following()
	nickname = await TikTok.nickname()
	avatar = await TikTok.getavatar()
```
#RU

## Как использовать
Для работы с ним надо сделать task в асинхронной функции
(я знаю есть такое же API но с подключенной авторизацией и поиском по id но плюс моего API это удобство использования)
```sh
from xh1scr import TikTok
async def func():
	await TikTok.run('xh1c2') 
	status = await TikTok.status() 
	likes = await TikTok.likes()
	followers = await TikTok.followers()
	following = await TikTok.following()
	nickname = await TikTok.nickname()
	avatar = await TikTok.getavatar()
```
Так же в run можно передать список значений
```sh
from xh1scr import TikTok
async def func2():
	await TikTok.run(['xh1c2','example','example2','and','more'])
	status = await TikTok.status()
	likes = await TikTok.likes()
	followers = await TikTok.followers()
	following = await TikTok.following()
	nickname = await TikTok.nickname()
	avatar = await TikTok.getavatar()
```
