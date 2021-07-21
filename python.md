### fire
```
pip install fire
import fire
fire.Fire(func)
```

### sorted multi key
```
s = sorted(s, key = lambda x: (x[1], x[2]))
```

### Shift Left/Right
```
from collections import deque

words = ['a', 'b', 'c']
deqWords = deque(words)
#Shift Left
deqWords.rotate(-1)
#Shift Right
deqWords.rotate(1)

```

### re
named group
```
restr = '(?P<name>regex)'
re.sub(restr, '\g<name>text_to_replace', string)
\s whitespace
\S anything but whitespace
```

### Combinations/Permutations
```
import itertools
words = ['a', 'b', 'c']
#Combinations
print list(itertools.combinations(words, 2))
#Permutations
print list(itertools.permutations(a, 2))
#Combination between two list

```

### Factorial
```
import math
math.factorial(2)
```
