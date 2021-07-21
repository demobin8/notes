#!/usr/bin/python3
#-*- coding: utf-8 -*-

#2016年 12月 18日 星期日 12:21:52 CST by Demobin

import ply.lex as Lex

from dictionary import Dictionary

dictionary = Dictionary('./dictionary.json')

#POS标注集关键字
pos_keywords = [
        '标点',
        '名词',
        '未知'
        ] + dictionary.tagset

feature_keywords = [
        '词语',
        ] + list(dictionary.attrs.keys())

#短语规则名称
grammar_keywords = {
        '名词短语':     'NP',
        '形容词短语':   'AP',
        '动词短语':     'VP',
        '主谓短语':     'DJ',
        '数词短语':     'MCP',
        '处所词短语':   'SP',
        '时间词短语':   'TP',
        '副词短语':     'DP',
        '介词短语':     'PP',
        '数量短语':     'MP',
        }

reserved_keywords = {
        }

reserved = dict(reserved_keywords)

# List of token names.   This is always required
tokens = [
   #--*--星号
   'ASTERISK',
   #--(--左圆括号
   'LBRACKET',
   #--)--右园括号
   'RBRACKET',
   #--<--左尖括号
   'LANGLE',
   #-->--右尖括号
   'RANGLE',
   #--[--左方括号
   'LSQUARE',
   #--]--右方括号
   'RSQUARE',
   #--$--美元符号
   'DOLLAR',
   #--:--冒号
   'COLON',
   #--%--百分号
   'PERCENT',
   #--,--逗号
   'COMMA',
   #--|--竖线
   'VERTICAL',
   #--?--问号
   'QUESTION',
   #--#--注释
   'COMMENT',
   #--!--感叹号
   'EXCLAMATION',
   #-----减号
   'MINUS',
   #--=--等号
   'EQUAL',
   #数字
   'NUMBER',
   #词性
   'POS',
   'GRAMMAR',
   'FEATURE',
   #文本字符串
   'TEXT',
] + list(reserved.keys())

# Regular expression rules for simple tokens
t_ASTERISK      = r'\*'
t_LBRACKET      = r'\('
t_RBRACKET      = r'\)'
t_LANGLE        = r'\<'
t_RANGLE        = r'\>'
t_LSQUARE       = r'\['
t_RSQUARE       = r'\]'
t_DOLLAR        = r'\$'
t_COLON         = r':'
t_PERCENT       = r'%'
t_COMMA         = r','
t_VERTICAL      = r'\|'
t_QUESTION      = r'\?'
t_EXCLAMATION   = r'!'
t_MINUS         = r'-'
t_EQUAL         = r'='

#注释
def t_COMMENT(t):
    r"[ ]*\043[^\n]*"
    #r'\#.*'
    pass

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_POS(t):
    return t
t_POS.__doc__ = r'|'.join(pos_keywords)

def t_FEATURE(t):
    return t
t_FEATURE.__doc__ = r'|'.join(feature_keywords)

def t_GRAMMAR(t):
    return t
t_GRAMMAR.__doc__ = r'|'.join(grammar_keywords.values())

def t_TEXT(t):
    r'\w+'
    t.type = reserved.get(t.value, 'TEXT')
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = Lex.lex(debug=True)
