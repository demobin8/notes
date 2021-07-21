> ...

## 说明
uboot源代码的tools/目录下有mkimage工具，这个工具可以用来制作不压缩或者压缩的多种可启动映象文件。

mkimage在制作映象文件的时候，是在原来的可执行映象文件的前面加上一个0x40字节的头，记录参数所指定的信息，这样uboot才能识别这个映象是针对哪个CPU体系结构的，哪个OS的，哪种类型，加载内存中的哪个位置， 入口点在内存的那个位置以及映象名是什么
`root@Glym:/tftpboot# ./mkimage`
## 用法
```
Usage: ./mkimage -l image
-l ==> list image header information
./mkimage -A arch -O os -T type -C comp -a addr -e ep -n name -d data_file[:data_file...] image
-A ==> set architecture to 'arch'
-O ==> set operating system to 'os'
-T ==> set image type to 'type'
-C ==> set compression type 'comp'
-a ==> set load address to 'addr' (hex)
-e ==> set entry point to 'ep' (hex)
-n ==> set image name to 'name'
-d ==> use image data from 'datafile'
-x ==> set XIP (execute in place)
```
参数说明：
* -A 指定CPU的体系结构：取值 表示的体系结构
  - alpha Alpha 
  - arm A RM 
  - x86 Intel x86
  - ia64 IA64
  - mips MIPS
  - mips64 MIPS 64 Bit
  - ppc PowerPC
  - s390 IBM S390
  - sh SuperH
  - sparc SPARC
  - sparc64 SPARC 64 Bit
  - m68k MC68000

* -O 指定操作系统类型，可以取以下值：
openbsd、netbsd、freebsd、4_4bsd、linux、svr4、esix、solaris、irix、sco、dell、ncr、lynxos、vxworks、psos、qnx、u-boot、rtems、artos

* -T 指定映象类型，可以取以下值：
standalone、kernel、ramdisk、multi、firmware、script、filesystem

* -C 指定映象压缩方式，可以取以下值：
none 不压缩
gzip 用gzip的压缩方式
bzip2 用bzip2的压缩方式

* -a 指定映象在内存中的加载地址，映象下载到内存中时，要按照用mkimage制作映象时，这个参数所指定的地址值来下载

* -e 指定映象运行的入口点地址，这个地址就是-a参数指定的值加上0x40（因为前面有个mkimage添加的0x40个字节的头）

* -n 指定映象名

* -d 指定制作映象的源文件 

我的script实例：
```
mkimage -A arm -T script -C none -n "boot image" -d boot.script boot.scr
```
