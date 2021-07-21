#-*- coding: utf-8 -*-

#2016年 12月 15日 星期四 09:13:16 CST by Demobin

import fire
import time
import datetime
import zhnum
import calendar
import regex as re

#原生re模块不能支持超过100的group
time_restr  = u'((前|昨|今|明|后)(天|日)?(早|晚)(晨|上|间)?)'
time_restr += u'|(\\d+个?[年月日天][以之]?[前后])'
time_restr += u'|(\\d+个?半?(小时|钟头|h|H|秒钟|秒|分钟|分)(半)?[以之]?[前后]?)'
time_restr += u'|(半个?(小时|钟头))'
time_restr += u'|(\\d+(分钟|min))'
time_restr += u'|([13]刻钟)'
time_restr += u'|((上|这|本|下)+(周|星期)([一二三四五六七天日]|[1-7])?)'
time_restr += u'|((周|星期)([一二三四五六七天日]|[1-7]))'
time_restr += u'|((早|晚)?([0-2]?[0-9](点|时)半)(am|AM|pm|PM)?)'
time_restr += u'|((早|晚)?(\\d+[:：]\\d+([:：]\\d+)*)\\s*(am|AM|pm|PM)?)'
time_restr += u'|((早|晚)?([0-2]?[0-9](点|时)[13一三]刻)(am|AM|pm|PM)?)'
time_restr += u'|((早|晚)?(\\d+[时点](\\d+)?分?(\\d+秒?)?)\\s*(am|AM|pm|PM)?)'
time_restr += u'|(大+(前|后)天)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)世)'
time_restr += u'|([0-9]?[0-9]?[0-9]{2}\\.((10)'
time_restr += u'|(11)'
time_restr += u'|(12)'
time_restr += u'|([1-9]))\\.((?<!\\\\d))([0-3][0-9]|[1-9]))'
time_restr += u'|(现在)'
#time_restr += u'|(届时)'
time_restr += u'|(这个月)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)日)'
#time_restr += u'|(晚些时候)'
time_restr += u'|(今年)'
#time_restr += u'|(长期)'
#time_restr += u'|(以前)'
#time_restr += u'|(过去)'
#time_restr += u'|(时期)'
#time_restr += u'|(时代)'
#time_restr += u'|(当时)'
#time_restr += u'|(近来)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)夜)'
time_restr += u'|(当前)'
time_restr += u'|(日(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|((\\d+)点)'
time_restr += u'|(今年([零一二三四五六七八九十百千万]+|\\d+))'
time_restr += u'|(\\d+[:：]\\d+(分|))'
time_restr += u'|((\\d+):(\\d+))'
time_restr += u'|(\\d+/\\d+/\\d+)'
#time_restr += u'|(未来)'
#time_restr += u'|((充满美丽、希望、挑战的)?未来)'
#time_restr += u'|(最近)'
time_restr += u'|(早上)'
time_restr += u'|(早(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(日前)'
#time_restr += u'|(新世纪)'
time_restr += u'|(小时)'
time_restr += u'|(([0-3][0-9]|[1-9])(日|号)(?!(店|家居网|商城)))'
time_restr += u'|(明天)'
time_restr += u'|(半[个]?(天|日|年|月)[以之]?(前|后))'
time_restr += u'|(([0-3][0-9]|[1-9])[日号](?!(店|家居网|商城)))'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)周)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|([一二三四五六七八九十百千万几多]+[天日周月年][后前左右]*)'
time_restr += u'|(每[年月日天小时分秒钟]+)'
time_restr += u'|((\\d+分)+(\\d+秒)?)'
time_restr += u'|([一二三四五六七八九十]+来?[岁年])'
time_restr += u'|([新?|\\d*]世纪末?)'
time_restr += u'|((\\d+)时)'
time_restr += u'|(世纪)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)岁)'
time_restr += u'|(今年)'
time_restr += u'|([星期周]+[一二三四五六七])'
time_restr += u'|(星期([零一二三四五六七八九十百千万]+|\\d+))'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|((大)?[本后昨当新后明今去前那这][一二三四五六七八九十]?[年月日天])'
time_restr += u'|(早|早晨|早上|上午|中午|午后|下午|晚上|晚间|夜里|夜|凌晨|深夜)'
time_restr += u'|(回归前后)'
time_restr += u'|((\\d+点)+(\\d+分)?(\\d+秒)?左右?)'
time_restr += u'|((\\d+)年代)'
time_restr += u'|(本月(\\d+))'
time_restr += u'|(第(\\d+)天)'
time_restr += u'|((\\d+)岁)'
time_restr += u'|((\\d+)年(\\d+)月)'
time_restr += u'|([去今明]?[年月](底|末))'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)世纪)'
time_restr += u'|(昨天(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(年度)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)星期)'
time_restr += u'|(年底)'
time_restr += u'|([下个本]+赛季)'
time_restr += u'|(今年(\\d+)月(\\d+)日)'
time_restr += u'|((\\d+)月(\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午(\\d+)时)'
time_restr += u'|(今年晚些时候)'
time_restr += u'|(两个星期)'
time_restr += u'|(过去(数|多|多少|好几|几|差不多|近|前|后|上|左右)周)'
time_restr += u'|(本赛季)'
time_restr += u'|(半个(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(稍晚)'
time_restr += u'|((\\d+)号晚(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(今(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+)年)'
time_restr += u'|(这个时候)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)个小时)'
time_restr += u'|(最(数|多|多少|好几|几|差不多|近|前|后|上|左右)(数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(凌晨)'
time_restr += u'|((\\d+)年(\\d+)月(\\d+)日)'
time_restr += u'|((\\d+)个月)'
time_restr += u'|(今天早(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(第[一二三四五六七八九十\\d+]+季)'
time_restr += u'|(当地时间)'
time_restr += u'|(今(数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|(早晨)'
time_restr += u'|(一段时间)'
time_restr += u'|([本上]周[一二三四五六七])'
time_restr += u'|(凌晨(\\d+)点)'
time_restr += u'|(去年(\\d+)月(\\d+)日)'
time_restr += u'|(年关)'
time_restr += u'|(如今)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)小时)'
time_restr += u'|(当晚)'
time_restr += u'|((\\d+)日晚(\\d+)时)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(每年(\\d+)月(\\d+)日)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)周)'
time_restr += u'|((\\d+)月)'
time_restr += u'|(农历)'
time_restr += u'|(两个小时)'
time_restr += u'|(本周([零一二三四五六七八九十百千万]+|\\d+))'
time_restr += u'|(长久)'
time_restr += u'|(清晨)'
time_restr += u'|((\\d+)号晚)'
time_restr += u'|(春节)'
time_restr += u'|(星期日)'
time_restr += u'|(圣诞)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)段)'
time_restr += u'|(现年)'
time_restr += u'|(当日)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)分钟)'
time_restr += u'|(\\d+(天|日|周|月|年)(后|前|))'
time_restr += u'|((文艺复兴|巴洛克|前苏联|前一|暴力和专制|成年时期|古罗马|我们所处的敏感)+时期)'
time_restr += u'|((\\d+)[年月天])'
time_restr += u'|(清早)'
time_restr += u'|(两年)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(昨天(数|多|多少|好几|几|差不多|近|前|后|上|左右)午(\\d+)时)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(今(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+))'
time_restr += u'|(圣诞节)'
time_restr += u'|(学期)'
time_restr += u'|(\\d+来?分钟)'
time_restr += u'|(过去(数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(星期天)'
time_restr += u'|(夜间)'
time_restr += u'|((\\d+)日凌晨)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)月底)'
time_restr += u'|(当天)'
time_restr += u'|((\\d+)日)'
time_restr += u'|(((10)'
time_restr += u'|(11)'
time_restr += u'|(12)'
time_restr += u'|([1-9]))月)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)(数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(今年(\\d+)月份)'
time_restr += u'|(晚(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+)时)'
time_restr += u'|(连[年月日夜])'
time_restr += u'|((\\d+)年(\\d+)月(\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|((一|二|两|三|四|五|六|七|八|九|十|百|千|万|几|多|上|\\d+)+个?(天|日|周|月|年)(后|前|半|))'
time_restr += u'|((胜利的)日子)'
time_restr += u'|(青春期)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(早(数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)点(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|([0-9]{4}年)'
time_restr += u'|(周末)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)个(数|多|多少|好几|几|差不多|近|前|后|上|左右)小时)'
time_restr += u'|(([(小学)|初中?|高中?|大学?|研][一二三四五六七八九十]?(\\d+)?)?[上下]半?学期)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)时期)'
time_restr += u'|(午间)'
time_restr += u'|(次年)'
time_restr += u'|(这时候)'
time_restr += u'|(农历新年)'
time_restr += u'|([春夏秋冬](天|季))'
time_restr += u'|((\\d+)天)'
time_restr += u'|(元宵节)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)分)'
time_restr += u'|((\\d+)月(\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(晚(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+)时(\\d+)分)'
time_restr += u'|(傍晚)'
time_restr += u'|(周([零一二三四五六七八九十百千万]+|\\d+))'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)午(\\d+)时(\\d+)分)'
time_restr += u'|(同日)'
time_restr += u'|((\\d+)年(\\d+)月底)'
time_restr += u'|((\\d+)分钟)'
time_restr += u'|((\\d+)世纪)'
time_restr += u'|(冬季)'
time_restr += u'|(国庆)'
time_restr += u'|(年代)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)年半)'
time_restr += u'|(今年年底)'
time_restr += u'|(新年)'
time_restr += u'|(本周)'
time_restr += u'|(当地时间星期([零一二三四五六七八九十百千万]+|\\d+))'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)岁)'
time_restr += u'|(半小时)'
time_restr += u'|(每周)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)周年)'
time_restr += u'|((重要|最后)?时刻)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)期间)'
time_restr += u'|(周日)'
time_restr += u'|(晚(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(今后)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)段时间)'
time_restr += u'|(明年)'
time_restr += u'|([12][09][0-9]{2}(年度?))'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)生)'
time_restr += u'|(今天凌晨)'
time_restr += u'|(过去(\\d+)年)'
time_restr += u'|(元月)'
time_restr += u'|((\\d+)月(\\d+)日凌晨)'
time_restr += u'|([前去今明后新]+年)'
time_restr += u'|((\\d+)月(\\d+))'
time_restr += u'|(夏天)'
time_restr += u'|((\\d+)日凌晨(\\d+)时许)'
time_restr += u'|((\\d+)月(\\d+)日)'
time_restr += u'|((\\d+)点半)'
time_restr += u'|(去年底)'
time_restr += u'|(最后一[天刻])'
time_restr += u'|(最(数|多|多少|好几|几|差不多|近|前|后|上|左右)(数|多|多少|好几|几|差不多|近|前|后|上|左右)个月)'
time_restr += u'|(圣诞节?)'
time_restr += u'|(下?个?(星期|周)(一|二|三|四|五|六|七|天))'
time_restr += u'|((\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)年)'
time_restr += u'|(当天(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(每年的(\\d+)月(\\d+)日)'
time_restr += u'|((\\d+)日晚(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(星期([零一二三四五六七八九十百千万]+|\\d+)晚)'
time_restr += u'|(深夜)'
time_restr += u'|(现如今)'
time_restr += u'|([上中下]+午)'
time_restr += u'|(第(一|二|三|四|五|六|七|八|九|十|百|千|万|几|多|\\d+)+个?(天|日|周|月|年))'
time_restr += u'|(昨晚)'
time_restr += u'|(近年)'
time_restr += u'|(今天清晨)'
time_restr += u'|(中旬)'
time_restr += u'|(星期([零一二三四五六七八九十百千万]+|\\d+)早)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)战期间)'
time_restr += u'|(星期)'
time_restr += u'|(昨天晚(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(较早时)'
time_restr += u'|(个(数|多|多少|好几|几|差不多|近|前|后|上|左右)小时)'
time_restr += u'|((民主高中|我们所处的|复仇主义和其它危害人类的灾难性疾病盛行的|快速承包电影主权的|恢复自我美德|人类审美力基础设施|饱受暴力、野蛮、流血、仇恨、嫉妒的|童年|艰苦的童年)+时代)'
time_restr += u'|(元旦)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)个礼拜)'
time_restr += u'|(昨日)'
time_restr += u'|([年月]初)'
time_restr += u'|((\\d+)年的(\\d+)月)'
time_restr += u'|(每年)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)月份)'
time_restr += u'|(今年(\\d+)月(\\d+)号)'
time_restr += u'|(今年([零一二三四五六七八九十百千万]+|\\d+)月)'
time_restr += u'|((\\d+)月底)'
time_restr += u'|(未来(\\d+)年)'
time_restr += u'|(第([零一二三四五六七八九十百千万]+|\\d+)季)'
time_restr += u'|(\\d?多年)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)[个]?(星期|周)(前|后)[的]?(周|星期)\d+)'
time_restr += u'|((\\d+)年([零一二三四五六七八九十百千万]+|\\d+)月)'
time_restr += u'|([下上中]午)'
time_restr += u'|(早(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+)点)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)月)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)个(数|多|多少|好几|几|差不多|近|前|后|上|左右)月)'
time_restr += u'|(同([零一二三四五六七八九十百千万]+|\\d+)天)'
time_restr += u'|((\\d+)号凌晨)'
time_restr += u'|(夜里)'
time_restr += u'|(两个(数|多|多少|好几|几|差不多|近|前|后|上|左右)小时)'
time_restr += u'|(昨天)'
time_restr += u'|(罗马时代)'
time_restr += u'|(目(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)月)'
time_restr += u'|((\\d+)年(\\d+)月(\\d+)号)'
time_restr += u'|(((10)'
time_restr += u'|(11)'
time_restr += u'|(12)'
time_restr += u'|([1-9]))月份?)'
time_restr += u'|([12][0-9]世纪)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)天)'
time_restr += u'|(工作日)'
time_restr += u'|(稍后)'
time_restr += u'|((\\d+)号(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(未来([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|([0-9]+[天日周月年][后前左右]*)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(最(数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)刻)'
time_restr += u'|(很久)'
time_restr += u'|((\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)岁)'
time_restr += u'|(去年(\\d+)月(\\d+)号)'
time_restr += u'|(两个月)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)午(\\d+)时)'
time_restr += u'|(古代)'
time_restr += u'|(两天)'
time_restr += u'|(\\d+个?(小时|星期))'
time_restr += u'|((\\d+)年半)'
time_restr += u'|(较早)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)个小时)'
time_restr += u'|([一二三四五六七八九十]+周年)'
time_restr += u'|(星期([零一二三四五六七八九十百千万]+|\\d+)(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(时刻)'
time_restr += u'|((\\d+天)+(\\d+点)?(\\d+分)?(\\d+秒)?)'
time_restr += u'|((\\d+)日([零一二三四五六七八九十百千万]+|\\d+)时)'
time_restr += u'|((\\d+)周年)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)早)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)日)'
time_restr += u'|(去年(\\d+)月)'
time_restr += u'|(过去([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|((\\d+)个星期)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)(数|多|多少|好几|几|差不多|近|前|后|上|左右)天)'
time_restr += u'|(执政期间)'
time_restr += u'|([当前昨今明后春夏秋冬]+天)'
time_restr += u'|(去年(\\d+)月份)'
time_restr += u'|(今(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|((\\d+)周)'
time_restr += u'|(两星期)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)年代)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)天)'
time_restr += u'|(昔日)'
time_restr += u'|(两个半月)'
time_restr += u'|([印尼|北京|美国]?当地时间)'
time_restr += u'|(连日)'
time_restr += u'|(本月(\\d+)日)'
time_restr += u'|(第([零一二三四五六七八九十百千万]+|\\d+)天)'
time_restr += u'|((\\d+)点(\\d+)分)'
time_restr += u'|([长近多]年)'
time_restr += u'|((\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午(\\d+)时)'
time_restr += u'|(那时)'
time_restr += u'|(冷战时代)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)天)'
time_restr += u'|(这个星期)'
time_restr += u'|(去年)'
time_restr += u'|(昨天傍晚)'
time_restr += u'|(近期)'
time_restr += u'|(星期([零一二三四五六七八九十百千万]+|\\d+)早些时候)'
time_restr += u'|((\\d+)([零一二三四五六七八九十百千万]+|\\d+)年)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)两个月)'
time_restr += u'|((\\d+)个小时)'
time_restr += u'|(([零一二三四五六七八九十百千万]+|\\d+)个月)'
time_restr += u'|(当年)'
time_restr += u'|(本月)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)([零一二三四五六七八九十百千万]+|\\d+)个月)'
time_restr += u'|((\\d+)点(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(目前)'
time_restr += u'|(去年([零一二三四五六七八九十百千万]+|\\d+)月)'
time_restr += u'|((\\d+)时(\\d+)分)'
time_restr += u'|(每月)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)段时间)'
time_restr += u'|((\\d+)日晚)'
time_restr += u'|(早(数|多|多少|好几|几|差不多|近|前|后|上|左右)(\\d+)点(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(下旬)'
time_restr += u'|((\\d+)月份)'
time_restr += u'|(逐年)'
time_restr += u'|(稍(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|((\\d+)年)'
time_restr += u'|(月底)'
time_restr += u'|(这个月)'
time_restr += u'|((\\d+)年(\\d+)个月)'
time_restr += u'|(\\d+大寿)'
time_restr += u'|(周([零一二三四五六七八九十百千万]+|\\d+)早(数|多|多少|好几|几|差不多|近|前|后|上|左右))'
time_restr += u'|(半年)'
time_restr += u'|(今日)'
time_restr += u'|(末日)'
time_restr += u'|(昨天深夜)'
time_restr += u'|(今年(\\d+)月)'
time_restr += u'|((\\d+)月(\\d+)号)'
time_restr += u'|((\\d+)日夜)'
time_restr += u'|((早些|某个|晚间|本星期早些|前些)+时候)'
time_restr += u'|(同年)'
time_restr += u'|((北京|那个|更长的|最终冲突的)时间)'
time_restr += u'|(每个月)'
time_restr += u'|(一早)'
time_restr += u'|((\\d+)来?[岁年])'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)个月)'
time_restr += u'|([鼠牛虎兔龙蛇马羊猴鸡狗猪]年)'
time_restr += u'|(季度)'
time_restr += u'|(早些时候)'
time_restr += u'|(今天)'
time_restr += u'|(每天)'
time_restr += u'|(年半)'
time_restr += u'|(半(个)?月)'
time_restr += u'|(下下(个)?月)'
time_restr += u'|(下(个)?月)'
time_restr += u'|(午后)'
time_restr += u'|((\\d+)日(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|((数|多|多少|好几|几|差不多|近|前|后|上|左右)个星期)'
time_restr += u'|(今天(数|多|多少|好几|几|差不多|近|前|后|上|左右)午)'
time_restr += u'|(同[一二三四五六七八九十][年|月|天])'
time_restr += u'|(T\\d+:\\d+:\\d+)'
time_restr += u'|(\\d+/\\d+/\\d+:\\d+:\\d+.\\d+)'
time_restr += u'|(\\?\\?\\?\\?-\\?\\?-\\?\\?T\\d+:\\d+:\\d+)'
time_restr += u'|(\\d+-\\d+-\\d+T\\d+:\\d+:\\d+)'
time_restr += u'|(\\d+/\\d+/\\d+ \\d+:\\d+:\\d+.\\d+)'
time_restr += u'|(\\d+-\\d+-\\d+|[0-9]{8})'
time_restr += u'|(((\\d+)年)?((10)'
time_restr += u'|(11)'
time_restr += u'|(12)'
time_restr += u'|([1-9]))月(\\d+))'
time_restr += u'|((\\d[\\.\\-])?((10)'
time_restr += u'|(11)'
time_restr += u'|(12)'
time_restr += u'|([1-9]))[\\.\\-](\\d+))'

