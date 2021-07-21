### install php with php-gd with gd-jpeg support[fix:400:Unknown Error, open debug to trace]
`./configure --with-gd --with-jpeg-dir=/usr/lib64`

[if gd.so not install auto , cd path-to-php/ext/gd and execute ./configure && make && make install]

`yum install autoconf libxml2-devel libpng-devel libjpeg-devel gcc-c++`
### start server
`php -S 127.0.0.1:9000 -t ./ &`


### crack limit
1. beautified ckfinder.js
2. js decode using function S()
3. modify ckfinder-beautified-decoded.js:19807,change This is a demo version of CKFinder 3
vim search /function i\(\)\{h to modify or
```
//t[S("\x13ypedy~\x7f")]=[S("9jVSI"),S("!OU"),"e",S("\x1b|}uw"),S("\x1dl\x7fTUCE@"),S("=U\\"),S(")melCHB_H"),"7"][S("\val~")](n)[S("8SURR")](" ")
t['message'] = "Hello World",
```
4. remove setInterval
vim search /
```
```
