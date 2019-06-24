import nltk
from nltk.corpus import nps_chat

vocab = [i for i in range(33, 127) if i != 96]

posts = nps_chat.posts()
raw_text = "<new>".join(posts)
raw_text = raw_text.lower()