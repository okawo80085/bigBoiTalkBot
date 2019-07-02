made for discord hack week by okawo#0901 and Dr. Big Cashew PhD Rodent TV#4485.
A chating bot using AI and ```tensorflow```!


[invite the bot](https://discordapp.com/api/oauth2/authorize?client_id=592786784065159188&permissions=37215296&scope=bot)

some people named him `aiol`

#### ~~use test branch for a new model, the bot, that is currently up, is running of test branch code~~, test branch code is now merged with master

### requirements

Python libs:
* ```nltk```
* ```tensorflow==1.14.0```
* ~~```mosestokenizer```~~
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

**have fun :D**

### training the AI/neural network model

to train the model you need to pre-process the training data AT LEAST ONCE first or download [train_data_big_v3_only.npz (our training data)](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV)

optional if you downloaded [train_data_big_v3_only.npz](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV), to pre-process the data, run
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

~~training data will be uploaded later~~ training data:
[train_data_big_v3_only.npz](https://drive.google.com/open?id=1ZEp2oyQ0tz0T9GhOpK7_C0zOnOlC1abV)

note: `train_data_big_v3_only.npz` works with v3 model and new vocab only, if you want to use our old dataset you need to change models to v2 or v1 and use `old_vocab` from `utils.py`

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

and try to chat with it, note that it's severally under-trained


## how it works

we have an RNN neural network model, trained on normalized nps_chat corpus data, to predict the next character basted on the user input and characters it generated before.

we achived some progress with training but it seems that model design needs to be improved and/or our training data switched, to reddit data for example, and way more training.

out right switching from an RNN to a Seq2Seq model might also help.

## bugs

if you have any problems or bugs while running the code, feel free to open an issue on this repo
