```
#!/usr/bin/env python
#-*- coding: utf-8 -*-

#2016年 04月 06日 星期三 15:16:02 CST by Demobin
class ACState():

    def __init__(self, depth):

        self.depth = depth
        self.failure = None
        self.emits = None
        self.success = dict()
        self.index = 0

    def getDepth(self):
        return self.depth

    def addEmit(self, emit):
        #print('add emit:', emit)
        if self.emits == None:
            self.emits = set()
        self.emits.add(emit)

    def getMaxValueId(self):
        if self.emits == None or len(self.emits) == 0:
            return None
        return self.emits.__iter__().__next__()

    def addEmitList(self, emits):
        for emit in emits:
            self.add(emit)

    def getEmit(self):
        return self.emits == None and set() or self.emits

    def isAcceptable(self):
        return self.depth > 0 and self.emits != None

    def failure(self):
        return self.failure

    def setFailure(self, failState, fail = []):
        self.failure = failState
        fail[self.index] = failState.index

    def nextState2(self, char, ignoreRootState):
        nextState = self.success.get(char)
        if not ignoreRootState and nextState == None and self.depth == 0:
            nextState = self
        return nextState

    def nextState(self, char):
        return self.nextState2(char, False)

    def nextStateIgnoreRootState(self, char):
        return self.nextState2(char, True)

    def addState(self, char):
        nextState = self.nextStateIgnoreRootState(char)
        if nextState == None:
            nextState = ACState(self.depth + 1)
            self.success[char] = nextState
        return nextState

    def getStates(self):
        return self.success.values()

    def getTransitions(self):
        return self.success.keys()

    def getSuccess(self):
        return self.success

    def getIndex(self):
        return self.index

    def setIndex(self, index):
        self.index = index

    def __repr__(self):
        s = 'ACState{'
        s += 'depth = %s,'%self.depth
        s += 'ID = %s,'%self.index
        s += 'emits = %s,'%self.emits
        s += 'success = %s,'%self.success.keys()
        s += 'failureId = %s,'%(self.failure == None and '-1' or self.failure.index())
        s += 'failure = %s'%self.failure
        s += '}'
        return s

```
```
#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#2016年 04月 06日 星期三 15:16:02 CST by Demobin

import time
import codecs

from collections import deque

from state import ACState

class Hit():
    
    def __init__(self, begin, end, value):
        self.begin = begin
        self.end = end
        self.value = value

    def __repr__(self):
        return '[%d:%d] = %s'%(begin, end, value)

class ACDATrie():

    def __init__(self):
        self.check = []
        self.base = []
        self.fail = []
        self.output = []
        self.v = []
        self.l = []
        self.size = 0

    def transitionWithRoot(self, nodePos, char):
        b = self.base[nodePos]
        p = b + c + 1
        if b != check[p]:
            if nodePos == 0:
                return 0
            return -1
        return p

    def getState(self, curState, char):
        newCurState = self.transitionWithRoot(curState, char)
        while newCurState == -1:
            curState = self.fail[curState]
            newCurState = self.transitionWithRoot(curState, char)
        return newCurState

    def storeEmits(self, pos, curState, emits):
        hitArray = self.output[curState]
        if hitArray != None:
            for hit in hitArray:
                emits.append(Hit(pos - self.l[hit], pos, self.v[hit]))

    def parseText(self, text):
        pos = 1
        curState = 0
        emits = list()
        for char in text:
            curState = self.getState(curState, char)
            self.storeEmits(pos, curState, emits)
            pos += 1
        return emits

    def parseTextProcessor(self, text, processor):
        pos = 1
        curState = 0
        for char in text:
            curState = self.getState(curState, char)
            hitArray = self.output[curState]
            if hitArray != None:
                for hit in hitArray:
                    processor.hit(pos - self.l[hit], pos, self.v[hit])
                pos += 1

    def exactMatchSearch(self, key, pos, length, nodePos):
        if length <= 0:
            length = len(key)

        if nodePos <= 0:
            nodePos = 0

        result = -1
        b = self.base[nodePos]
        p = 0
        for i in range(length):
            p = b + key[i] + 1
            if b == self.check[p]:
                b = base[p]
            else:
                return result

        p = b
        n = self.base[p]
        if b == self.check[p] and n < 0:
            result = -n - 1
        
        return result
            

    def exactMatchSearch(self, key):
        return exactMatchSearch2(key, 0, 0, 0)

    def get(self, key):
        index = self.exactMathSearch(key)
        if index >= 0:
            return self.v[index]
        return None

    def getSize(self):
        return len(self.v)

class ACDATrieBuilder():
    
    def __init__(self, acInstance):
        self.ac = acInstance
        self.rootState = ACState(0)
        self.used = []
        self.allocSize = 0
        self.progress = 0
        self.nextCheckPos = 0
        self.keySize = 0
        self.allcounter = 0

    def addKeyword(self, keyword, index):
        curState = self.rootState
        for char in keyword:
            #print('add keyword char:', char)
            curState = curState.addState(char)
        curState.addEmit(index)
        self.ac.l[index] = len(keyword)

    def addAllKeyword(self, keywords):
        i = 0
        for keyword in keywords:
            #print('add keyword:', keyword)
            self.addKeyword(keyword, i)
            i += 1

    def resize(self, size):
        self.ac.base = [0 for i in range(size)]
        self.ac.check = [0 for i in range(size)]
        self.used = [False for i in range(size)]
        
        self.allocSize = size

    @profile
    def insert(self, siblings):

        self.allcounter += 1
        #print('================', len(siblings), siblings[0][1])
        begin = 0 
        pos = max(siblings[0][0], self.nextCheckPos) - 1
        nonZeroNum = 0
        first = 0

        if self.allocSize <= pos:
            self.resize(pos + 1)

        '''
        #outer:
        counter = 0
        outer = False
        while True:
            pos += 1

            #print('pos: %d, allocSize: %d'%(pos, self.allocSize))

            #if self.allocSize <= pos:
            #    self.resize(pos + 1)

            if self.ac.check[pos] != 0:
                nonZeroNum += 1
                continue
            elif first == 0:
                self.nextCheckPos = pos
                first = 1

            begin = pos - siblings[0][0]

            #if self.allocSize <= (begin + siblings[-1][0]):
            #    l = (1.05 > 1 * self.keySize / (self.progress + 1)) and 1.05 or 1.0 * self.keySize / (self.progress + 1)
            #    self.resize(self.allocSize * l)

            if self.used[begin]:
                continue

            for sibling in siblings:
                if self.ac.check[begin + sibling[0]] != 0:
                    #outer = True
                    #counter += 1
                    break
            else:
                #outer = False
                continue

            break

        if 1.0 * nonZeroNum / (pos - self.nextCheckPos + 1) >= 0.95:
            self.nextCheckPos = pos

        '''

        self.used[begin] = True

        self.ac.size = (self.ac.size > begin + siblings[-1][0] + 1) and self.ac.size or (begin + siblings[-1][0] + 1)

        for sibling in siblings:
            self.ac.check[begin + sibling[0]] = begin

        for sibling in siblings:
            #newSiblingsLen = len(sibling[1].getSuccess()) + 1
            newSiblings = []
            if self.fetch(sibling[1], newSiblings) == 0:
                self.ac.base[begin + sibling[0]] = -sibling[1].getMaxValueId() - 1
                self.progress += 1
            else:
                h = self.insert(newSiblings)
                self.ac.base[begin + sibling[0]] = h

            sibling[1].setIndex(begin + sibling[0])

        return begin

    def fetch(self, parent, siblings):
        #print(parent)
        if parent.isAcceptable():
            #print('isAcceptable')
            fakeNode = ACState(- (parent.getDepth() + 1))
            fakeNode.addEmit(parent.getMaxValueId())
            siblings.append((0, fakeNode))

        #for state in parent.getSuccess().iteritems():
        #py3和py2的方法不一致
        for state in parent.getSuccess().items():
            siblings.append((ord(state[0]) + 1, state[1]))
            #print('integer: %d, value: %s'%(ord(state[0]) + 1, state[1]))

        return len(siblings)

    def constructOutput(self, state):
        emits = state.getEmit()
        if emits == None or len(emits) == 0: return
        output = [n for n in emits]
        self.ac.output[state.getIndex()] = output

    def constructFailureStates(self):
        fail = [0 for i in range(self.ac.size)]
        fail[1] = self.ac.base[0]

        output = [0 for i in range(self.ac.size + 1)]
        
        dq = deque() 

        for state in self.rootState.getStates():
            state.setFailure(self.rootState, fail)
            dq.append(state)
            self.constructOutput(state)

        while len(dq) != 0:
            state = dq.remove()
            for char in stat.getTransitions():
                cState = state.nextState(char)
                dq.append(cState)

                failState = cState.failure()

                while failState.nextState(char) == None:
                    failState = failState.failure()

                newFailState = failState.nextState(char)

                cState.setFailure(newFailState, fail)
                cState.addEmit(newFailState.emit())

                self.constructOutput(state)

    @profile
    def buildDATrie(self, keySize):
        progress = 0
        self.keySize = keySize
        self.resize(65536 * 32)
        
        self.ac.base[0] = 1
        self.nextCheckPos = 0

        rootNode = self.rootState
        #siblings = list(range(len(rootNode.getSuccess())))
        siblings = []
        self.allcounter = 0
        self.fetch(rootNode, siblings)
        
        self.insert(siblings)
        print('all counter', self.allcounter)

    def build(self, pairs):
        self.ac.v = pairs.values()
        self.ac.l = list(range(len(self.ac.v)))
        keys = pairs.keys()
        self.addAllKeyword(keys)
        self.buildDATrie(len(keys))
        self.used = None
        self.constructFailureStates()
        self.rootState = None
        #self.loseWeight()

def loadText(path):

    with codecs.open(path, 'r', 'utf-8') as fd:
        lines = fd.readlines()
        return lines

def loadDict(path):
    
    dic = []

    with codecs.open(path, 'r', 'utf-8') as fd:
        lines = fd.readlines()
        for line in lines:
            dic.append(line.strip())

        return dic

def test(dictPath, textPath):
    dic = loadDict(dictPath)
    texts = loadText(textPath)
    
    acdaTrie = ACDATrieBuilder(ACDATrie())
    
    dicMap = {}
    for word in dic:
        #print(word)
        dicMap[word] = word
    
    acdaTrie.build(dicMap)

    print('dic len: %d, text char: %d'%(len(texts), len(dic)))

    acdaTrie.ac.parseText(text)

if __name__ == '__main__':
    test('./resources/cn/dictionary.txt', './resources/cn/text.txt')

```
