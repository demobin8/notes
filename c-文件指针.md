> ...

用read、write读写文件时，每读取或写入一定长度，文件指针就偏移对应的长度。

可以用lseek将文件指针设置到想要的偏移：off_t lseek(int fd,off_t offset ,int whence);

第一个参数是你open的文件句柄，第二个参数是偏移量，第三个参数是从哪儿开始计算偏移量。

whence为下列其中一种:（SEEK_SET,SEEK_CUR和SEEK_END和依次为0，1和2）。

SEEK_SET 将读写位置指向文件头后再增加offset个位移量、SEEK_CUR 以目前的读写位置往后增加offset个位移量、SEEK_END 将读写位置指向文件尾后再增加offset个位移量。当whence 值为SEEK_CUR 或SEEK_END时，参数offet允许负值的出现。

下列是几个常用的使用方式:

1) 欲将读写位置移到文件开头时:　　
```
lseek(int fildes, 0, SEEK_SET);
```
3) 欲将读写位置移到文件尾时:　　    
```
lseek(int fildes, 0, SEEK_END);
```
5) 想要取得目前文件位置时:　　       
```
lseek(int fildes, 0, SEEK_CUR);
```