time_rules = [
#1988-01-28
('day',    'day1',       1, u'[0-9]?[0-9]?[0-9]{2}-((10)|(11)|(12)|([1-9]))-((?<!\\d))([0-3][0-9]|[1-9])'),
#1988/01/28
('day',    'day2',       1, u'((10)|(11)|(12)|([1-9]))/((?<!\\d))([0-3][0-9]|[1-9])/[0-9]?[0-9]?[0-9]{2}'), 
#1988.01.28
('day',    'day3',       1, u'[0-9]?[0-9]?[0-9]{2}\\.((10)|(11)|(12)|([1-9]))\\.((?<!\\d))([0-3][0-9]|[1-9])'),
#12:00:00
('second', 'time1',      1, u'(?<!(周|星期))([0-2]?[0-9]):[0-5]?[0-9]:[0-5]?[0-9]'),
#12:00
('second', 'time2',      1, u'(?<!(周|星期|:|[0-9]))([0-2]?[0-9]):[0-5]?[0-9](?!(:|[0-9]))'),
#30秒,1分30秒
('second', 'abs_rel',    1, u'([0-5]?[0-9](?=秒[钟]?(?!([钟]?[以之]?(前|后)))))|((?<=分)[0-5]?[0-9])'),
#12点半
('minute', 'abs',       30, u'(?<=[点时])半(?!(前|后))'),
#12点3刻
('minute', 'abs',       45, u'(?<=[点时])[3三]刻(?!钟)'),
#12点1刻
('minute', 'abs',       15, u'(?<=[点时])[1一]刻(?!钟)'),
#12点30分,12点30
('minute', 'abs_rel',    1, u'([0-5]?[0-9](?=分(?!钟)))|((?<=((?<!小)[点时]))[0-5]?[0-9](?!刻))'),
#12点,下午3点
('hour',   'rel_base',   1, u'(?<!(周|星期))(?<=(中午|午间|下午|午后|晚上|夜间|夜里|今晚))([0-2]?[0-9])(?=(点|时))'),
('hour',   'abs_rel',    1, u'(?<!(周|星期))(?<!(中午|午间|下午|午后|晚上|夜间|夜里|今晚))([0-2]?[0-9])(?=(点|时))'),
('hour',   'abs',        3, u'(凌晨)(?![0-9]点)'),
('hour',   'abs',        8, u'(早上|早晨|早间|晨间|今早|明早)(?![0-9]点)'),
('hour',   'abs',       10, u'(上午)(?![0-9]点)'),
('hour',   'abs',       12, u'(中午|午间)(?![0-9]点)'),
('hour',   'abs',       15, u'(下午|午后)(?![0-9]点)'),
('hour',   'abs',       18, u'(晚上|夜间|夜里|今晚)(?![0-9]点)'),
('hour',   'abs',       20, u'(夜晚)(?![0-9]点)'),
('hour',   'abs',       23, u'(深夜)(?![0-9]点)'),
#88年,08年
('year',   'base_rel',   0, u'[0-9]{2}(?=年)'),
#2000年
('year',   'abs_rel',    1, u'[0-9][0-9]{3}(?=年)'),
('month',  'abs_rel',    1, u'((10)|(11)|(12)|([1-9]))(?=月)'),
('day',    'abs_rel',    1, u'((?<!\d))([0-3][0-9]|[1-9])(?=(日|号))'),
#3秒前
('second', 'cur_abs_rel',-1, u'\d+(?=秒(钟)?[以之]?前)'),
('second', 'cur_abs_rel', 1, u'\d+(?=秒(钟)?[以之]?后)'),
#3分钟前
('minute', 'cur_abs_rel',-1, u'\d+(?=分钟[以之]?前)'),
('minute', 'cur_abs_rel', 1, u'\d+(?=分钟[以之]?后)'),
#3个半小时前,三个小时半前
('hour',   'cur_abs_rel_base',-1, u'\d+(?=个(半小时|小时半)[以之]?前)'),
('hour',   'cur_abs_rel_base', 1, u'\d+(?=个(半小时|小时半)[以之]?后)'),
#3个小时前
('hour',   'cur_abs_rel',-1, u'\d+(?=(个)?小时[以之]?前)'),
('hour',   'cur_abs_rel', 1, u'\d+(?=(个)?小时[以之]?后)'),
#3天前,3天之前,3天以前
('day',    'cur_abs_rel',-1, u'\d+(?=天[以之]?前)'),
('day',    'cur_abs_rel', 1, u'\d+(?=天[以之]?后)'),
#3个月半前,3个月半前
('month',  'cur_abs_rel_base',-1, u'\d+(?=个(半月|月半)[以之]?前)'),
('month',  'cur_abs_rel_base', 1, u'\d+(?=个(半月|月半)[以之]?后)'),
#3个月前,3月前
('month',  'cur_abs_rel',-1, u'\d+(?=(个)?月[以之]?前)'),
('month',  'cur_abs_rel', 1, u'\d+(?=(个)?月[以之]?后)'),
#3年前
('year',   'cur_abs_rel',-1, u'\d+(?=年[以之]?前)'),
('year',   'cur_abs_rel', 1, u'\d+(?=年[以之]?后)'),
#半分钟前
('second', 'cur_rel',  -30, u'(?<![0-9]个)半(?=分钟[以之]?前)'),
('second', 'cur_rel',   30, u'(?<![0-9]个)半(?=分钟[以之]?后)'),
#半小时前
('minute', 'cur_rel',  -30, u'(?<![0-9]个)半(?=(个))?(?=小时[以之]?前)'),
('minute', 'cur_rel',   30, u'(?<![0-9]个)半(?=(个))?(?=小时[以之]?后)'),
#半天前
('hour',   'cur_rel',   -6, u'(?<![0-9]个)半(?=天[以之]?前)'),
('hour',   'cur_rel',    6, u'(?<![0-9]个)半(?=天[以之]?后)'),
#半个月前
('day',    'cur_rel',  -15, u'(?<![0-9]个)半(?=(个)?月[以之]?前)'),
('day',    'cur_rel',   15, u'(?<![0-9]个)半(?=(个)?月[以之]?后)'),
#半年前
('month',  'cur_rel',   -6, u'(?<![0-9]个)半(?=年[以之]?前)'),
('month',  'cur_rel',    6, u'(?<![0-9]个)半(?=年[以之]?后)'),
('year',   'cur_rel',   -3, u'大前年'),
('year',   'cur_rel',   -2, u'(?<!大)前年'),
('year',   'cur_rel',   -1, u'去年'),
('year',   'cur_rel',    0, u'今年'),
('year',   'cur_rel',    1, u'明年'),
('year',   'cur_rel',    3, u'大后年'),
('year',   'cur_rel',    2, u'(?<!大)后年'),
('month',  'cur_rel',   -2, u'上上(个)?月'),
('month',  'cur_rel',   -1, u'(?<!上)上(个)?月'),
('month',  'cur_rel',    0, u'(本|这个)月'),
('month',  'cur_rel',    1, u'(?<!下)下(个)?月'),
('month',  'cur_rel',    2, u'下下(个)?月'),
('day',    'cur_rel',   -3, u'大前天'),
('day',    'cur_rel',    3, u'大后天'),
('day',    'cur_rel',   -3, u'(?<!大)前天'),
('day',    'cur_rel',    2, u'(?<!大)后天'),
('day',    'cur_rel',   -1, u'昨(天|日)'),
('day',    'cur_rel',    0, u'(今|这)(天|日)'),
('day',    'cur_rel',    1, u'明(天|日)'),
#上上周周3
('week',   'cur_rel',   -2, u'(?<=(上上(周|星期){2}))[1-7]'),
#上周,上周3
('week',   'cur_rel',   -1, u'(?<=((?<!上)上(周|星期){1,2}))[1-7]?'),
('week',   'cur_rel',    1, u'(?<=((?<!下)下(周|星期){1,2}))[1-7]?'),
('week',   'cur_rel',    2, u'(?<=(下下(周|星期){2}))[1-7]'),
('week',   'cur_rel',    0, u'(?<=((?<!(上|下|周|前|后))(周|星期)))[1-7]'),
#3个星期后的周3
('week',  'cur_abs_abs',-1, u'(?P<weeks>\d+)(个)?(星期|周)[以之]?前(周|星期)(?P<weekday>[1-7])'),
('week',  'cur_abs_abs', 1, u'(?P<weeks>\d+)(个)?(星期|周)[以之]?后(周|星期)(?P<weekday>[1-7])'),
]

