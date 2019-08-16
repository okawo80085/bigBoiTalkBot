from bpe import BPE
import utils

bpe_vocab = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-+=/<>\'":;,.[]'

data = utils.get_dataset()

text = '\n'.join(data)
text = text.lower()

bpe = BPE()
bpe.add_seq(text)
bpe.set_merges(bpe_vocab)

bpe.embed(800)
bpe.save('bpeData/words.bpe')