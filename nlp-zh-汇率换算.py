#!/usr/bin/env python
#-*- coding: utf-8 -*-

#2016年 07月 13日 星期三 11:42:13 CST By Demobin

import re
import json
import urllib2
import handle_num as cnnum

normal_map = {
        u'智利披索': u'智利比索',
        u'巴拿马巴波亚': u'巴拿马巴尔博亚',
        }

names = {
	u'阿尔及利亚第纳尔': 'NGN',
	u'阿根廷比索': 'ARS',
	u'阿联酋迪拉姆': 'AED',
	u'阿曼里亚尔': 'OMR',
	u'埃及镑': 'EGP',
	u'爱尔兰镑': 'IEP',
	u'奥地利先令': 'ATS',
	u'澳大利亚元': 'AUD',
	u'澳门元': 'MOP',
	u'巴基斯坦卢比': 'PKR',
	u'巴拉圭瓜拉尼': 'PYG',
	u'巴林第纳尔': 'BHD',
	u'巴拿马巴尔博亚': 'PAB',
	u'巴西雷亚尔': 'BRL',
	u'百慕大元': 'BMD',
	u'保加利亚列弗': 'BGN',
	u'比利时法郎': 'BEF',
	u'冰岛克朗': 'ISK',
	u'波兰兹罗提': 'PLN',
	u'玻利维亚诺': 'BOB',
	u'博茨瓦纳普拉': 'BWP',
	u'丹麦克朗': 'DKK',
	u'德国马克': 'DEM',
	u'法国法郎': 'FRF',
	u'菲律宾比索': 'PHP',
	u'芬兰马克': 'FIM',
	u'港币': 'HKD',
	u'哥伦比亚比索': 'COP',
	u'古巴比索': 'CUP',
	u'哈萨克坚戈': 'KZT',
	u'韩元': 'KRW',
	u'荷兰盾': 'NLG',
	u'加拿大元': 'CAD',
	u'加纳塞地': 'GHC',
	u'捷克克朗': 'CZK',
	u'津巴布韦元': 'ZWD',
	u'卡塔尔里亚尔': 'QAR',
	u'科威特第纳尔': 'KWD',
	u'克罗地亚库纳': 'HRK',
	u'肯尼亚先令': 'KES',
	u'拉脱维亚拉图': 'LVL',
	u'老挝基普': 'LAK',
	u'黎巴嫩镑': 'LBP',
	u'立陶宛立特': 'LTL',
	u'林吉特': 'MYR',
	u'卢布': 'RUB',
	u'罗马尼亚列伊': 'RON',
	u'毛里求斯卢比': 'MUR',
	u'美元': 'USD',
	u'蒙古图格里克': 'MNT',
	u'孟加拉塔卡': 'BDT',
	u'秘鲁新索尔': 'PEN',
	u'缅甸缅元': 'BUK',
	u'摩洛哥迪拉姆': 'MAD',
	u'墨西哥比索': 'MXN',
	u'南非兰特': 'ZAR',
	u'挪威克朗': 'NOK',
	u'欧元': 'EUR',
	u'葡萄牙埃斯库多': 'PTE',
	u'人民币': 'CNH',
	u'日元': 'JPY',
	u'瑞典克朗': 'SEK',
	u'瑞士法郎': 'CHF',
	u'沙特里亚尔': 'SAR',
	u'斯里兰卡卢比': 'LKR',
	u'索马里先令': 'SOS',
	u'泰国铢': 'THB',
	u'坦桑尼亚先令': 'TZS',
	u'突尼斯第纳尔': 'TND',
	u'土耳其里拉': 'TRY',
	u'危地马拉格查尔': 'GTQ',
	u'委内瑞拉博利瓦': 'VEB',
	u'乌拉圭比索': 'UYU',
	u'西班牙比塞塔': 'ESP',
	u'希腊德拉克马': 'GRD',
	u'新加坡元': 'SGD',
	u'新台币': 'TWD',
	u'新西兰元': 'NZD',
	u'匈牙利福林': 'HUF',
	u'牙买加元': 'JMD',
	u'以色列谢克尔': 'ILS',
	u'意大利里拉': 'ITL',
	u'印度卢比': 'INR',
	u'印尼盾': 'IDR',
	u'英镑': 'GBP',
	u'约旦第纳尔': 'JOD',
	u'越南盾': 'VND',
	u'智利比索': 'CLP',
	}

headers = {'UserAgent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1', 'Referer': 'http://forex.hexun.com/rmbhl/'}

def code2name(code):
    for name in names:
        if names[name] == code:
            return name
    return None

def getjh():
    url = 'http://data.bank.hexun.com/other/cms/fxjhjson.ashx'
    opener = urllib2.build_opener()
    opener.addheaders = headers.items()
    try:
        rsp = opener.open(url).read()
    except:
        print('error: urllib2.urlopen(%s) failed'%(url))
        return results
    rsp = rsp.decode('gbk')
    rsp = re.findall('\[.*?\]', rsp)[0]
    rsp = re.sub('\'', '"', rsp)
    #print rsp
    rsp = re.sub('(currency|refePrice|code)', '"\g<1>"', rsp)
    #print rsp
    j = json.loads(rsp)
    for index, node in enumerate(j):
        j[index]['code'] = node['code'].strip()
        j[index]['refePrice'] = float(node['refePrice'].strip())
    return j

conj_dict = [
        u'是',
        u'有',
        u'等于',
        ]

ques_dict = [
        u'多少',
        u'几',
        ]

#统一转换为人民币进行计算
def convert(n, src, dst, j):
    for node in j:
        if node['currency'] == src:
            srcValue = n/(100.0/node['refePrice'])
            break
    for node in j:
        if node['currency'] == dst:
            dstValue = 100.0/node['refePrice'] * srcValue
            break
    return dstValue

def conv(text):
    #获取汇率
    j = getjh()
    #转中文转数字
    text = cnnum.cn_to_num(text)
    #同义词正规化
    for m in normal_map:
        text = re.sub(m, normal_map[m], text)
    #取出所有数值备用
    nums = re.findall('\d+\.\d+|\d+', text)
    if(len(nums)) != 1: return None
    num = nums[0]
    #按数值和的还有运算符进行切割
    currencys = [currency for currency in names]
    splits = re.split(u'(\d+\.\d+|\d+|' + u'|'.join(currencys) + '|' + u'|'.join(ques_dict) + '|' +u'|'.join(conj_dict) + ')', text)
    #去掉空值
    splits = [split for split in splits if len(split) != 0]
    currencys2 = []
    valid = True
    for split in splits:
        if split == num: continue
        if split in currencys:
            currencys2.append(split)
        elif split not in ques_dict and split not in conj_dict:
            valid = False
            break
    if valid == False or len(currencys2) != 2: return None

    src, dst = currencys2[0], currencys2[1]

    num = float(num)
    if int(num) != 0 and num % int(num) == 0.0:
        num = int(num)
    #print num, domain, src, dst
    return str(num) + src + '=' + str(convert(num, src, dst, j)) + dst

if __name__ == '__main__':
    print conv(u'一亿韩元哈哈是多少人民币')