unit2index = {
        'year':     0,
        'month':    1,
        'day':      2,
        'hour':     3,
        'minute':   4,
        'second':   5,
        }

index2unit = {
        0: 'year',
        1: 'month',
        2: 'day',
        3: 'hour',
        4: 'minute',
        5: 'second',
        }

holidays = {
        u'元旦': (1, 1),
        }

def gettimestr(time=None):
    if time == None:
        time = datetime.datetime.now()
    return time.strftime('%Y-%m-%d-%H-%M-%S')

def add_years(srcdate, years):
    return datetime.datetime(srcdate.year + years, srcdate.month, srcdate.day, srcdate.hour, srcdate.minute, srcdate.second)

def add_months(srcdate, months):
    month = srcdate.month - 1 + months
    year = int(srcdate.year + month / 12 )
    month = month % 12 + 1
    day = min(srcdate.day, calendar.monthrange(year, month)[1])
    return datetime.datetime(year, month, day, srcdate.hour, srcdate.minute, srcdate.second)

def replace_number(m, delimiter=None):
    cndigs = {u'０': '0',
              u'１': '1',
              u'２': '2',
              u'３': '3',
              u'４': '4',
              u'５': '5',
              u'６': '6',
              u'７': '7',
              u'８': '8',
              u'９': '9'}
    text = m.group()
    rst = ''
    if delimiter != None:
        splits = text.split(delimiter)
    else:
        splits = text
    for split in splits:
        if split == u'': continue
        rst += cndigs[split]
    return rst

