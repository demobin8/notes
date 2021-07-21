> 以前写C的时候，充满了未知。。。

### warning: suggest parentheses around ‘+’ inside ‘>>’

跟踪警告信息，可知表达式
```
(MAX_SUPPORT_CNU*MAX_CNU_PORT+4)>>3+2
```
在GCC中会有警告，更改如下
```
((MAX_SUPPORT_CNU*MAX_CNU_PORT+4)>>3)+2
```

### warning: assignment from incompatible pointer type

意思是类型不匹配

示例如下
```
typedef struct _linknode{
    char name[8];
    struct linknode *next;
}linknode;

typedef struct linknode{
    char name[8];
    struct linknode *next;

}linknode;
```

一级指针指向二级指针也会出这个警告 可以忽略也可以强制转换一下 如

```
int *p;

int a[][3];

p = a;

p = (int*)a;
```
