### numpy.flatten
flatten拉伸 返回拷贝

### numpy.ravel
ravel拉伸　返回视图

### numpy.square
square平方

### numpy.sqrt
square root平方根

### numpy.power
power乘方

### numpy.inf
infinity无限大

### numpy.cumsum
cumulation sum累加
```
>>> np.cumsum([[1, 2, 3], [2, 3, 4]], axis=0)
array([[1, 2, 3],
       [3, 5, 7]])
>>> np.cumsum([[1, 2, 3], [2, 3, 4]], axis=1)
array([[1, 3, 6],
       [2, 5, 9]])
```

### numpy.dot
dot点乘
```
>>> np.dot(3, 4)
12
>>> np.dot([[1, 0], [0, 1]], [[1, 2], [3, 4]])
array([[1, 2],
       [3, 4]])
```

### numpy.prod
product乘，指定轴
```
>>> np.prod([[1., 2.],[3., 4.]], axis=1)
array([  2.,  12.])
```

### numpy.cumprod
cumulation product累乘
```
>>> np.cumprod([1, 2, 3], axis=0)
array([1, 2, 6])
>>> np.cumprod([[1, 2, 3], [2, 3, 4]], axis=1)
array([[ 1,  2,  6],
       [ 2,  6, 24]])
```

### numpy.transpose
transpose返回转置矩阵
```
>>> numpy.transpose([[1, 2, 3], [4, 5, 6]])
array([[1, 4],
       [2, 5],
       [3, 6]])
```

### numpy.conj
conjugate返回共轭矩阵
```
>>> np.conjugate(1 + 2j)
(1-2j)
>>> x = np.eye(2) + 1j * np.eye(2)
>>> np.conjugate(x)
array([[ 1.-1.j,  0.-0.j],
       [ 0.-0.j,  1.-1.j]])
```

### numpy.inv
inverse返回逆矩阵，互逆矩阵满足dot(Ａ, Ａinv) = dot(Ａinv, Ａ) = eye(a.shape[0])
```
>>> numpy.linalg.inv([[1, 2], [3, 4]])
array([[-2. ,  1. ],
       [ 1.5, -0.5]])
```

### numpy.diag
diagonal返回主对角线上的元素为一个一维数组，或者转换一个一维数组到方阵
```
>>> numpy.diag((1, 2, 3))
array([[1, 0, 0],
       [0, 2, 0],
       [0, 0, 3]])
>>> numpy.diag([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
array([1, 3, 5])
```

### linalg
linear algebra线性代数库

### numpy.linalg.det
determinant计算矩阵行列式(数学上写做det(A)或者|A|，是取自不同行不同列的n个元素的乘积的代数和)
二阶行列式(主对角线的乘积减去副对角线的乘积)
```
>>> numpy.linalg.det([[1, 2],[2,3]])
-1.0
>>> numpy.linalg.det([[2, 2],[2,3]])
2.0
```

### numpy.trace
trace返回矩阵的迹(即矩阵的主对角线上各元素的和)
```
>>> numpy.trace([[1, 2, 3], [2, 3, 4], [3, 4, 5]])
9
```

### numpy.eig
eigen返回矩阵的特征值和特征向量
```
>>> numpy.linalg.eig(numpy.diag((1, 2, 3)))
(array([ 1.,  2.,  3.]), array([[ 1.,  0.,  0.],
       [ 0.,  1.,  0.],
       [ 0.,  0.,  1.]]))
```

### numpy.linalg.norm
norm范数记做||A||，原型norm(x, ord=None, axis=None, keepdims=False)

```
>>> A = numpy.array([1, 2])
>>> numpy.linalg.norm(A)
2.2360679774997898
>>> numpy.linalg.norm(A, 1)
3.0
>>> numpy.linalg.norm(A, 2)
2.2360679774997898
>>> numpy.linalg.norm(A, numpy.inf)
2.0
```

### numpy.zeros
```
>>> np.zeros(10)
array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
```

### numpy.reshape
```
>>> np.reshape([1, 2, 3, 4, 5, 6], (2, 3))
array([[1, 2, 3],
       [4, 5, 6]])
```

### numpy.arange
```
>>> np.arange(0,1,0.1)
array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9])
```

### numpy.linspace
```
>>> np.linspace(0, 1, 12)
array([ 0.        ,  0.09090909,  0.18181818,  0.27272727,  0.36363636,
        0.45454545,  0.54545455,  0.63636364,  0.72727273,  0.81818182,
        0.90909091,  1.        ])
```

### numpy.fromstring
```
>>> np.fromstring('abcdefgh', dtype=np.int8)
array([ 97,  98,  99, 100, 101, 102, 103, 104], dtype=int8)
```

### numpy.savetxt
```
np.savetxt('a.txt', A)
```

### numpy.loadtxt
```
np.loadtxt('a.txt')
```

