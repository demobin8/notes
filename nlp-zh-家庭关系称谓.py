#!/usr/bin/env python
#-*- coding: utf-8 -*-

#2016年 07月 13日 星期三 11:42:13 CST By Demobin

import re

#简写
relation_filter = [
    #表亲
    {#表亲的关系
        'exp':'^(.+)&o([^#]+)&l',
        'str':'\g<1>\g<2>'
    },
    {#表亲的关系
        'exp':'^(.+)&l([^#]+)&o',
        'str':'\g<1>\g<2>'
    },
    {#表亲的关系
        'exp':'(,[ds],(.+),[ds])&[ol]',
        'str':'\g<1>'
    },
    #父母
    {#母亲的丈夫是自己的父亲
        'exp':'m,h',
        'str':'f'
    },
    {#父亲的妻子是自己的母亲
        'exp':'f,w',
        'str':'m'
    },
    {#兄弟的父母就是自己的父母
        'exp':',[xol][sb](,[mf])',
        'str':'\g<1>'
    },
    #父母的子女
    {#父母的女儿年龄判断是哥哥还是弟弟
        'exp':',[mf],d&([ol])',
        'str':',\g<1>s'
    },
    {#父母的女儿年龄判断是姐姐还是妹妹
        'exp':',[mf],s&([ol])',
        'str':',\g<1>b'
    },
    {#如果自己是男性,父母的儿子是自己或者兄弟
        'exp':'^(.*)(,[fh]|[xol]b),[mf],s(.*)$',
        'str':'\g<1>\g<2>,xb\g<3>#\g<1>\g<2>\g<3>'
    },
    {#如果自己是女性,父母的女儿是自己或者姐妹
        'exp':'^(.*)(,[mw]|[xol]s),[mf],d(.*)$',
        'str':'\g<1>\g<2>,xs\g<3>#\g<1>\g<2>\g<3>'
    },
    {#如果自己是女性,父母的儿子是自己兄弟
        'exp':'(,[mw]|[xol]s),[mf],s',
        'str':'\g<1>,xb'
    },
    {#如果自己是男性,父母的女儿是自己姐妹
        'exp':'(,[fh]|[xol]b),[mf],d',
        'str':'\g<1>,xs'
    },
    {#父母的儿子是自己或兄弟
        #'exp':'^,[mf],s(.+)?$',
        'exp':'^,[mf],s(.*)$',
        'str':',1\g<1>#,xb\g<1>'
    },
    {#父母的女儿是自己或者姐妹
        #'exp':'^,[mf],d(.+)?$',
        'exp':'^,[mf],d(.*)$',
        'str':',0\g<1>#,xs\g<1>'
    },
    #兄弟姐妹
    {#哥哥姐姐的哥哥姐姐还是自己的哥哥姐姐(年龄判断)
        'exp':'(,o[sb])+(,o[sb])',
        'str':'\g<2>'
    },
    {#弟弟妹妹的弟弟妹妹还是自己的弟弟妹妹(年龄判断)
        'exp':'(,l[sb])+(,l[sb])',
        'str':'\g<2>'
    },
    {#如果自己是男性,兄弟姐妹的兄弟就是自己的兄弟或自己
        'exp':'^(.*)(,[fh1])(,[olx][sb])+,[olx]b(.*)$',
        'str':'\g<1>\g<2>,xb\g<4>#\g<1>\g<2>\g<4>'
    },
    {#如果自己是女性,兄弟姐妹的姐妹就是自己的姐妹或自己
        'exp':'^(.*)(,[mw0])(,[olx][sb])+,[olx]s(.*)$',
        'str':'\g<1>\g<2>,xs\g<4>#\g<1>\g<2>\g<4>'
    },
    {#如果自己是男性,兄弟姐妹的姐妹就是自己的姐妹
        'exp':'(,[fh1])(,[olx][sb])+,[olx]s',
        'str':'\g<1>,xs'
    },
    {#如果自己是女性,兄弟姐妹的兄弟就是自己的兄弟
        'exp':'(,[mw0])(,[olx][sb])+,[olx]b',
        'str':'\g<1>,xb'
    },
    {#不知道性别，兄弟姐妹的兄弟是自己或兄弟
        #'exp':'^,[olx][sb],[olx]b(.+)?$',
        'exp':'^,[olx][sb],[olx]b(.*)$',
        'str':'\g<1>#,xb\g<1>'
    },
    {#不知道性别，兄弟姐妹的姐妹是自己或姐妹
        #'exp':'^,[olx][sb],[olx]s(.+)?$',
        'exp':'^,[olx][sb],[olx]s(.*)$',
        'str':'\g<1>#,xs\g<1>'
    },
    {#将复合称谓拆分
        'exp':'^,x([sb])$',
        'str':',o\g<1>#,l\g<1>'
    },
    #孩子
    {#孩子的姐妹是自己的女儿(年龄判断)
        'exp':',[ds]&o,ob',
        'str':',s&o'
    },
    {#孩子的姐妹是自己的女儿(年龄判断)
        'exp':',[ds]&o,os',
        'str':',d&o'
    },
    {#孩子的兄弟是自己的儿子(年龄判断)
        'exp':',[ds]&l,lb',
        'str':',s&l'
    },
    {#孩子的兄弟是自己的儿子(年龄判断)
        'exp':',[ds]&l,ls',
        'str':',d&l'
    },
    {#孩子的姐妹是自己的女儿
        'exp':',[ds](&[ol])?,[olx]s',
        'str':',d'
    },
    {#孩子的兄弟是自己的儿子
        'exp':',[ds](&[ol])?,[olx]b',
        'str':',s'
    },
    #夫妻
    {#自己是女性，女儿或儿子的妈妈是自己
        'exp':'(,[mwd0](&[ol])?|[olx]s),[ds](&[ol])?,m',
        'str':'\g<1>'
    },
    {#自己是女性，女儿或儿子的爸爸是自己的丈夫
        'exp':'(,[mwd0](&[ol])?|[olx]s),[ds](&[ol])?,f',
        'str':'\g<1>,h'
    },
    {#自己是男性，女儿或儿子的爸爸是自己
        'exp':'(,[fhs1](&[ol])?|[olx]b),[ds](&[ol])?,f',
        'str':'\g<1>'
    },
    {#自己是男性，女儿或儿子的妈妈是自己的妻子
        'exp':'(,[fhs1](&[ol])?|[olx]b),[ds](&[ol])?,m',
        'str':'\g<1>,w'
    },
    {#不知道性别，子女的妈妈是自己或妻子
        #'exp':'^,[ds],m(.+)?$',
        'exp':'^,[ds],m(.*)$',
        'str':'\g<1>#,w\g<1>'
    },
    {#不知道性别，子女的爸爸是自己或丈夫
        #'exp':'^,[ds],f(.+)?$',
        'exp':'^,[ds],f(.*)$',
        'str':'\g<1>#,h\g<1>'
    },
    {#夫妻的孩子就是自己的孩子
        'exp':',[wh](,[ds])',
        'str':'\g<1>'
    },
    {#夫妻的对方是自己
        'exp':',w,h|,h,w',
        'str':''
    }
]

