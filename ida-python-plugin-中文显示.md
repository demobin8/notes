> ...

ida版本是网上流传甚广的61，系统是xp，在逆向的时候，已经知道很多字符串是utf-8的中文，但是网上查关于如何在ida中正确显示的资料很少，有一些做了也没有效果，测试了一下发现只有cp936编码的中文ida才能正确显示，不知道是不是只有xp才会如此，总之最后只好自己做了一个将utf-8的中文编码成cp936的中文添加到注释中的ida-py脚本。

我是从这里学习ida-python的api的

https://www.hex-rays.com/products/ida/support/idapython_docs/

操作方法：

在python cmd窗口
```
import conv82936

con82936.conv82936all()
```
即可

脚本内容如下：
```
import idaapi

import idautils



def isch(data):

    for char in data:

        if char >= u'\u4e00' and char <= u'\u9fa5':

            return True

    return False



def conv82936_2(ea):

    length = idaapi.get_max_ascii_length(ea, 0)

    data8 = idaapi.get_ascii_contents(ea, length, 0)

    try:

        datau = data8.decode('utf-8')

        if not isch(datau):

            data936 = None

            #print 'addr: %x donot contain chinese'%ea

        else:

            data936 = datau.encode('cp936')

    except:

        print 'addr: %x cannot decode as utf-8'%ea

        data936 = None

    return data936



def conv82936():

    ea = idaapi.get_screen_ea()

    return conv82936_2(ea)



def conv82936all():

    s = idautils.Strings(False)

    s.setup(strtypes = idautils.Strings.STR_UNICODE|idautils.Strings.STR_C)

    for i, v in enumerate(s):

        if v is None:

            pass

            #print 'failed to get string from addr: %x  index: %d' %(v.ea, v.index)

        else:

            #print 'addr: %x  len: %d  type: %d  index: %d  str: %s' %(v.ea, v.length, v.type, i, str(v))

            cmt = conv82936_2(v.ea)

            if cmt is None:

                idaapi.set_cmt(v.ea, '', 1)

                #print "addr: %x cannot convert to 936 string"%v.ea

            else:

                idaapi.set_cmt(v.ea, cmt, 1)
```                
