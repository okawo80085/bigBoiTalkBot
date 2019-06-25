import nltk
from nltk.corpus import nps_chat
import re

vocab = ''.join([chr(i) for i in range(33, 127) if i != 96])

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
re_pat5 = re.compile('^[!] \w+')

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

#exit()

#print

for i in posts:
	print (' '.join(i))