relation_title = {
    '':[u'自己',u'我'],
    #本家
    'f':[u'爸爸',u'爸', u'父亲',u'阿爸',u'老爸',u'老窦',u'爹',u'爹爹',u'爹地',u'爹啲',u'老爷子', u'家父', u'老父'],
    'f,f':[u'爷爷',u'祖父',u'阿爷',u'奶爷'],
    'f,f,f':[u'曾祖父',u'太爷',u'太爷爷',u'太公',u'祖公',u'祖奶爷'],
    'f,f,f,f':[u'高祖父',u'老太爷'],
    'f,f,f,f,ob':[u'伯高祖父'],
    'f,f,f,f,lb':[u'叔高祖父'],
    'f,f,f,m':[u'高祖母',u'老太太'],
    'f,f,f,ob':[u'伯曽祖父',u'曾伯祖父',u'伯公太'],
    'f,f,f,ob,w':[u'叔曽祖母',u'曾伯祖母',u'伯婆太'],
    'f,f,f,lb':[u'伯曽祖父',u'曾叔祖父',u'叔公太'],
    'f,f,f,lb,w':[u'叔曽祖母',u'曾叔祖母',u'叔婆太'],
    'f,f,f,xb,s&o':[u'堂伯祖父'],
    'f,f,f,xb,s&o,w':[u'堂伯祖母'],
    'f,f,f,xb,s&l':[u'堂叔祖父'],
    'f,f,f,xb,s&l,w':[u'堂叔祖母'],
    'f,f,f,xb,s,s&o':[u'从伯父'],
    'f,f,f,xb,s,s&o,w':[u'从伯母'],
    'f,f,f,xb,s,s&l':[u'从叔父'],
    'f,f,f,xb,s,s&l,w':[u'从叔母'],
    'f,f,f,xb,s,s,s&o':[u'族兄'],
    'f,f,f,xb,s,s,s&l':[u'族弟'],
    'f,f,f,xs':[u'太姑婆',u'姑婆太',u'曾祖姑母'],
    'f,f,f,xs,h':[u'太姑丈公',u'姑丈公太',u'曾祖姑丈'],
    'f,f,f,xs,s&o':[u'表伯祖父'],
    'f,f,f,xs,s&o,w':[u'表伯祖母'],
    'f,f,f,xs,s&l':[u'表叔祖父'],
    'f,f,f,xs,s&l,w':[u'表叔祖母'],
    'f,f,m':[u'曾祖母',u'太奶奶',u'太婆',u'祖婆',u'祖奶奶'],
    'f,f,m,xb':[u'太舅公',u'太舅爷'],
    'f,f,m,xb,w':[u'太舅婆'],
    'f,f,m,xb,s&o':[u'表伯祖父'],
    'f,f,m,xb,s&o,w':[u'表伯祖母'],
    'f,f,m,xb,s&l':[u'表叔祖父'],
    'f,f,m,xb,s&l,w':[u'表叔祖母'],
    'f,f,m,xs':[u'太姨奶',u'曾姨奶奶'],
    'f,f,m,xs,h':[u'太姨爷'],
    'f,f,m,xs,s&o':[u'表伯祖父'],
    'f,f,m,xs,s&o,w':[u'表伯祖母'],
    'f,f,m,xs,s&l':[u'表叔祖父'],
    'f,f,m,xs,s&l,w':[u'表叔祖母'],
    'f,f,xb':[u'堂祖父',u'x爷爷'],
    'f,f,xb,w':[u'堂祖母'],
    'f,f,xb,s&o':[u'堂伯',u'堂伯父'],
    'f,f,xb,s&o,w':[u'堂伯母'],
    'f,f,xb,s&l':[u'堂叔'],
    'f,f,xb,s,w':[u'堂婶',u'堂叔母',u'堂婶母'],
    'f,f,xb,s,s&o':[u'从兄',u'从兄弟'],
    'f,f,xb,s,s&o,w':[u'从嫂'],
    'f,f,xb,s,s&l':[u'从弟',u'从兄弟'],
    'f,f,xb,s,s&l,w':[u'从弟妹'],
    'f,f,xb,s,s,s':[u'从侄',u'从侄子'],
    'f,f,xb,s,s,s,w':[u'从侄媳妇'],
    'f,f,xb,s,s,s,s':[u'从侄孙'],
    'f,f,xb,s,s,s,d':[u'从侄孙女'],
    'f,f,xb,s,s,d':[u'从侄女'],
    'f,f,xb,s,s,d,h':[u'从侄女婿'],
    'f,f,xb,s,d&o':[u'从姐',u'从姐妹'],
    'f,f,xb,s,d&o,h':[u'从姐夫'],
    'f,f,xb,s,d&l':[u'从妹',u'从姐妹'],
    'f,f,xb,s,d&l,h':[u'从妹夫'],
    'f,f,xb,d':[u'堂姑'],
    'f,f,xb,d,h':[u'堂姑丈'],
    'f,f,ob':[u'伯祖父',u'伯公',u'大爷爷',u'大爷',u'堂祖父',u'伯爷爷',u'伯老爷'],
    'f,f,ob,w':[u'伯祖母',u'伯婆',u'大奶奶',u'堂祖母'],
    'f,f,lb':[u'叔祖父',u'叔公',u'小爷爷',u'堂祖父',u'叔爷爷',u'叔老爷'],
    'f,f,lb,w':[u'叔祖母',u'叔婆',u'小奶奶',u'堂祖母',u'叔奶奶'],
    'f,f,xs':[u'姑婆',u'姑祖母',u'祖姑母',u'姑奶奶'],
    'f,f,xs,h':[u'姑丈公',u'姑祖父',u'祖姑丈',u'姑爷爷',u'姑奶爷',u'姑老爷'],
    'f,f,xs,s&o':[u'表伯',u'表伯父'],
    'f,f,xs,s&o,w':[u'表伯母'],
    'f,f,xs,s&l':[u'表叔',u'表叔父'],
    'f,f,xs,s&l,w':[u'表婶',u'表叔母'],
    'f,f,xs,d':[u'表姑'],
    'f,f,xs,d,h':[u'表姑丈'],
    'f,m':[u'奶奶',u'祖母',u'阿嫲',u'嫲嫲'],
    'f,m,f':[u'曾外祖父',u'外太公'],
    'f,m,m':[u'曾外祖母',u'外太婆'],
    'f,m,xb':[u'舅公',u'舅老爷',u'舅爷爷',u'舅爷',u'舅祖',u'舅奶爷',u'舅祖父',u'太舅父'],
    'f,m,xb,w':[u'舅婆',u'舅奶奶',u'舅祖母',u'妗婆',u'太舅母'],
    'f,m,xb,s&o':[u'表伯',u'表伯父'],
    'f,m,xb,s&o,w':[u'表伯母'],
    'f,m,xb,s&l':[u'表叔',u'表叔父'],
    'f,m,xb,s&l,w':[u'表婶',u'表叔母'],
    'f,m,xb,d':[u'表姑'],
    'f,m,xb,d,h':[u'表姑丈'],
    'f,m,xs':[u'姨婆',u'姨奶奶',u'姨祖父'],
    'f,m,xs,h':[u'姨丈公',u'姨爷爷',u'姨祖母',u'姨爷',u'姨老爷',u'姨奶爷'],
    'f,m,xs,s&o':[u'表伯',u'表伯父'],
    'f,m,xs,s&o,w':[u'表伯母'],
    'f,m,xs,s&l':[u'表叔',u'表叔父'],
    'f,m,xs,s&l,w':[u'表婶',u'表叔母'],
    'f,m,xs,d':[u'表姑'],
    'f,m,xs,d,h':[u'表姑丈'],
    'f,xb,s&o':[u'堂哥',u'堂兄'],
    'f,xb,s&o,w':[u'堂嫂'],
    'f,xb,s&l':[u'堂弟'],
    'f,xb,s&l,w':[u'堂弟媳'],
    'f,xb,s,s':[u'堂侄',u'堂侄子'],
    'f,xb,s,s,w':[u'堂侄媳妇'],
    'f,xb,s,s,s':[u'堂侄孙'],
    'f,xb,s,s,s,w':[u'堂侄孙媳妇'],
    'f,xb,s,s,d':[u'堂侄孙女'],
    'f,xb,s,s,d,h':[u'堂侄孙女婿'],
    'f,xb,s,d':[u'堂侄女'],
    'f,xb,s,d,h':[u'堂侄女婿'],
    'f,xb,d&o':[u'堂姐'],
    'f,xb,d&o,h':[u'堂姐夫'],
    'f,xb,d&l':[u'堂妹'],
    'f,xb,d&l,h':[u'堂妹夫'],
    'f,xb,d,s':[u'堂外甥'],
    'f,xb,d,d':[u'堂外甥女'],
    'f,ob':[u'伯父',u'伯伯',u'大伯',u'x伯'],
    'f,ob,w':[u'伯母',u'大娘'],
    'f,lb':[u'叔叔',u'叔父',u'阿叔',u'叔',u'仲父',u'x叔'],
    'f,lb,w':[u'婶婶',u'婶母',u'阿婶',u'家婶',u'婶',u'季母'],
    #姑家
    'f,xs':[u'姑妈',u'姑母',u'姑姑',u'姑'],
    'f,xs,h':[u'姑丈',u'姑父',u'姑夫'],
    'f,xs,s&o':[u'表哥(姑家)',u'表哥'],
    'f,xs,s&o,w':[u'表嫂(姑家)',u'表嫂'],
    'f,xs,s&l':[u'表弟(姑家)',u'表弟'],
    'f,xs,s&l,w':[u'表弟媳(姑家)',u'表弟媳'],
    'f,xs,s,s':[u'表侄子'],
    'f,xs,s,s,s':[u'表侄孙'],
    'f,xs,s,s,s,w':[u'表侄孙媳妇'],
    'f,xs,s,s,d':[u'表侄孙女'],
    'f,xs,s,s,d,h':[u'表侄孙女婿'],
    'f,xs,s,d':[u'表侄女'],
    'f,xs,s,d,s':[u'外表侄孙'],
    'f,xs,s,d,s,w':[u'外表侄孙媳妇'],
    'f,xs,s,d,d':[u'外表侄孙女'],
    'f,xs,s,d,d,h':[u'外表侄孙女婿'],
    'f,xs,d&o':[u'表姐(姑家)',u'表姐'],
    'f,xs,d&o,h':[u'表姐夫(姑家)',u'表姐夫',u'表姐丈'],
    'f,xs,d&l':[u'表妹(姑家)',u'表妹'],
    'f,xs,d&l,h':[u'表妹夫(姑家)',u'表妹夫'],
    'f,xs,d,s':[u'表外甥'],
    'f,xs,d,d':[u'表外甥女'],
    'f,os':[u'姑母'],
    'f,ls':[u'姑姐'],
    #外家
    'm':[u'妈妈',u'妈', u'母亲',u'老妈',u'阿妈',u'老母',u'老妈子',u'娘',u'娘亲',u'妈咪'],
    'm,f':[u'外公',u'姥爷',u'阿公'],
    'm,f,f':[u'外曾祖父',u'外太祖父',u'太外祖父',u'太姥爷',u'外太公'],
    'm,f,f,xb':[u'外太伯公'],
    'm,f,f,xb,w':[u'外太伯母'],
    'm,f,f,xs':[u'外太姑婆'],
    'm,f,f,xs,h':[u'外太姑丈公'],
    'm,f,f,xs,s&o':[u'外表伯祖父'],
    'm,f,f,xs,s&o,w':[u'外表伯祖母'],
    'm,f,f,xs,s&l':[u'外表叔祖父'],
    'm,f,f,xs,s&l,w':[u'外表叔祖母'],
    'm,f,m':[u'外曾祖母',u'外太祖母',u'太外祖母',u'太姥姥',u'外太婆'],
    'm,f,m,xb':[u'外太舅公'],
    'm,f,m,xb,w':[u'外太舅母',u'外太舅婆'],
    'm,f,m,xs':[u'外太姨婆'],
    'm,f,m,xs,h':[u'外太姑姨公'],
    'm,f,xb':[u'小姥爷',u'x姥爷'],
    'm,f,xb,s':[u'堂舅',u'堂舅父'],
    'm,f,xb,s,w':[u'堂舅妈',u'堂舅母'],
    'm,f,xb,d':[u'堂姨'],
    'm,f,xb,d,h':[u'堂姨丈'],
    'm,f,ob':[u'外伯祖父',u'伯姥爷',u'大姥爷',u'外伯祖'],
    'm,f,ob,w':[u'外伯祖母',u'伯姥姥',u'大姥姥',u'外姆婆'],
    'm,f,lb':[u'外叔祖父',u'叔姥爷',u'小姥爷',u'外叔祖'],
    'm,f,lb,w':[u'外叔祖母',u'叔姥姥',u'小姥姥',u'外姆婆'],
    'm,f,xs':[u'外姑祖父',u'姑姥姥',u'外太姑母'],
    'm,f,xs,h':[u'外姑祖母',u'姑姥爷',u'外太姑父'],
    'm,f,xs,s':[u'表舅',u'表舅父'],
    'm,f,xs,s,w':[u'表舅妈',u'表舅母'],
    'm,f,xs,d':[u'表姨',u'表姨母',u'表姨妈',u'表阿姨'],
    'm,f,xs,d,h':[u'表姨丈',u'表姨父'],
    'm,m':[u'外婆',u'姥姥',u'阿婆'],
    'm,m,f':[u'外曾外祖父',u'外太外公',u'太姥爷'],
    'm,m,m':[u'外曾外祖母',u'外太外婆',u'太姥姥'],
    'm,m,xb':[u'外舅公',u'外舅祖父',u'舅姥爷',u'舅外祖父',u'舅外公',u'舅公'],
    'm,m,xb,w':[u'外舅婆',u'外舅祖母',u'舅姥姥'],
    'm,m,xb,s':[u'表舅',u'表舅父'],
    'm,m,xb,s,w':[u'表舅妈',u'表舅母'],
    'm,m,xb,d':[u'表姨',u'表姨母',u'表姨妈',u'表阿姨'],
    'm,m,xb,d,h':[u'表姨丈',u'表姨父'],
    'm,m,xs':[u'外姨婆',u'外姨祖母',u'姨姥姥',u'姨婆'],
    'm,m,xs,h':[u'外姨丈公',u'外姨祖父',u'姨姥爷'],
    'm,m,xs,s':[u'表舅',u'表舅父'],
    'm,m,xs,s,w':[u'表舅妈',u'表舅母'],
    'm,m,xs,d':[u'表姨',u'表姨母',u'表姨妈',u'表阿姨'],
    'm,m,xs,d,h':[u'表姨丈',u'表姨父'],
    #舅家
    'm,xb':[u'舅舅',u'舅父',u'舅',u'娘舅',u'舅仔',u'x舅'],
    'm,xb,w':[u'舅妈',u'舅母',u'妗妗',u'妗母',u'阿妗',u'x舅妈'],
    'm,xb,s&o':[u'表哥(舅家)',u'表哥'],
    'm,xb,s&o,w':[u'表嫂(舅家)',u'表嫂'],
    'm,xb,s&l':[u'表弟(舅家)',u'表弟'],
    'm,xb,s&l,w':[u'表弟媳(舅家)',u'表弟媳'],
    'm,xb,s,s':[u'表侄子'],
    'm,xb,s,s,s':[u'表侄孙'],
    'm,xb,s,s,s,w':[u'表侄孙媳妇'],
    'm,xb,s,s,d':[u'表侄孙女'],
    'm,xb,s,s,d,h':[u'表侄孙女婿'],
    'm,xb,s,d':[u'表侄女'],
    'm,xb,s,d,s':[u'外表侄孙'],
    'm,xb,s,d,s,w':[u'外表侄孙媳妇'],
    'm,xb,s,d,d':[u'外表侄孙女'],
    'm,xb,s,d,d,h':[u'外表侄孙女婿'],
    'm,xb,d&o':[u'表姐(舅家)',u'表姐'],
    'm,xb,d&o,h':[u'表姐夫(舅家)',u'表姐夫',u'表姐丈'],
    'm,xb,d&l':[u'表妹(舅家)',u'表妹'],
    'm,xb,d&l,h':[u'表妹夫(舅家)',u'表妹夫'],
    'm,xb,d,s':[u'表外甥'],
    'm,xb,d,d':[u'表外甥女'],
    'm,ob':[u'大舅'],
    'm,ob,w':[u'大舅妈'],
    'm,lb':[u'小舅',u'舅父仔'],
    'm,lb,w':[u'小舅妈'],
    #姨家
    'm,xs':[u'姨妈',u'姨母',u'姨姨',u'姨娘',u'阿姨',u'姨',u'x姨',u'x姨妈'],
    'm,xs,h':[u'姨丈',u'姨夫',u'姨父',u'x姨父'],
    'm,xs,s&o':[u'表哥(姨家)',u'表哥'],
    'm,xs,s&o,w':[u'表嫂(姨家)',u'表嫂'],
    'm,xs,s&l':[u'表弟(姨家)',u'表弟'],
    'm,xs,s&l,w':[u'表弟媳(姨家)',u'表弟媳'],
    'm,xs,s,s':[u'表侄子'],
    'm,xs,s,s,s':[u'表侄孙'],
    'm,xs,s,s,s,w':[u'表侄孙媳妇'],
    'm,xs,s,s,d':[u'表侄孙女'],
    'm,xs,s,s,d,h':[u'表侄孙女婿'],
    'm,xs,s,d':[u'表侄女'],
    'm,xs,s,d,s':[u'外表侄孙'],
    'm,xs,s,d,s,w':[u'外表侄孙媳妇'],
    'm,xs,s,d,d':[u'外表侄孙女'],
    'm,xs,s,d,d,h':[u'外表侄孙女婿'],
    'm,xs,d&o':[u'表姐(姨家)',u'表姐'],
    'm,xs,d&o,h':[u'表姐夫(姨家)',u'表姐夫',u'表姐丈'],
    'm,xs,d&l':[u'表妹(姨家)',u'表妹'],
    'm,xs,d&l,h':[u'表妹夫(姨家)',u'表妹夫'],
    'm,xs,d,s':[u'表外甥'],
    'm,xs,d,d':[u'表外甥女'],
    'm,os':[u'大姨',u'大姨妈'],
    'm,os,h':[u'大姨父',u'大姨丈',u'大姨夫'],
    'm,ls':[u'小姨',u'小姨妈',u'姨仔'],
    'm,ls,h':[u'小姨父',u'小姨丈',u'小姨夫'],
    #婆家
    'h':[u'老公',u'丈夫',u'先生',u'官人',u'男人',u'汉子',u'夫',u'夫君',u'爱人'],
    'h,f':[u'公公'],
    'h,f,f':[u'祖翁'],
    'h,f,f,f':[u'太公翁'],
    'h,f,f,m':[u'太奶亲'],
    'h,f,m':[u'祖婆'],
    'h,f,ob':[u'伯翁'],
    'h,f,ob,w':[u'伯婆'],
    'h,f,lb':[u'叔翁'],
    'h,f,lb,w':[u'叔婆'],
    'h,f,xb,s&o':[u'堂大伯',u'堂兄'],
    'h,f,xb,s&o,w':[u'堂嫂'],
    'h,f,xb,s&l':[u'堂叔仔',u'堂弟'],
    'h,f,xb,s&l,w':[u'堂小弟'],
    'h,m':[u'婆婆'],
    'h,m,xb':[u'舅公'],
    'h,m,xb,w':[u'舅婆'],
    'h,m,xs':[u'姨婆'],
    'h,m,xs,h':[u'姨公'],
    'h,xb,s':[u'侄子',u'侄儿'],
    'h,xb,s,w':[u'侄媳',u'侄媳妇'],
    'h,xb,s,s':[u'侄孙',u'侄孙子'],
    'h,xb,s,s,w':[u'侄孙媳'],
    'h,xb,s,d':[u'侄孙女'],
    'h,xb,s,d,h':[u'侄孙女婿'],
    'h,xb,d':[u'侄女'],
    'h,xb,d,h':[u'侄女婿',u'侄婿'],
    'h,xb,d,s':[u'外侄孙'],
    'h,xb,d,s,w':[u'外侄媳妇'],
    'h,xb,d,d':[u'外侄孙女'],
    'h,xb,d,d,h':[u'外侄孙女婿'],
    'h,ob':[u'大伯子',u'大伯哥',u'夫兄'],
    'h,ob,w':[u'大婶子',u'大伯嫂',u'大伯妇',u'伯娘',u'大伯娘',u'大嫂',u'夫兄嫂',u'妯娌'],
    'h,lb':[u'小叔子',u'小叔弟'],
    'h,lb,w':[u'小婶子',u'小叔妇',u'小叔媳妇',u'妯娌'],
    'h,xs,s':[u'外甥'],
    'h,xs,s,w':[u'外甥媳妇'],
    'h,xs,s,s':[u'外甥孙'],
    'h,xs,s,s,w':[u'外甥孙媳妇'],
    'h,xs,s,s,s':[u'外曾甥孙'],
    'h,xs,s,s,d':[u'外曾甥孙女'],
    'h,xs,s,d':[u'外甥孙女'],
    'h,xs,s,d,h':[u'外甥孙女婿'],
    'h,xs,s,d,s':[u'外曾甥孙'],
    'h,xs,s,d,d':[u'外曾甥孙女'],
    'h,xs,d':[u'外甥女'],
    'h,xs,d,h':[u'外甥女婿'],
    'h,xs,d,s':[u'外甥孙'],
    'h,xs,d,s,w':[u'外甥孙媳妇'],
    'h,xs,d,s,s':[u'外曾甥孙'],
    'h,xs,d,s,d':[u'外曾甥孙女'],
    'h,xs,d,d':[u'外甥孙女'],
    'h,xs,d,d,h':[u'外甥孙女婿'],
    'h,xs,d,d,s':[u'外曾甥孙'],
    'h,xs,d,d,d':[u'外曾甥孙女'],
    'h,os':[u'大姑子',u'大姑',u'大娘姑'],
    'h,os,h':[u'大姑夫',u'姊丈',u'大姑姐夫'],
    'h,ls':[u'小姑子',u'小姑',u'姑仔'],
    'h,ls,h':[u'小姑夫',u'小姑妹夫'],
    #岳家
    'w':[u'老婆',u'妻子',u'太太',u'媳妇',u'夫人',u'女人',u'婆娘',u'妻',u'内人',u'娘子',u'爱人', u'爱妻', u'贱内'],
    'w,f':[u'岳父',u'老丈人',u'丈人',u'泰山',u'妻父'],
    'w,f,f':[u'太岳父'],
    'w,f,f,ob':[u'太伯岳'],
    'w,f,f,ob,w':[u'太伯岳母'],
    'w,f,f,lb,u':[u'太叔岳'],
    'w,f,f,lb,w':[u'太叔岳母'],
    'w,f,f,xb,s&o':[u'姻伯'],
    'w,f,f,xb,s&o,w':[u'姻姆'],
    'w,f,f,xb,s&l':[u'姻叔'],
    'w,f,f,xb,s&l,w':[u'姻婶'],
    'w,f,f,xs':[u'太姑岳母'],
    'w,f,f,xs,h':[u'太姑岳父'],
    'w,f,m':[u'太岳母'],
    'w,f,m,xb':[u'太舅岳父'],
    'w,f,m,xb,w':[u'太舅岳母'],
    'w,f,m,xs':[u'太姨岳母'],
    'w,f,m,xs,h':[u'太姨岳父'],
    'w,f,xb,s&o':[u'堂大舅',u'姻家兄'],
    'w,f,xb,s&l':[u'堂舅仔',u'姻家弟'],
    'w,f,xb,d&o':[u'堂大姨'],
    'w,f,xb,d&l':[u'堂姨仔'],
    'w,f,ob':[u'伯岳',u'伯岳父'],
    'w,f,ob,w':[u'伯岳母'],
    'w,f,lb':[u'叔岳',u'叔岳父'],
    'w,f,lb,w':[u'叔岳母'],
    'w,f,xs':[u'姑岳母'],
    'w,f,xs,s&o':[u'表大舅'],
    'w,f,xs,s&l':[u'表舅仔'],
    'w,f,xs,d&o':[u'表大姨'],
    'w,f,xs,d&l':[u'表姨仔'],
    'w,m':[u'岳母',u'丈母娘'],
    'w,m,f':[u'外太岳父'],
    'w,m,m':[u'外太岳母'],
    'w,m,xb':[u'舅岳父'],
    'w,m,xb,w':[u'舅岳母'],
    'w,m,xb,s&o':[u'表大舅'],
    'w,m,xb,s&l':[u'表舅仔'],
    'w,m,xb,d&o':[u'表大姨'],
    'w,m,xb,d&l':[u'表姨仔'],
    'w,m,xs':[u'姨岳母'],
    'w,m,xs,h':[u'姨岳父'],
    'w,m,xs,s&o':[u'表大舅'],
    'w,m,xs,s&l':[u'表舅仔'],
    'w,m,xs,d&o':[u'表大姨'],
    'w,m,xs,d&l':[u'表姨仔'],
    'w,xb,s':[u'内侄',u'妻侄'],
    'w,xb,s,w':[u'内侄媳妇'],
    'w,xb,s,s':[u'侄孙'],
    'w,xb,s,s,w':[u'侄孙媳妇'],
    'w,xb,s,d':[u'侄孙女'],
    'w,xb,s,d,h':[u'侄孙女婿'],
    'w,xb,d':[u'内侄女',u'妻侄女'],
    'w,xb,d,h':[u'内侄女婿'],
    'w,xb,d,s':[u'外侄孙'],
    'w,xb,d,s,w':[u'外侄孙媳妇'],
    'w,xb,d,d':[u'外侄孙女'],
    'w,xb,d,d,h':[u'外侄孙女婿'],
    'w,ob':[u'大舅哥',u'大舅子',u'内兄'],
    'w,ob,w':[u'舅嫂',u'大舅妇',u'大舅媳妇',u'大妗子',u'内嫂'],
    'w,lb':[u'小舅子',u'内弟'],
    'w,lb,w':[u'舅弟媳',u'小舅妇',u'小舅媳妇',u'小妗子'],
    'w,xs,s':[u'姨甥',u'妻外甥'],
    'w,xs,s,w':[u'姨甥媳妇'],
    'w,xs,s,s':[u'姨甥孙'],
    'w,xs,s,s,w':[u'姨甥孙媳妇'],
    'w,xs,s,d':[u'姨甥孙女'],
    'w,xs,s,d,h':[u'姨甥孙女婿'],
    'w,xs,d':[u'姨甥女',u'妻外甥女'],
    'w,xs,d,h':[u'姨甥女婿'],
    'w,xs,d,s':[u'姨甥孙'],
    'w,xs,d,s,w':[u'姨甥孙媳妇'],
    'w,xs,d,d':[u'姨甥孙女'],
    'w,xs,d,d,h':[u'姨甥孙女婿'],
    'w,os':[u'大姨子',u'大姨姐',u'妻姐'],
    'w,os,h':[u'大姨夫',u'大姨姐夫',u'襟兄',u'连襟'],
    'w,ls':[u'小姨子',u'小姨姐',u'妻妹',u'小妹儿'],
    'w,ls,h':[u'小姨夫',u'小姨妹夫',u'襟弟',u'连襟'],
    #旁支
    'xb':[u'兄弟'],
    'xb,w,f':[u'姻世伯',u'亲家爷',u'亲爹',u'亲伯'],
    'xb,w,m':[u'姻伯母',u'亲家娘',u'亲娘'],
    'xb,s':[u'侄子',u'侄儿'],
    'xb,s,w':[u'侄媳',u'侄媳妇'],
    'xb,s,s':[u'侄孙',u'侄孙子'],
    'xb,s,s,w':[u'侄孙媳'],
    'xb,s,s,s':[u'侄曾孙'],
    'xb,s,s,d':[u'侄曾孙女'],
    'xb,s,d':[u'侄孙女'],
    'xb,s,d,h':[u'侄孙女婿'],
    'xb,d':[u'侄女'],
    'xb,d,h':[u'侄女婿'],
    'xb,d,s':[u'外侄孙',u'外侄孙子'],
    'xb,d,s,w':[u'外侄孙媳妇'],
    'xb,d,d':[u'外侄孙女'],
    'xb,d,d,h':[u'外侄孙女婿'],
    'ob':[u'哥哥',u'哥',u'兄',u'阿哥',u'大哥',u'大佬',u'老哥', u'家兄'],
    'ob,w':[u'嫂子',u'大嫂',u'嫂',u'阿嫂'],
    'ob,w,f':[u'姻伯父'],
    'ob,w,m':[u'姻伯母'],
    'lb':[u'弟弟',u'弟',u'细佬',u'老弟', u'舍弟'],
    'lb,w':[u'弟妹',u'弟媳',u'弟媳妇'],
    'lb,w,f':[u'姻叔父'],
    'lb,w,m':[u'姻叔母'],
    'xs':[u'姐妹'],
    'xs,h,f':[u'姻世伯',u'亲家爷',u'亲爹',u'亲伯'],
    'xs,h,m':[u'姻伯母',u'亲家娘',u'亲娘'],
    'xs,s':[u'外甥'],
    'xs,s,w':[u'外甥媳妇'],
    'xs,s,s':[u'外甥孙'],
    'xs,s,s,w':[u'外甥孙媳妇'],
    'xs,s,s,s':[u'外曾甥孙'],
    'xs,s,s,d':[u'外曾甥孙女'],
    'xs,s,d':[u'外甥孙女'],
    'xs,s,d,h':[u'外甥孙女婿'],
    'xs,s,d,s':[u'外曾甥孙'],
    'xs,s,d,d':[u'外曾甥孙女'],
    'xs,d':[u'外甥女'],
    'xs,d,h':[u'外甥女婿'],
    'xs,d,s':[u'外甥孙'],
    'xs,d,s,w':[u'外甥孙媳妇'],
    'xs,d,s,s':[u'外曾甥孙'],
    'xs,d,s,d':[u'外曾甥孙女'],
    'xs,d,d':[u'外甥孙女'],
    'xs,d,d,h':[u'外甥孙女婿'],
    'xs,d,d,s':[u'外曾甥孙'],
    'xs,d,d,d':[u'外曾甥孙女'],
    'os':[u'姐姐',u'姐',u'家姐',u'阿姐',u'阿姊', u'家姐'],
    'os,h':[u'姐夫',u'姊夫',u'姊婿'],
    'ls':[u'妹妹',u'妹',u'老妹', u'舍妹'],
    'ls,h':[u'妹夫',u'妹婿'],
    #自家
    's':[u'儿子',u'仔',u'阿仔',u'仔仔', u'爱子', u'犬子'],
    's,w':[u'儿媳妇',u'儿媳'],
    's,w,xb':[u'姻侄'],
    's,w,xs':[u'姻侄女'],
    's,s':[u'孙子'],
    's,s,w':[u'孙媳妇',u'孙媳'],
    's,s,s':[u'曾孙'],
    's,s,s,w':[u'曾孙媳妇'],
    's,s,s,s':[u'玄孙',u'元孙',u'膀孙'],
    's,s,s,d':[u'玄孙女'],
    's,s,s,s,s':[u'来孙'],
    's,s,d':[u'曾孙女'],
    's,s,d,h':[u'曾孙女婿'],
    's,s,d,s':[u'外玄孙'],
    's,s,d,d':[u'外玄孙女'],
    's,d':[u'孙女'],
    's,d,h':[u'孙女婿'],
    's,d,s':[u'曾外孙'],
    's,d,d':[u'曾外孙女'],
    'd':[u'女儿',u'千金',u'女',u'阿女',u'女女',u'掌上明珠', u'爱女', u'闺女'],
    'd,h':[u'女婿',u'女婿子',u'女婿儿'],
    'd,h,xb':[u'姻侄'],
    'd,h,xs':[u'姻侄女'],
    'd,s':[u'外孙'],
    'd,s,w':[u'外孙媳'],
    'd,s,s':[u'外曾孙',u'重外孙'],
    'd,s,d':[u'外曾孙女',u'重外孙女'],
    'd,d':[u'外孙女'],
    'd,d,h':[u'外孙女婿'],
    'd,d,s':[u'外曾外孙'],
    'd,d,d':[u'外曾外孙女'],
    #亲家
    's,w,m':[u'亲家母'],
    's,w,f':[u'亲家公',u'亲家翁'],
    's,w,f,f':[u'太姻翁'],
    's,w,f,m':[u'太姻姆'],
    's,w,f,ob':[u'姻兄'],
    's,w,f,lb':[u'姻弟'],
    'd,h,m':[u'亲家母'],
    'd,h,f':[u'亲家公',u'亲家翁'],
    'd,h,f,f':[u'太姻翁'],
    'd,h,f,m':[u'太姻姆'],
    'd,h,f,ob':[u'姻兄'],
    'd,h,f,lb':[u'姻弟'],
    #未知
    'x':[u'孩子', u'后代']
}

