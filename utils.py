import nltk
from nltk.corpus import nps_chat
from mosestokenizer import MosesDetokenizer
import re

def clean_text(text):
	'''
	normalizes the string
	'''
	chars = {'\'':[u"\u0060", u"\u00B4", u"\u2018", u"\u2019"], 'a':[u"\u00C0", u"\u00C1", u"\u00C2", u"\u00C3", u"\u00C4", u"\u00C5", u"\u00E0", u"\u00E1", u"\u00E2", u"\u00E3", u"\u00E4", u"\u00E5"],
				'e':[u"\u00C8", u"\u00C9", u"\u00CA", u"\u00CB", u"\u00E8", u"\u00E9", u"\u00EA", u"\u00EB"],
				'i':[u"\u00CC", u"\u00CD", u"\u00CE", u"\u00CF", u"\u00EC", u"\u00ED", u"\u00EE", u"\u00EF"],
				'o':[u"\u00D2", u"\u00D3", u"\u00D4", u"\u00D5", u"\u00D6", u"\u00F2", u"\u00F3", u"\u00F4", u"\u00F5", u"\u00F6"],
				'u':[u"\u00DA", u"\u00DB", u"\u00DC", u"\u00DD", u"\u00FA", u"\u00FB", u"\u00FC", u"\u00FD"]}

	for gud in chars:
		for bad in chars[gud]:
			text = text.replace(bad, gud)

	if 'http' in text:
		return ''

	text = text.replace('&', ' and ')
	text = re.sub(r'\.( +\.)+', '..', text)
	text = re.sub(r'\.\.+', ' ^ ', text)
	text = re.sub(r',+', ',', text)
	text = re.sub(r'\-+', '-', text)
	text = re.sub(r'\?+', ' ? ', text)
	text = re.sub(r'\!+', ' ! ', text)
	text = re.sub(r'\'+', "'", text)
	text = re.sub(r';+', ':', text)
	text = re.sub(r'/+', ' / ', text)
	text = re.sub(r'<+', ' < ', text)
	text = re.sub(r'>+', ' > ', text)
	text = text.replace('%', '% ')
	text = text.replace(' - ', ' : ')
	text = text.replace(' -', " - ")
	text = text.replace('- ', " - ")
	text = text.replace(" '", " ")
	text = text.replace("' ", " ")

	for c in ".,:":
		text = text.replace(c + ' ', ' ' + c + ' ')

	text = re.sub(r' +', ' ', text.strip(' '))

	return text

def proc_text(msgObj, vocab):
	'''
	converts a Discord message object into a pre-processed string for AI
	'''
	text = str(msgObj.content)
	for i in msgObj.mentions:
		x = '<@{}>'.format(i.id)
		text = re.sub(x, 'U{}'.format(str(i.id)[:2]), text)

	text = clean_text(text)

	for i in text:
		if i not in vocab:
			text = text.replace(i, '')

	return text

def get_dataset():
	'''
	removes most not natural messages from the nps_chat dataset and returns it
	'''
	posts = list(nps_chat.posts())

	#removing the START, JOIN, PART messages
	while 1:
		try:
			posts.remove(['PART'])

		except Exception as e:
			pass

		try:
			posts.remove(['JOIN'])

		except Exception as e:
			pass

		try:
			posts.remove(['START'])

		except Exception as e:
			pass


		if ['PART'] not in posts and ['START'] not in posts and ['JOIN'] not in posts:
			break

	#normalization

	re_pat = re.compile('^[.][ ]ACTION[ ]')
	re_pat2 = re.compile('^[.][ ]wz')
	#re_pat3 = re.compile('^\d+ [/] [a-m] [a-zA-Z!@#$%^&*()_\\/\'";:<>,.?`~]+')
	re_pat4 = re.compile('^[.] [3-9] |^[1-2][0-9] [/] [a-m]')
	re_pat5 = re.compile('^[!] \w+|^UnScramble|^U\d+ [(] U\d+|^[:] U\d+')
	re_pat6 = re.compile('^[.] Question |^[.] Scorpio |^[.] Rooster ')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)
		result = re_pat.search(to_search)

		if result != None:
			temp = i[2:-1]
			temp.insert(0, '*')
			temp.append('*')
			posts[index] = temp
			#print (posts[index])

	print ('beep')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat2.search(to_search) != None:
			#print (to_search)
			del posts[index]
			del posts[index+1]
			del posts[index+2]

	print ('bop')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat4.search(to_search) != None:
			#print (to_search)
			del posts[index]

	print ('boop')

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat5.search(to_search) != None:
			#print (to_search)
			#print (' '.join(posts[index+1]))
			del posts[index]

	for index, i in enumerate(posts):
		to_search = ' '.join(i)

		if re_pat6.search(to_search) != None:
			#print (to_search)
			#print (' '.join(posts[index+1]))
			posts[index] = i[3:]
			#print (posts[index])

	return posts

def untokenize(nps_chatTokenized):
	'''
	takes a tokenized nps_chat dataset and returns a string list
	'''
	with MosesDetokenizer('en') as detokenizer:
		return [detokenizer(i) for i in nps_chatTokenized]

def dataset_to_inputs(textList):
	pass