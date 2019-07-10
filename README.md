made for discord hack week by okawo#0901 and Dr. Big Cashew PhD Rodent TV#4485.
A chating bot using Neural Networks and ```tensorflow```!


[invite the bot](https://discordapp.com/api/oauth2/authorize?client_id=592786784065159188&permissions=37215296&scope=bot)

some people named him `aiol`, but they also say it named it self...

### requirements

Python libs:
* ```nltk```
* ```tensorflow==1.14.0```
* ```sacremoses```
* ```numpy```
* ```discord.py```

Nltk packages:
* ```nps_chat```
* ```names```
* ```moses_sample```

and Python3 😃

#### note: if nltk packages and/or nltk is not installed, training and data processing most likely wont work

## running the bot

to run the bot you need to have all dependencies installed

replace ```TOKEN = 'your token'``` with your actual bot token

and to start the bot run
```python
python3 bbtb.py
```
or
```python
python bbtb.py
```

this will run the bot using the v3.1 model

**have fun :D**

### training the AI/neural network model

to train the model you need to pre-process the training data AT LEAST ONCE first or download [train_data_big2_v3andup.npz (our training data)](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV)

optional if you downloaded [train_data_big2_v3andup.npz](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV), to pre-process the data, run
```python
python3 data_processing.py
```
or
```python
python data_processing.py
```

to train the model, run
```python
python3 ai_train.py
```
or
```python
python ai_train.py
```


```bigBoiAI.h5``` is the model's save file

training data:
[train_data_big2_v3andup.npz](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV)

note: `train_data_big2_v3andup.npz` works with v3 or higher models and new vocab only, if you want to use our old dataset you need to change models to v2 or v1 and use `old_vocab` from `utils.py`

**vocab examples**
```python
>>> utils.vocab 	# new vocab, works with v3 or higher models only
[None, ' ', '\n', 'A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e', 'F', 'f', 'G', 'g', 'H', 'h', 'I', 'i', 'J', 'j', 'K', 'k', 'L', 'l', 'M', 'm', 'N', 'n', 'O', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', '(', '[', '{', '}', ']', ')', '\\', '/', '|', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', ',', '.', '!', '?', ':', ';', "'", '"', '~', '<', '>']

>>> utils.old_vocab 	# old vocab, works with models v1 and v2
[None, ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']
```

## using the AI/neural network in predict mode/talking with it!!!
this functionality is complitley incomporated in ```bbtb.py``` i. e. **bigBoiTalkBot**, but if you want to just test out the AI after training


run
```python
python3 ai_chat.py
```
or
```python
python ai_chat.py
```

and try to chat with it, note that it's ~~severally~~ a bit under-trained


## automatic model evaluation

make file `test.txt` and populate it with messages for evaluation, 1 per line, leave the last line empty

then run
```python
python3 ai_chat_test.py
```
or
```python
python ai_chat_test.py
```

it will then output a score for `test.txt` and for model's responses

## how it works

we have an RNN neural network model, trained on normalized nps_chat corpus data, to predict the next character basted on the user input and characters it generated before.

we achived some progress with training but it seems that model design needs to be improved and/or our training data switched, to reddit data for example, and way more training.

out right switching from an RNN to a Seq2Seq model might also help.

## bugs

report them here