made for discord hack week by okawo#0901 and Dr. Big Cashew PhD Rodent TV#4485.
A chating bot using AI and ```tensorflow```!


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

to train the model you need to pre-process the training data, AT LEAST ONCE, first

to pre-process the data, run
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


## bugs

if you have any problems or bugs while running the code, feel free to open an issue on this repo