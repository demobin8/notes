#-*- coding: utf-8 -*-

#2016年 12月 16日 星期五 12:01:50 CST by Demobin

import regex as re

word2numdict = {
        u'零':   0,
        u'0':    0,
        u'一':   1,
        u'1':    1,
        u'01':   1,
        u'二':   2,
        u'两':   2,
        u'2':    2,
        u'02':   2,
        u'三':   3,
        u'3':    3,
        u'03':   3,
        u'四':   4,
        u'4':    4,
        u'04':   4,
        u'五':   5,
        u'5':    5,
        u'05':   5,
        u'六':   6,
        u'6':    6,
        u'06':   6,
        u'七':   7,
        u'天':   7,
        u'日':   7,
        u'末':   7,
        u'7':    7,
        u'07':   7,
        u'八':   8,
        u'8':    8,
        u'08':   8,
        u'九':   9,
        u'9':    9,
        u'09':   9,
        }
def word2num(text):
    return word2numdict.get(text, 0)

word2numdict2 = [
            u'十',
            u'百',
            u'千',
            u'万',
            u'十万',
            u'百万',
            u'千万',
            u'亿',
            ]
def word2num2(text):
    return 10 * 10 ** word2numdict2.index(text)

def zh2num(text):

    def repl(match):
        num = 0
        #百万和十万不做单位
        #words = re.split(u'(亿|千万|百万|十万|万|千|百|十)', match.group())
        words = re.split(u'(亿|千万|万|千|百|十)', match.group())
        base = word2num2(words[1])
        #处理三百十二的说法
        if words[1] == u'十':
            if words[0] == '' or word2num(words[0]) == 0:
                num += base
            else:
                num += word2num(words[0]) * base
            num += word2num(words[2])
        else:
            if re.match('\d+', words[0]):
                #支持小数点
                if words[0].find('.') != -1:
                    l = int(float(words[0]) * base)
                else:
                    l = int(words[0]) * base
            else:
                l = word2num(words[0])  * base

            if re.match('\d+', words[2]):
                #处理3万3的说法
                if len(words[2]) == 1:
                    r = int(words[2]) * base/10
                else:
                    r = int(words[2]) 
            else:
                r = word2num(words[2]) * base/10
            num += l + r
        
        return str(num)

    regex = re.compile(u'[一二两三四五六七八九123456789]亿[一二两三四五六七八九123456789](?!(万|千|百|十))')
    text = regex.sub(repl, text)

    regex = re.compile(u'[一二两三四五六七八九123456789]万[一二两三四五六七八九123456789](?!(千|百|十))')
    text = regex.sub(repl, text)

    regex = re.compile(u'[一二两三四五六七八九123456789]千[一二两三四五六七八九123456789](?!(百|十))')
    text = regex.sub(repl, text)
		
    regex = re.compile(u'[一二两三四五六七八九123456789]百[一二两三四五六七八九123456789](?!十)')
    text = regex.sub(repl, text)

    def repl2(match):
        return str(word2num(match.group()))
    regex = re.compile(u'[零一二两三四五六七八九]')
    text = regex.sub(repl2, text)

    regex = re.compile(u'点(?=([0-9]?(万|千万|亿)))')
    text = regex.sub('.', text)

    #FIXME:这里，用原生的re模块有一个bug
    #原生re模块要求look-behind条件长度必须一致
    #也就是说用(周|星)没错都两个字的长度，但(周|星期)就报错了
    regex = re.compile(u'(?<=(周|星期))[末天日]')
    text = regex.sub(repl2, text)

    regex = re.compile(u'(?<!(周|星期))0?[0-9]?十[0-9]?')
    text = regex.sub(repl, text)

    regex = re.compile(u'0?[1-9]百[0-9]?[0-9]?(?!万)')
    text = regex.sub(repl, text)

    regex = re.compile(u'0?[1-9]千[0-9]?[0-9]?[0-9]?(?!万)')
    text = regex.sub(repl, text)

    regex = re.compile(u'([0-9]+|[0-9]+.[0-9]+)万[0-9]?[0-9]?[0-9]?[0-9]?')
    text = regex.sub(repl, text)

    #不会有这个表达
    #regex = re.compile(u'([0-9]+|[0-9]+.[0-9]+)十万[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?')
    #text = regex.sub(repl, text)

    #regex = re.compile(u'([0-9]+|[0-9]+.[0-9]+)百万[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?')
    #text = regex.sub(repl, text)

    regex = re.compile(u'([0-9]+|[0-9]+.[0-9]+)千万[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?')
    text = regex.sub(repl, text)

    regex = re.compile(u'([0-9]+|[0-9]+.[0-9]+)亿[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?')
    text = regex.sub(repl, text)

    return text

if __name__ == '__main__':
    print(zh2num(u"三万零三"))
    print(zh2num(u"3万3"))
    print(zh2num(u"十九万三千八"))
    print(zh2num(u'三点一四一五'))
    print(zh2num(u'一千二'))
    print(zh2num(u'118.2千万零2百'))
    print(zh2num(u'118.2亿'))
    print(zh2num(u'三十四点七万'))
    print(zh2num(u'一千零十'))
    print(zh2num(u'一千十'))
    print(zh2num(u'19万零3百'))
    print(zh2num(u'一万三百二十'))
    print(zh2num(u'一九九八.四.五'))
    print(zh2num(u'一九九八点二五'))
    print(zh2num(u'二十亿年前，中国只有不到三十万人'))
    print(zh2num(u"19万3千8"))
    print(zh2num(u"3点半"))
    print(zh2num(u"三点二十"))
    print(zh2num(u"3点20"))
