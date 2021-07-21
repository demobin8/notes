> 原样的笔记，估计大部分人看了也不知道这是啥，不改了都放出来。。。

加解密算法
Py版
```
def p2p_udp_encrypt(pkt):
    header=random.randint(0,0xffff)
    t=((header&0x1fff)+0x4000)<<0x10
    t+=random.randint(0,0xffff)
    body=struct.pack('I',t)
    sec2=random.randint(0,0xff)
    body+=struct.pack('B',sec2)
    length=(sec2&0x03)+9
    pos=length
    for i in range(length-5):
        x=random.randint(0,0xff)
        body+=struct.pack('B',x)
        
    l=pos*7
    t=struct.unpack('B',body[pos-3])[0]
    t*=0x0d
    t&=0xff
    k=l^t
    header=body[:pos-2]+struct.pack('B',k)
    t=struct.unpack('B',header[-1])[0]
    t*=0x0d
    t&=0xff
    k=(l+7)^t
    header=header+struct.pack('B',k)
    out=''
    j=0
    t=array.array('B',header)
    buf=array.array('B',pkt)
    body_len=len(pkt)
    for i in range(body_len):
        j+=1
        if j==pos:
            j=0
        x=t[j]+0x5b
        x&=0xff
        x^=t[j-1]
        t[j-1]=x
        buf[i]=(buf[i]+x)&0xff
    
    out=header+buf.tostring()
    #print "out buf len is %d"%len(out)
    #print hexdump(out)
    #print hexdump(p2p_udp_decrypt(out))
    return out
        
def p2p_udp_decrypt(pkt):
    if len(pkt)<=8:
        return False
    header=struct.unpack('<I',pkt[:4])[0]
    header>>=0x1d
    if header>3:
        return False
    elif header ==1:
        pass
    elif header ==2:
        byte5=struct.unpack('B',pkt[4])[0]
        byte5&=0x80000003
        byte5+=9
        if byte5>len(pkt):
            return False
        pos=byte5
        head_check=array.array('B',pkt[:pos])
        t=struct.unpack('B',pkt[pos-2])[0]
        mid=pos*7
        p=7*pos+7
        t*=0x0d
        t&=0xff
        p^=t
        s=struct.unpack('B',pkt[pos-1])[0]
        if p != s:
            return False
        
        t=struct.unpack('B',pkt[pos-3])[0]
        t*=0x0d
        t&=0xff
        t^=mid
        if t !=struct.unpack('B',pkt[pos-2])[0]:
            return False
        j=0
        body=array.array('B',pkt[pos:])
        body_len=len(pkt)-pos
        for i in range(body_len):
            j+=1
            if j==pos:
                j=0
            x=head_check[j]+0x5b
            x&=0xff
            x^=head_check[j-1]
            head_check[j-1]=x
            body[i]=(body[i]-x)&0xff
        
        x=body.tostring()  
        #print hexdump(x)
        return x                           
        
    elif header ==3:
        pass
    return False
```    
