# -*- coding: utf-8 -*-
version=2.3
lencommands=0
import os
clear=lambda: os.system(f'cls && title Selfbot by LALOL {version} - {lencommands} Commands' if os.name == 'nt' else 'clear')
try:
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
	from plyer import notification
	from googletrans import Translator
	from emoji import EMOJI_DATA
	from qrcode import make
except:
	os.system('pip install -U discord.py-self==1.9.2 colorama requests plyer googletrans==4.0.0rc1 emoji qrcode')
	import discord
	from discord.ext import commands
	from colorama import init, Fore;init()
	import requests
from subprocess import Popen
from time import sleep
from webbrowser import open as webopen
from threading import Thread
from datetime import datetime
import random
import json
with open("config.json", "r", encoding="utf-8-sig") as f:
	try: config = json.load(f)
	except Exception as e:
		clear()
		print(e)
		print(Fore.LIGHTBLUE_EX+'\nОшибка конфига')
		while True: sleep(9)

theme=config['GENERAL']['theme']
if theme=='random':
	theme=random.choice(['standart', 'discord', 'hacker', 'beach'])
if theme=='standart':
	color={'Intro': Fore.RED, 'Info_name': Fore.MAGENTA, 'Info_value': Fore.YELLOW}
elif theme=='discord':
	color={'Intro': Fore.LIGHTBLUE_EX, 'Info_name': Fore.WHITE, 'Info_value': Fore.LIGHTCYAN_EX}
elif theme=='hacker':
	color={'Intro': Fore.LIGHTGREEN_EX, 'Info_name': Fore.GREEN, 'Info_value': Fore.WHITE}
elif theme=='beach':
	color={'Intro': Fore.LIGHTYELLOW_EX, 'Info_name': Fore.LIGHTYELLOW_EX, 'Info_value': Fore.LIGHTCYAN_EX}
else:
	clear()
	print(Fore.LIGHTBLUE_EX+'Неизвестная тема')
	while True: sleep(9)
on_command_error=True
Intro=color['Intro']+"""
   _____      ________          __     __             __    ___    __    ____  __ 
  / ___/___  / / __/ /_  ____  / /_   / /_  __  __   / /   /   |  / /   / __ \/ / 
  \__ \/ _ \/ / /_/ __ \/ __ \/ __/  / __ \/ / / /  / /   / /| | / /   / / / / /  
 ___/ /  __/ / __/ /_/ / /_/ / /_   / /_/ / /_/ /  / /___/ ___ |/ /___/ /_/ / /___
/____/\___/_/_/ /_.___/\____/\__/  /_.___/\__, /  /_____/_/  |_/_____/\____/_____/
                                         /____/                                   \n"""
lencommands=0
clear()
print(Intro)
print(Fore.WHITE+'Loading...')
pref=config['GENERAL']['prefix']
try: bot=commands.Bot(command_prefix=pref, case_insensitive=True, self_bot=True)
except Exception as e:
	clear()
	print(e)
	print(Fore.LIGHTBLUE_EX+'\nНа странице селфбота написано как решить эту ошибку!!!')
	sleep(3)
	webopen('https://github.com/Its-LALOL/Discord-Selfbot#-%D0%B5%D1%81%D0%BB%D0%B8-%D0%B2%D1%8B%D0%B4%D0%B0%D1%91%D1%82-%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D1%83', 2)
	while True: sleep(9)
bot.remove_command('help')
update=''

async def check(ctx):
	if not config['OTHER']['nuke_commands']:
		await ctx.message.edit(content='**__Selfbot by LALOL__\n\n:warning: Краш команды отключены! Для того чтобы включить краш команды измените файл config.json**')
		return False
	return True
def disco_status():
	while True:
		text=''
		lasttext=''
		for i in range(5):
			while True:
				emoji=random.choice(['Сотрудничество/Реклама'])
				if not emoji in text:
					text+=emoji
					break
		if text==lasttext: continue
		lasttext=text
		try:requests.patch("https://discord.com/api/v9/users/@me/settings", headers={'authorization': bot.http.token}, json={'custom_status': {'text': text}})
		except:pass
		sleep(5)
@bot.event
async def on_connect():
	global lencommands
	lencommands=len(bot.commands)
	for file in ['LICENSE', 'README.md']:
		try: os.remove(file)
		except: pass
	for file in os.listdir():
		if file.endswith('.txt') or file.endswith('.png'):
			os.remove(file)
	if config['OTHER']['disco_status']: Thread(target=disco_status).start()
