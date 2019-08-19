#!/bin/bash

path="/home/okwokk/Downloads/okawo's/python/bots-discord/bigBoiTalkBot/"

name=$(basename -- "$0")

echo gnome-terminal -- \"$PWD/$name\"

cd $path

for (( c=0; c<5; c++))
do
	python3 ai_train.py
	git commit ./modelz/ytc_adopted_bpe_edition.h5 -m "automated training"
	git push origin master
	echo batch $c complete
done
echo done