import re

def clean_text(text):
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
	text = str(msgObj.content)
	for i in msgObj.mentions:
		x = '<@{}>'.format(i.id)
		text = re.sub(x, 'U{}'.format(i.name[:3]), text)

	text = clean_text(text)

	for i in text:
		if i not in vocab:
			text = text.replace(i, '')

	return text
