import discord
from discord import Game
from discord.ext.commands import Bot
#import asyncio
#import aiohttp
#import json
#from concurrent.futures import ThreadPoolExecutor

import tensorflow as tf
from tensorflow.keras.models import load_model

import re
import utils
import string


print (tf.__version__)

our_github_repo_link = 'https://github.com/okawo80085/bigBoiTalkBot'

modelSaveFileName = 'bigBoiAI_v2.h5'

try:
	botModel = load_model(modelSaveFileName)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFileName))
	exit()


botModel.summary()

vocab = sorted([chr(i) for i in range(32, 127) if i != 96])
vocab.insert(0, None)


BOT_PREFIX = '!'
TOKEN = 'your token'

gameStat = 'with humans'


bop = Bot(command_prefix=BOT_PREFIX)


@bop.event
async def on_message(msg):
	if msg.author == bop.user:
		return
	proced = utils.proc_text(msg, vocab)

	print ('{} > {} : {}'.format(msg.channel, msg.author, proced))

	if re.search('^[!]halp', str(msg.content)) != None:
		await bop.send_typing(msg.channel)
		await bop.send_message(msg.channel, 'hi, im a bot... i talk mad shit\nim made by okawo#0901 and Dr. Big Cashew PhD Rodent TV#4485\nmy home:\n{}'.format(our_github_repo_link))

	elif 0 < len(proced) <= 200:
		await bop.send_typing(msg.channel)
		#do the thing
		#print (len(proced), ':', proced)

		#loop = asyncio.get_event_loop()

		resp, ix, ix_prob = utils.generate_a_reply(botModel, proced, vocab)

		print (ix)

		responce = re.sub('[ ]+', ' ', ''.join(resp).strip(' '))
		print ([responce])

		if len(responce) > 0:
			await bop.send_message(msg.channel, responce)

	else:
		await bop.send_message(msg.channel, 'i cant process that ^')


@bop.event
async def on_ready():
	await bop.change_presence(game=Game(name="{}... !halp".format(gameStat)))
	print("name: " + bop.user.name)

async def list_servers():
	await bop.wait_until_ready()
	print ('-'*25)
	print("Current servers connected:")
	for server in bop.servers:
		print(server.name, 'channels with access', len(server.channels))
	print ('-'*25)

	return False

try:
	bop.loop.create_task(list_servers())
	bop.run(TOKEN)
	bop.close()

except Exception as e:
	bop.close()
	print (e)

print ('(σ´-ω-`)σ')

# https://discordapp.com/api/oauth2/authorize?client_id=592786784065159188&permissions=37215296&scope=bot