def getAllTitle():
    ranges = [u'二', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三']
    titles = []
    for rel in relation_title:
        for title in relation_title[rel]:
            if title not in titles and title.find('(') == -1:
                if title.startswith('x'):
                    for n in ranges:
                        if title not in titles:
                            titles.append(n + title[1:])
                else:
                    if len(title) != 1:
                        titles.append(title)

    titles.remove(u'自己')
    titles.remove(u'女人')
    titles.remove(u'男人')

    extras = [u'长子', u'次子']

    titles.extend(extras)

    return titles

def unique(arr):
    rst = []
    hash = {}
    for elem in arr:
        if not hash.get(elem):
            rst.append(elem)
            hash[elem] = True
    return rst

def getSelect(text):
    text = re.sub(u'[二|三|四|五|六|七|八|九|十]{1,2}', 'x', text)
    splits = text.split(u'的')
    rst = []
    match = True
    length = len(splits)
    for index, split in enumerate(splits):
        name = split
        arr = []
        has = False
        
        for title in relation_title:
            if name in relation_title[title]:
                if title != '' or index == length - 1:
                    arr.append(title)
                has = True

        if has == False: match = False

        if len(rst) != 0:
            res = []
            for i in range(len(rst)):
                for j in range(len(arr)):
                    res.append(rst[i] + ',' + arr[j])
            rst = res
        else:
            for i in range(len(arr)):
                rst.append(',' + arr[i])

    return match and rst or []

def select2id(selector, sex):
    rst = []
    hash = {}
    sex2 = -1
    restr = ',([mw]|[olx]s|d(&[ol])?)$'
    r = re.compile(restr)
    sex2 = not r.search(selector) and 1 or 0
    
    def getid(selector):
        s = ''
        if not hash.get(selector):
            hash[selector] = True
            status = True
            while 1:
                s = selector
                for tmp in relation_filter:
                    selector = re.sub(tmp['exp'], tmp['str'], selector)
                    if selector.find('#') > -1:
                        arr = selector.split('#')
                        for i in range(len(arr)):
                            getid(arr[i])
                        status = False
                        break
                if s == selector: break
            if status:
                selector = re.sub(',[01]', '', selector)[1:]
                if selector == '' and sex > -1 and sex != sex2: pass
                else: rst.append(selector)

    getid(selector)
    return rst

def reverseId(id, sex):
    hash = {
        'f':    ['d','s'],
        'm':    ['d','s'],
        'h':    ['w',''],
        'w':    ['','h'],
        's':    ['m','f'],
        'd':    ['m','f'],
        'lb':   ['os','ob'],
        'ob':   ['ls','lb'],
        'xb':   ['xs','xb'],
        'ls':   ['os','ob'],
        'os':   ['ls','lb'],
        'xs':   ['xs','xb']
    }
    
    age = '';
    if(id.find('&o') > -1): age = '&l'
    elif(id.find('&l') > -1): age = '&o'
    
    if(id):
        id = re.sub('&[ol]', '', id)
        sex = sex and 1 or 0
        tmp = re.sub(',[fhs]|,[olx]b', ',1', ',' + str(sex) + ','+ id)
        sid = re.sub(',[mwd]|,[olx]s', ',0', tmp)
        sid = sid[0:sid.rfind(',')]
        id_arr = id.split(',')
        id_arr.reverse()
        sid_arr = sid.split(',')
        sid_arr.reverse()
        arr = []
        for i in range(len(id_arr)):
            arr.append(hash[id_arr[i]][int(sid_arr[i])])
        return ','.join(arr) + age

    return ''

def getDataById(id):
    rst = []
    flt = '&[olx]'
    for title in relation_title:
        if re.sub(flt, '', title) == id:
    	    rst.append(relation_title[title])
    return rst

def getChainById(id):
    arrs = id.split(',')
    items = []
    for arr in arrs:
        key = re.sub('&[ol]', '', arr)
        items.append(relation_title[key][0])
    return u'的'.join(items)

#sex=1默认为男性0为女性
#kind=chain表示查询关系，其它表示查询称呼
#reverse=False表示查询我如何称呼对方，True表示查询别人如何称呼我
def relationship(text, sex=1, kind='chain', reverse=False):
    print text
    selectors = getSelect(text)
    rst = []
    for i in range(len(selectors)):
        ids = select2id(selectors[i], sex)
        for id in ids:
            if kind == 'chain':
                data = getChainById(id)
                if data: rst.append(data)
            else:
                if reverse:
                    id = reverseId(id, sex)
                if relation_title.get(id):
                    rst.append(relation_title[id][0])
                else:
                    data = getDataById(id)
                    if len(data) == 0:
                        id = re.sub('&[ol]', '', id)
                        data = getDataById(id)
                    if len(data) == 0:
                        id = re.sub('[ol]', 'x', id)
                        data = getDataById(id)
                    if len(data) == 0:
                        l = re.sub('x', 'l', id)
                        data = getDataById(l)
                        o = re.sub('x','o', id)
                        data.extend(getDataById(o))
                    for j in range(len(data)):
                        rst.append(data[j][0])

    rst = unique(rst)
    if len(rst) == 0: rst.append(u'貌似对方和你似乎不是很熟~')
    return rst

def testRelationship():
#    rst = relationship(u'爸爸的妈妈的老公的儿子的女儿')
#    print ';'.join(rst)
#    rst = relationship(u'我的阿爸的妈咪的孙子')
#    print ';'.join(rst)
#    rst = relationship(u'老公的老婆的儿子的爸爸的老婆的儿子的爸爸')
#    print ';'.join(rst)
    rst = relationship(u'我的三舅的儿子的爸爸的妹妹的儿子的叔叔的哥哥')
    print ';'.join(rst)
#    rst = relationship(u'老婆的外孙的姥姥')
#    print ';'.join(rst)
#    rst = relationship(u'大姨的女儿的表哥')
#    print ';'.join(rst)

if __name__ == '__main__':
    ts = getAllTitle()
    print '/'.join(ts)
