## 0 编译和安装
略
### 1.0 语料处理
语料一般按90%用作训练，10%用作测试进行处理，处理后的文件格式如下：
```
迈    v    B
向    v    E
充    v    B
满    v    E
希    n    B
望    n    E
的    u    S
新    a    S
世    n    B
纪    n    E
...
```
第一列为字，第二列为词性，第三列为词的位置，特征含义为：S(Single), B(Begin), M(Middle), E(End) 
人民日报半年语料处理脚本如下：
```
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 2016年 01月 20日 星期三 11:47:33 CST by Demobin

import sys

data_path = '/root/work/corpus/people-daily.txt.utf8'

def splitWord(words):
    uni = words.decode('utf-8')
    rst = list()    
    for u in uni:
        rst.append(u.encode('utf-8'))
    return rst   

#4 feature
#S/B/E/M
#Single单字/Begin词的开始/End词的结束/Middle词的中间
def get4Feature(chars):
    length = len(chars)
    if length == 1: return ['S']
    elif length == 2: return ['B','E']
    elif length > 2:
        rst = list()
        rst.append('B')
        for i in range(0, length - 2):
            rst.append('M')
        rst.append('E')
        return rst

#6 feature
#S/B/E/M/M1/M2
def get6Feature(chars):
    length = len(chars)
    if length == 1: return ['S']
    elif length == 2: return ['B','E']
    elif length == 3: return ['B','M','E']
    elif length == 4: return ['B','M1','M','E']
    elif length == 5: return ['B','M1','M2','M','E']
    elif length > 5:
        rst = list()
        rst.append('B')
        rst.append('M1')
        rst.append('M2')
        for i in range(0, length - 4):
            rst.append('M')
        rst.append('E')
        return rst

def save(fdtrain, fdtest, isTest, word, tag, feature):
    if isTest: write(fdtest, word, tag, feature)
    else: write(fdtrain, word, tag, feature)

def write(fd, word, tag, feature): 
    if len(word) > 0:
        chars = splitWord(word)
        if feature == '4': features = get4Feature(chars)
        elif feature == '6': features = get6Feature(chars)
        for i in range(0, len(chars)):
            c = chars[i]
            f = features[i]
            fd.write(c + '\t' + tag + '\t' + f + '\n')
    else: fd.write('\n')

#B,M,M1,M2,M3,E,S
def convertFeature(feature):

    fdcorpus = open(data_path, 'r')
    fdtrain = open(data_path + '-feature' + feature + '.train', 'w' )
    fdtest = open(data_path + '-feature' + feature + '.test', 'w')

    lines = fdcorpus.readlines()
    i = 0
    for l in lines:
        i += 1
        l = l.strip('\r\n\t ')
        words = l.split(' ')

        test = False
        #十分之一为测试，十分之九为训练
        if i % 10 == 0: test = True

        for word in words:
            word = word.strip('\t ')
            if len(word) > 0:       
                word_hand = word.split('/')
                w, h = word_hand
                #print w,h
                if h == 'nr':    
                    #处理人名中包含的'·'
                    #print 'NR',w
                    if w.find('·') >= 0:
                        tmpArr = w.split('·')
                        for tmp in tmpArr:
                            save(fdtrain, fdtest, test, tmp, h, feature)
                    continue
                if h != 'm':
                    save(fdtrain, fdtest, test, w, h, feature)
            
                if h == 'w':
                    save(fdtrain, fdtest, test, "", "", feature)

        fdtrain.flush()
        fdtest.flush()

if __name__ == '__main__':    
    features = '6'
    convertFeature(features)
```
### 1.1 模板文件讲解
模板文件中的每一行代表一个template。每一个template中，专门的宏%x[row,col]用于确定输入数据中的一个token。row用于确定与当前的token的相对行数。col用于确定绝对行数。

6特征模板文件如下
```
# Unigram  
# 前一个字
U00:%x[-1,0] 
# 当前字
U01:%x[0,0]
# 后一个字
U02:%x[1,0] 
# 前一个字/当前字
U03:%x[-1,0]/%x[0,0]  
# 当前字/后一个字
U04:%x[0,0]/%x[1,0] 
# 前一个字/后一个字
U05:%x[-1,0]/%x[1,0]  
  
# Bigram  
B
```
## 2 训练
`crf_learn -f 3 -c 4.0 template people-daily.txt.utf8-feature6.train model`

## 3 测试与评估
`crf_test -m model people-daily.txt.utf8-feature6.test > test.rst`

评估脚本如下：
```
#!/usr/bin/python  
# -*- coding: utf-8 -*-  

#2016年 01月 20日 星期三 14:41:20 CST by Demobin

import sys  
 
filename = './test.rst'

fd = open(filename, 'r')
 
testCnt = 0  
goldCnt = 0  
crctCnt = 0  
flag = True  
  
for l in fd:  
    if l == '\n': continue  
  
    _, _, g, r = l.strip().split()
 
    if r != g: flag = False  
  
    if r in ('E', 'S'):  
        testCnt += 1  
        if flag: crctCnt +=1  
        flag = True  
  
    if g in ('E', 'S'): goldCnt += 1  

print 'Count of test:', testCnt  
print 'Count of gold:', goldCnt  
print 'Count of crct:', crctCnt  
```

* 查全率  
P = crctCnt/float(testCnt)  
* 查准率，召回率  
R = crctCnt/float(goldCnt)  
  
print 'P = %f, R = %f, F-score = %f' % (P, R, (2*P*R)/(P+R))