#	status=config['GENERAL']['status']
	response=requests.get('https://discord.com/api/users/@me/settings', headers={'authorization': bot.http.token})
	status=response.json()['status']
	sstatus=discord.Status.online
	if status=='idle':
		sstatus=discord.Status.idle
	elif status=='dnd':
		sstatus=discord.Status.dnd
	elif status=='invisible':
		sstatus=discord.Status.invisible
	await bot.change_presence(status=sstatus)
	try:
		channel=bot.get_channel(config['OTHER']['auto_send_channel'])
		for i in config['OTHER']['auto_send_text']:
			await channel.send(i)
	except: pass
	clear()
	print(Intro)
	print(f"{color['Info_name']}Аккаунт: {color['Info_value']}{bot.user}{color['Info_name']}\nID: {color['Info_value']}{bot.user.id}{color['Info_name']}\nPrefix: {color['Info_value']}{pref}")
	if float(requests.get('https://raw.githubusercontent.com/Its-LALOL/Discord-Selfbot/main/cogs/version').text)>version:
		global update
		update=f':warning: Пожалуйста, обновите селфбота используя команду {pref}bot**\n**'
		print(f'{Fore.CYAN}Пожалуйста, обновите селфбота используя команду {Fore.LIGHTCYAN_EX}{pref}bot{Fore.RESET}{Fore.RED}\n')
		return
	print(Fore.RED)
