#!/bin/bash

path="some/path/"
titleName="automated trainer"

name=$(basename -- "$0")

echo -ne "\033]0;$titleName\007"

echo gnome-terminal -- \"$PWD/$name\"

cd $path

for (( c=0; c<8; c++))
do
	python3 ai_train.py
	git commit ./modelz/ytc_adopted_bpe_edition.h5 -m "automated training"
	git push origin master
	killall python3.6
	echo
	echo batch $c complete
	echo
done
echo done
shutdown now