def full2half_number(string):
    restr = u'[１２３４５６７８９０]{1,}'
    return re.sub(restr, replace_number, string)

def preprocess(text):
    text = re.sub('\s+', '', text)
    text = re.sub(u'[的]+', '', text)
    text = full2half_number(text)
    text = zhnum.zh2num(text)
    return text

class TimeCtx:

    def __init__(self):
        self.units = [-1, -1, -1, -1, -1, -1]

class TimeUnit:

    def __init__(self, text, model, ctx):
        self.timeexp = text
        self.timenorm = ''
        self.timefull = 0
        self.timeorg = 0
        self.time = None
        self.isAllDaytime = True
        self.isFirstTimeSolveCtx = True
        self.type = ''
        self.model = model
        self.ctx = TimeCtx()
        self.ctxorg = ctx
        self.parse()

    def input_unit_with_base(self, base, units, unit, value):
        if self.model.base == self.model.now:
            units[unit2index[unit]] = value
        else:
            unit_tmps = unit2index.keys()
            unit_tmps.remove(unit)
            for unit_tmp in unit_tmps:
                if unit2index[unit_tmp] <= unit2index[unit] and units[unit2index[unit_tmp]] == -1:
                    units[unit2index[unit_tmp]] = base.__getattribute__(unit_tmp)
            units[unit2index[unit]] = value
    
    def export_units(self, base, units, unit, date):
        for unit_tmp in unit2index.keys():
            if unit_tmp == unit or (unit2index[unit_tmp] < unit2index[unit] and (date.__getattribute__(unit_tmp) != base.__getattribute__(unit_tmp) or units[unit2index[unit_tmp]] == -1)):
                units[unit2index[unit_tmp]] = date.__getattribute__(unit_tmp)

    def value(self, match, unit, kind, relate):
        text = match.group()
    
        #print('%s, %s, %s, %s, %s, %s'%(text, unit, kind, relate, self.ctx.units, self.model.base))
        if unit == 'second':
            if kind == 'abs_rel':
                seconds = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'second', seconds)
            elif kind == 'time1':
                hours, minutes, seconds = text.split(':')
                self.input_unit_with_base(self.model.base, self.ctx.units, 'second', int(seconds))
                self.input_unit_with_base(self.model.base, self.ctx.units, 'minute', int(minutes))
                self.input_unit_with_base(self.model.base, self.ctx.units, 'hour', int(hours))
            elif kind == 'time2':
                hours, minutes = text.split(':')
                self.input_unit_with_base(self.model.base, self.ctx.units, 'minute', int(minutes))
                self.input_unit_with_base(self.model.base, self.ctx.units, 'hour', int(hours))
            elif kind == 'cur_rel':
                date = self.model.now + datetime.timedelta(seconds=relate)
                self.export_units(self.model.now, self.ctx.units, 'second', date)
            elif kind == 'cur_abs_rel':
                date = self.model.now + datetime.timedelta(seconds=relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'second', date)
    
        elif unit == 'minute':
            if kind == 'abs_rel':
                minutes = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'minute', minutes)
            elif kind == 'abs':
                self.ctx.units[4] = relate
            elif kind == 'cur_rel':
                date = self.model.now + datetime.timedelta(minutes=relate)
                self.export_units(self.model.now, self.ctx.units, 'minute', date)
            elif kind == 'cur_abs_rel':
                date = self.model.now + datetime.timedelta(minutes=relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'minute', date)
    
        elif unit == 'hour':
            if kind == 'abs_rel':
                hours = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'hour', hours)
            elif kind == 'abs':
                self.ctx.units[3] = relate
            elif kind == 'rel_base':
                hours = int(text) * relate
                hours += 12
                self.input_unit_with_base(self.model.base, self.ctx.units, 'hour', hours)
            elif kind == 'cur_rel':
                date = self.model.now + datetime.timedelta(hours=relate)
                self.export_units(self.model.now, self.ctx.units, 'hour', date)
            elif kind == 'cur_abs_rel':
                date = self.model.now + datetime.timedelta(hours=relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'hour', date)
            elif kind == 'cur_abs_rel_base':
                date = self.model.now + datetime.timedelta(hours=relate * int(text) + 0.5)
                self.export_units(self.model.now, self.ctx.units, 'minute', date)

        elif unit == 'day':
            if kind == 'abs_rel':
                days = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'day', days)
            elif kind == 'day1':
                splits = text.split('-')
                self.ctx.units[0] = int(splits[0])
                self.ctx.units[1] = int(splits[1])
                self.ctx.units[2] = int(splits[2])
            elif kind == 'day2':
                splits = text.split('/')
                self.ctx.units[0] = int(splits[0])
                self.ctx.units[1] = int(splits[1])
                self.ctx.units[2] = int(splits[2])
            elif kind == 'day3':
                splits = text.split('.')
                self.ctx.units[0] = int(splits[0])
                self.ctx.units[1] = int(splits[1])
                self.ctx.units[2] = int(splits[2])
            elif kind == 'cur_rel':
                date = self.model.now + datetime.timedelta(days=relate)
                self.export_units(self.model.now, self.ctx.units, 'day', date)
            elif kind == 'cur_abs_rel':
                date = self.model.now + datetime.timedelta(days=relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'day', date)
    
        elif unit == 'week':
            if kind == 'cur_rel':
                if text == '':
                    weekday = 1
                else:
                    weekday = int(text)
                delta = weekday - (self.model.now.weekday() + 1)
                date = self.model.now + datetime.timedelta(weeks=relate)
                date += datetime.timedelta(days=delta)
                self.export_units(self.model.now, self.ctx.units, 'day', date)
            elif kind == 'cur_abs_rel':
                if text == '':
                    weekday = 1
                else:
                    weekday = int(text)
                delta = weekday - (self.model.now.weekday() + 1)
                date = self.model.now + datetime.timedelta(weeks=relate)
                date += datetime.timedelta(days=delta)
                self.export_units(self.model.now, self.ctx.units, 'day', date)
            elif kind == 'cur_abs_abs':
                weekday = int(match.group('weekday'))
                weeks = int(match.group('weeks'))
                delta = weekday - (self.model.now.weekday() + 1)
                date = self.model.now + datetime.timedelta(weeks=relate * weeks)
                date += datetime.timedelta(days=delta)
                self.export_units(self.model.now, self.ctx.units, 'day', date)
    
        elif unit == 'month':
            if kind == 'abs_rel':
                months = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'month', months)
            elif kind == 'cur_rel':
                date = add_months(self.model.now, relate)
                self.export_units(self.model.now, self.ctx.units, 'month', date)
            elif kind == 'cur_abs_rel':
                date = add_months(self.model.now, relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'month', date)
            elif kind == 'cur_abs_rel_base':
                date = add_months(self.model.now, relate * int(text) + 0.5)
                self.export_units(self.model.now, self.ctx.units, 'month', date)
    
        elif unit == 'year':
            if kind == 'abs_rel':
                years = int(text) * relate
                self.input_unit_with_base(self.model.base, self.ctx.units, 'year', years)
            elif kind == 'cur_rel':
                date = add_years(self.model.now, relate)
                self.export_units(self.model.now, self.ctx.units, 'year', date)
            elif kind == 'base_rel':
                if len(text) == 2:
                    if int(text) > 20:
                        self.ctx.units[0] = 1900 + int(text)
                    else:
                        self.ctx.units[0] = 2000 + int(text)
                else:
                    self.ctx.units[0] = int(text)
            elif kind == 'cur_abs_rel':
                date = add_years(self.model.now, relate * int(text))
                self.export_units(self.model.now, self.ctx.units, 'year', date)
    
        pass

    def getdatetime(self, units):
        for i in range(6):
            if units[i] == -1:
                if i >= 3: units[i] = 0
                elif i == 0: units[i] = 1900
                else: units[i]  = 1
        return datetime.datetime(units[0], units[1], units[2], units[3], units[4], units[5])

    def makefuturedatetime(self):
        if self.type == 'datetime':
            print('Cannot convert a datetime to future datetime')
            return -1, None
        if (self.type == 'year' or self.type == 'date') and self.ctx.units[0] < self.model.now.year:
            print('Cannot convert a past %s  to future datetime'%self.type)
            return -1, None

        units = [-1 for i in range(6)]
        flag = False
        for i in range(5, -1, -1):
            if self.ctx.units[i] == -1:
                if flag:
                    units[i] = self.model.now.__getattribute__(index2unit[i])
            else:
                units[i] = self.ctx.units[i]
                if not flag: flag = True

        date = self.getdatetime(units)
        if date < self.model.now:
            print('Convert failed datetime(%s) base on now(%s) pasted!'%(gettimestr(date), gettimestr(self.model.now)))
            if self.ctx.units[1] != -1:
                date = add_years(date, 1)
            elif self.ctx.units[2] != -1:
                date = add_months(date, 1)
            else:
                date += datetime.timedelta(days=1)
            print('Suggestion datetime: %s'%gettimestr(date))

            return -1, date
        return 0, date

    def repeatable(self):
        if self.type in ['time', 'month_only', 'date_only', 'month_date_only']:
            return True
        return False

    def timetype(self, units):
        t = 'error'
        if units[0] != -1 \
                and units[1] == -1 \
                and units[2] == -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'year'
            units[1] = 1
            units[2] = 1
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] != -1 \
                and units[1] != -1 \
                and units[2] == -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'year_month'
            units[2] = 1
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] != -1 \
                and units[1] != -1 \
                and units[2] != -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'date'
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] != -1 \
                and units[1] != -1 \
                and units[2] != -1 \
                and units[3] != -1:
            t = 'datetime'
            if units[4] == -1:
                units[4] = 0
                units[5] = 0
            else:
                units[5] = 0
        elif units[0] == -1 \
                and units[1] == -1 \
                and units[2] == -1 \
                and units[3] != -1:
            t = 'time'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            units[1] = self.model.now.__getattribute__(index2unit[1])
            units[2] = self.model.now.__getattribute__(index2unit[2])
            if units[4] == -1:
                units[4] = 0
                units[5] = 0
            else:
                units[5] = 0
        elif units[0] == -1 \
                and units[1] != -1 \
                and units[2] == -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'month'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            units[2] = 1
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] == -1 \
                and units[1] == -1 \
                and units[2] != -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'day'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            units[1] = self.model.now.__getattribute__(index2unit[1])
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] == -1 \
                and units[1] != -1 \
                and units[2] != -1 \
                and units[3] == -1 \
                and units[4] == -1 \
                and units[5] == -1:
            t = 'month_day'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            units[3] = 0
            units[4] = 0
            units[5] = 0
        elif units[0] == -1 \
                and units[1] != -1 \
                and units[2] != -1 \
                and units[3] != -1:
            t = 'month_day_time'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            if units[4] == -1:
                units[4] = 0
                units[5] = 0
            else:
                units[5] = 0
        elif units[0] == -1 \
                and units[1] == -1 \
                and units[2] != -1 \
                and units[3] != -1:
            t = 'day_time'
            units[0] = self.model.now.__getattribute__(index2unit[0])
            units[1] = self.model.now.__getattribute__(index2unit[1])
            if units[4] == -1:
                units[4] = 0
                units[5] = 0
            else:
                units[5] = 0
        else:
            units[0] = 1900
            units[1] = 1
            units[2] = 1
            units[3] = 0
            units[4] = 0
            units[5] = 0

        if units[0] < 1900:
            units[0] = 1900

        return t, units

    def parse(self):
        #print('parse: %s'%self.timeexp)

        for unit, kind, relate, restr in time_rules:
            regex = re.compile(restr)
            m = regex.search(self.timeexp)
            if m:
                self.value(m, unit, kind, relate)

        units = self.ctx.units[:]
        self.type, units = self.timetype(units)
        self.time = datetime.datetime(units[0], units[1], units[2], units[3], units[4], units[5])

    def __repr__(self):
        return '%s(%s)'%(gettimestr(self.time), self.type)

