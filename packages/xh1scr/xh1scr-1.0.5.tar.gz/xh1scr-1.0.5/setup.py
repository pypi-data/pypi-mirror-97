# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xh1scr']
install_requires = \
['aiohttp>=3.7.4,<4.0.0',
 'asyncio>=3.4.3,<4.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0']

setup_kwargs = {
    'name': 'xh1scr',
    'version': '1.0.5',
    'description': 'Asynchronous TikTok API Wrapper',
    'long_description': "#ENG\n## How to use\nIMPORT TikTok module\n```sh\nfrom xh1scr import TikTok\n```\nMake task in asynchronous func\n```sh\nasync def func():\n\tawait TikTok.run('xh1c2')\n\tstatus = await TikTok.status()\n\tlikes = await TikTok.likes()\n\tfollowers = await TikTok.followers()\n\tfollowing = await TikTok.following()\n\tnickname = await TikTok.nickname()\n\tavatar = await TikTok.getavatar()\n```\nbtw u can get list in run\n```sh\nfrom xh1scr import TikTok\nasync def func2():\n\tawait TikTok.run(['xh1c2','example','example2','and','more'])\n\tstatus = await TikTok.status()\n\tlikes = await TikTok.likes()\n\tfollowers = await TikTok.followers()\n\tfollowing = await TikTok.following()\n\tnickname = await TikTok.nickname()\n\tavatar = await TikTok.getavatar()\n```\n#RU\n\n## Как использовать\nДля работы с ним надо сделать task в асинхронной функции\n(я знаю есть такое же API но с подключенной авторизацией и поиском по id но плюс моего API это удобство использования)\n```sh\nfrom xh1scr import TikTok\nasync def func():\n\tawait TikTok.run('xh1c2') \n\tstatus = await TikTok.status() \n\tlikes = await TikTok.likes()\n\tfollowers = await TikTok.followers()\n\tfollowing = await TikTok.following()\n\tnickname = await TikTok.nickname()\n\tavatar = await TikTok.getavatar()\n```\nТак же в run можно передать список значений\n```sh\nfrom xh1scr import TikTok\nasync def func2():\n\tawait TikTok.run(['xh1c2','example','example2','and','more'])\n\tstatus = await TikTok.status()\n\tlikes = await TikTok.likes()\n\tfollowers = await TikTok.followers()\n\tfollowing = await TikTok.following()\n\tnickname = await TikTok.nickname()\n\tavatar = await TikTok.getavatar()\n```\n",
    'author': 'perfecto',
    'author_email': 'rektnpc@mail.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