if on_command_error:
	@bot.event
	async def on_command_error(ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			error='Недостаточно аргументов!'
		elif isinstance(error, commands.CommandNotFound):
			return
		elif isinstance(error, commands.BadArgument):
			error='Указан не правильный аргумент!'
		elif isinstance(error, discord.errors.Forbidden):
			error='Не достаточно прав для выполнения данной команды!'
		error=str(error).replace('Command raised an exception: ', '')
		print(f"{Fore.RED}[ERROR] {error}")
		try: await ctx.send(f'**__Selfbot by LALOL__\n\nПроизошла ошибка :x:\n```{error}```**')
		except: pass
@bot.event
async def on_command(ctx):
	time=datetime.now().strftime('%H:%M:%S')
	arguments=ctx.message.content.replace(pref+ctx.invoked_with, '')
	print(f'{Fore.LIGHTWHITE_EX}[{time}] {Fore.LIGHTCYAN_EX}{pref}{ctx.invoked_with}{Fore.LIGHTGREEN_EX}{arguments}{Fore.RESET}')
@bot.event
async def on_message_edit(before, after):
	await bot.process_commands(after)
@bot.command(aliases=['хелп', 'помощь'])
async def help(ctx, cat=None):
	if cat==None:
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:screwdriver:`{pref}help Tools` - Полезные команды\n:question:`{pref}help Info` - Команды для получения информации\n:joy:`{pref}help Fun` - Развлекательные команды\n:shield:`{pref}help Moderation` - Команды модерации\n:frame_photo:`{pref}help Images` - Команды связанные с изображениями\n:boom:`{pref}help Nuke` - Команды краша\n\n:octagonal_sign:`{pref}stopall` - Перезагружает селфбота\n:robot:`{pref}bot` - Получение ссылки на установку селфбота**')
		return
	cat=cat.lower()
	if cat=='tools':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:comet:`{pref}status [Тип статуса] [Текст]` - Меняет статус\n:broom:`{pref}purge [Количество]` - Удаляет ваши сообщения\n:pushpin:`{pref}masspin [Количество]` - Закрепляет сообщения\n:speaking_head:`{pref}spam [Количество] [Текст]` - Спам с обходом анти-спама\n:anger_right:`{pref}spamall [Количество] [Текст]` - Спам во все каналы\n:eye:`{pref}pingall [Количество]` - Пингует всех участников на сервере\n:envelope:`{pref}messages [Количество]` - Сохраняет сообщения в файл\n:busts_in_silhouette:`{pref}groupsleave` - Выходит из всех групп\n:thread:`{pref}spamthreads [Количество] [Имя ветки]` - Спамит ветками\n:white_flower:`{pref}spamthreadsall [Количество] [Имя ветки]` - Спамит ветками во все каналы\n:anger:`{pref}blocksend [Пинг/ID] [Текст]` - Отправляет сообщение в лс даже если вы добавили пользователя в чс\n:bubbles:`{pref}spamgroups [Количество] [Жертвы от 2 до 9]` - Спамит группами\n:jigsaw:`{pref}copystatus [Пинг/ID]` - Копирует RPC статус\n:flag_gb:`{pref}translate [На какой язык] [Текст]` - Переводчик\n:crown:`{pref}nitro [Количество] [classic/full]` - Генерирует нитро (без чекера)\n:smiley:`{pref}copyemojis [ID Сервера на который нужно скопировать]` - Копирует эмодзи\n:garlic:`{pref}hackpurge` - "Удаляет" все сообщения без прав\n:hamsa:`{pref}deletedms [Имя]` - Удаляет лс от ботов с таким же именем (поможет если вам заспамили лс)**')
	elif cat=='info':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:pen_fountain:`{pref}server` - Информация о сервере\n:pen_ballpoint:`{pref}user [Пинг/ID]` - Информация об аккаунте\n:key:`{pref}token [Токен]` - Получает информацию аккаунта по токену**')
	elif cat=='fun':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:face_with_symbols_over_mouth:`{pref}trolldelete [Пинг/ID]` - Удаление всех сообщений пользователя\n:imp:`{pref}trollreaction [Пинг/ID] [Эмодзи]` - Ставит реакции на все сообщения пользователя\n:ghost:`{pref}trollrepeat [Пинг/ID]` - Повторение всех сообщений пользователя\n:nauseated_face:`{pref}trollmove [Количество] [Пинг/ID]` - Перемещает пользователя по голосовым каналам\n:slight_smile:`{pref}untroll` - Выключение команды troll\n:stuck_out_tongue_winking_eye:`{pref}reactions [Количество] [Эмодзи] [ID Канала]` - Спамит реакциями\n:brain:`{pref}lags [Тип лагов] [Количество]` - Делает очень сильные лаги в канале\n:crystal_ball:`{pref}ball [Вопрос]` - Ответит на любые (почти) вопросы\n:rat:`{pref}hack [Пинг/ID]` - Фейковый взлом аккаунта\n:thought_balloon:`{pref}faketyping [Длительность в секундах] [ID Канала]` - Печатает сообщение\n:ringed_planet:`{pref}reactionbot [Эмодзи] [ID Сервера]` - Ставит реакции на все сообщения\n:speech_balloon:`{pref}say [Пинг/ID] [Текст]` - Пишет сообщение от имени другого пользователя\n:spider_web:`{pref}criptext` - Делает ваши сообщения очинь страшними!\n:rainbow:`{pref}color [rainbow/water/white]` - Делает ваши сообщения красочными!**')
	elif cat=='moderation':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:dagger:`{pref}ban [Пинг/ID] [Причина]` - Банит пользователя\n:ok_hand:`{pref}unban - [Пинг/ID]` - Разбанивает пользователя\n:door:`{pref}kick [Пинг/ID] [Причина]` - Кикает участника\n:mute:`{pref}mute [Пинг/ID] [Длительность] [Причина]` - Мутит участника\n:sound:`{pref}unmute [Пинг/ID] [Причина]` - Размучивает участника\n:timer:`{pref}slowmode [Длительность]` - Ставит слоумод на канал (Пример длительности: 3ч - 3 часа)\n:cloud_tornado:`{pref}nukechannel` - Удаляет все сообщения в канале +меняет айди канала**')
	elif cat=='images':
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:rainbow_flag:`{pref}lgbt [Пинг/ID]` - Делает аватарку пользователя "разноцветной"\n:speech_balloon:`{pref}comment [Пинг/ID] [Текст]` - Делает комментарий на ютубе\n:oncoming_police_car:`{pref}jail [Пинг/ID]` - "Садит" участника в тюрьму\n:low_brightness:`{pref}cmm [Текст]` - Change my mind\n:cat:`{pref}cat` - Картинка кота\n:dog:`{pref}dog` - Картинка собаки\n:fox:`{pref}fox` - Картинка лисы\n:koala:`{pref}koala` - Картинка коалы\n:feather:`{pref}lightshot [Количество]` - Генерирует случайные ссылки на lightshot\n:cd:`{pref}qrcode [Контент]` - Создаёт QRCode**')
	elif cat=='nuke':
		if await check(ctx):
			await ctx.message.edit(content=f'**__Selfbot by LALOL__\n{update}\n:skull:`{pref}nuke` - Уничтожение сервера\n:shushing_face:`{pref}silentnuke [ID Сервера] [Сообщение]` - Уничтожение сервера с обходом ВСЕХ анти-краш ботов +нельзя определить кто уничтожил сервер\n:smiling_imp:`{pref}spamchannels [Имя]` - Спам каналами\n:jack_o_lantern:`{pref}spamroles [Имя]` - Спам ролями\n:cold_face:`{pref}spamwebhooks [Сообщение]` - Спам вебхуками\n:clown:`{pref}deleteall` - Удаление всего\n\n`{pref}deletechannels` - Удаляет каналы\n`{pref}deleteroles` - Удаляет роли\n`{pref}deleteemojis` - Удаляет эмодзи**')
	else:
		await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:x: Напишите `{pref}help` для просмотра всех категорий команд**')
@bot.command(name='bot', aliases=['selfbot', 'бот', 'селфбот'])
async def __bot(ctx):
	await ctx.message.edit(content='**__Selfbot by LALOL__\n\nСсылка: https://github.com/Its-LALOL/Discord-Selfbot **')
@bot.command(aliases=['перезагрузка', 'стоп', 'перезагрузить', 'stop_all', 'остановить', 'reload', 'stop', 'reset'])
async def stopall(ctx):
	await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\nПерезагружаю селфбота...**')
	clear()
	Popen('python main.py')
	await ctx.message.edit(content=f'**__Selfbot by LALOL__\n\n:octagonal_sign: Селфбот был успешно перезагружен!**')
	await bot.logout()
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")
try: bot.run(config['GENERAL']["token"])
except:
	while True:
		clear()
		print(Fore.LIGHTBLUE_EX+"Неверный токен")
		while True: sleep(9)