class ZhTime:

    def __init__(self):
        self.regex = re.compile(time_restr)
        self.text = ''
        self.isPreferFuture = False
        self.base = None
        self.now = None

    def filter(self, rst):
        return rst

    def zh2time(self, text):

        buf = ['' for i in range(100)]
        startline = endline = -1
        pointer = 0
        startmarker = True

        for match in self.regex.finditer(text):
            startline = match.start()
            if endline == startline:
                pointer -= 1
                buf[pointer] += match.group()
            else:
                startmarker = False
                buf[pointer] = match.group()
            endline = match.end()
            pointer += 1
        
        rst = []
        ctx = TimeCtx()
        for i in range(pointer):
            rst.append(TimeUnit(buf[i], self, ctx))
            ctx = rst[i].ctx
            self.base = rst[i].time
        
        print('%s: %s'%(self.text, rst))
        rst = self.filter(rst)
        return rst

    def parse(self, text, basetime=None):
        if basetime == None:
            basetime = datetime.datetime.now()
        self.base = basetime
        self.now = basetime
        self.text = text
        text = preprocess(text)
        t = self.zh2time(text)
        return t

def test():
    texts = [
            u'2008年', 
            u'去年三月份',
            u'2012年2月23日', 
            u'去年3月20号上午九点半',
            u'12点十六分59秒',
            u'三月份',
            u'5号',
            u'八月八号',
            u'7月30号10:00:00', 
            u'8号1:20',
            u'今天上午八点二十三分叫我起床',
            u'下午四点半',
            u'周三八点',
            u'一九八八年', 
            u'一号家居网上午9点举行展览',
            u'大后年',
            u'下个月',
            u'后天',
            u'下周',
            u'2016-8-19',
            u'明年的今天',
            u'后年的3月2号',
            u'下午3点半',
            u'三个小时半后',
            u'十年以后',
            u'三个星期后的周三',
            u'下个月23号23:59:59',
            u'周六中午',
            u'半个月后',
            u'下周周五',
            u'前年10月20号的晚上十点半',
            u'明天23点',
            u'后天二十一点',
            u'23号21点',
            u'二十三号二十一点半',
            u'下个月二十八号1点半',
            u'下下个月1号8点半',
            u'下个月1号8:20',
            u'23日2点半',
            u'四点半',
            u'凌晨1点半',
            u'凌晨三点半',
            u'23:00',
            u'下个月25日晚上九点半',
            u'下下个月二十三号中午十二点',
            u'这个25号',
            u'这个月25号',
            u'我们计划在本月25号下午2点和下下个月13号上午10点半举行盛大的仪式',
            u'九寨沟8月13号的天气',
            u'我在去年就说过:"三月份是回归日"，你们不信',
            u'上个月和这个月',
            u'明天三点和后天四点',
            u'去年三月和四月',
            u'去年三月和今年四月',
            u'去年上个月和这个月',
            u'上个月三号和四号',
            u'上个月三号和这个月四号',
            u'去年今天',
            u'这天',
            u'去年这天',
            u'十天后',
            u'十年后的今天',
            u'２００８年的这天',
            u'下午4点多',
            u'后天十点到十点半',
            u'下个月三十号十点到十点半',
            u'昨天十点到今天十一点间',
            u'后天十点到大后天下午五点的车都可以',
            u'一年多以来',
            u'一个小时左右',
            u'三天内',
            u'二十四小时之内',
            u'未来一周的机票',
            u'国庆节这一天的机票',
            u'上一个周五',
            ]
    zt = ZhTime()
    for text in texts[-8:]:
        zt.parse(text)

def cmd(text):
    zt = ZhTime()
    zt.parse(text.decode('utf-8'))

if __name__ == '__main__':
    fire.Fire(test)
