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
import random
from bpe import BPE

import logging

log = logging.getLogger('chat')

fh = logging.FileHandler(filename='chat.log', mode='a')

formatter = logging.Formatter('%(asctime)s - %(message)s')

fh.setFormatter(formatter)

log.addHandler(fh)
log.setLevel(logging.INFO)

print (tf.__version__)

our_github_repo_link = 'https://github.com/okawo80085/bigBoiTalkBot'

modelSaveFilePath = 'modelz/ytc_adopted_bpe_edition.h5'

try:
	botModel = load_model(modelSaveFilePath)

except Exception as e:
	print (e)
	raise Exception('failed to load model from the file \'{}\''.format(modelSaveFilePath))
	exit()


botModel.summary()

vocab = utils.vocab
bpe = BPE()
bpe.load('data/words.bpe')
endToken = bpe.str_to_token['\n']

BOT_PREFIX = '!'
TOKEN = 'your token'

gameStat = 'with humans'


bop = Bot(command_prefix=BOT_PREFIX)


@bop.event
async def on_message(msg):

	if msg.author == bop.user:
		log.info('{} > {}'.format('bot', utils.proc_text(msg, vocab)))
		return

	proced = utils.proc_text(msg, vocab).lower()

	log.info('{} > {}'.format('human', proced))

	print ('{} > {} : {}'.format(msg.channel, msg.author, proced))

	if re.search('^[!]halp', str(msg.content)) != None:
		await bop.send_typing(msg.channel)
		await bop.send_message(msg.channel, 'hi, im a bot... i talk mad shit\nim made by okawo#0901 and Dr. Big Cashew PhD Rodent TV#4485\nmy home:\n{}'.format(our_github_repo_link))

	elif 0 < len(proced) <= 200:
		await bop.send_typing(msg.channel)
		#do the thing
		#print (len(proced), ':', proced)

		#loop = asyncio.get_event_loop()

		resp, ix, _ = utils.generate_a_reply3(botModel, proced, bpe, endToken)
		resp = resp.strip('\n')
		print ([resp])
		#responce = random.choice(resps)[0]
		#print (ix)
		if len(resp) > 0:
			await bop.send_message(msg.channel, resp)

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
