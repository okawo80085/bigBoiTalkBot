from bpe import BPE

bpe_vocab = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-+=/<>\'":;,.[]'

with open('ref.txt', 'rt') as f:
	text = f.read().lower()

bpe = BPE()
bpe.add_seq(text)
bpe.set_merges(bpe_vocab)

bpe.embed(800)
bpe.save('data/words3.bpe')