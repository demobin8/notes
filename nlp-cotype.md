### 1. Library
`cd code/Model/retype`

`make`
> retype.cpp:7:25: fatal error: gsl/gsl_rng.h: No such file or directory

`sudo apt install libgsl-dev`

`sudo pip install jsonrpclib unidecode nltk`
### 2. Config
stanford dir path

`vi code/DataProcessor/nlp_parse.py`

comment line 77

> parser = NLPParser('code/DataProcessor/stanford-corenlp-python/corenlp/stanford-corenlp-full-2015-04-20')

`parser = NLPParser('code/DataProcessor/stanford-corenlp-python/corenlp/stanford')`

`cp code/DataProcessor/stanford-corenlp-python/corenlp/stanford/default.properities code/DataProcessor/stanford-corenlp-python/corenlp/default.properities`

`vi code/DataProcessor/stanford-corenlp-python/corenlp/corenlp.py`

comment line 48

> DIRECTORY = "stanford-corenlp-full-2013-06-20"

```
DIRECTORY = "stanford"
```
