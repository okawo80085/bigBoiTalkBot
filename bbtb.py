import discord
from discord import Game
from discord.ext.commands import Bot
import re

BOT_PREFIX = '!'
TOKEN = 'NTkyNzg2Nzg0MDY1MTU5MTg4.XREZyg.FpMEVwfyNoW54eiPpW8_JGmdh6o'

gameStat = 'with idiots'


bop = Bot(command_prefix=BOT_PREFIX)


@bop.event
async def on_message(msg):
	if msg.author == bop.user:
		return
	print (msg.channel, msg.author, msg.content)

	if re.search('^[!]halp', str(msg.content)) != None:
		await bop.send_typing(msg.channel)
		await bop.send_message(msg.channel, 'hi, im a bot... i talk mad shit')

	elif len(proced) <= 300:
		#do the thing
		pass

	else:
		pass


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
