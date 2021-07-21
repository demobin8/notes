# SIGHAN测评
### 1. CIPS-SIGHAN测评及资源下载地址
CIPS-SIGHAN中文名：中国中文信息学会和国际计算语言学协会中文处理特别兴趣组

资源下载地址[SIGHAN DATA](http://sighan.cs.uchicago.edu/bakeoff2005/data/icwb2-data.zip)
### 2. 自带最大匹配分词方法演示
`cd scripts`
`./mwseg.pl ../gold/pku_training_words.utf8 < ../testing/pku_test.utf8 > pku_seg.utf8`

第一个参数是词表文件，第二个参数是待分词语料，最后是结果输出

`./score ../gold/pku_training_words.utf8 ../gold/pku_test_gold.utf8 pku_seg.utf8 > score.txt`

第一个参数是词表文件，第二个参数是标准分词的语料，第三个是分词结果，最后是得分输出
### 3. 说明
从标准分词的语料来看，个人觉得这个‘标准’很不标准，如‘中央电视台’它分词为‘中央/电视台’；‘香港特别行政区同胞’它分词为‘香港/特别/行政区/同胞’。

所以，比较得分可以使用，但是分词标准语料应该重新整理。
### 4. 关于Recall与Precision和F值
* Recall我们称之为查全率，也有叫它召回率的，但是我认为查全率更形象一点，体现了分出的标准词在所有标准词中的占比。
  查全率=算法分出的标准词总数/标准词总数
* Precision称之为准确率，体现了分出的标准词在分出的所有词中的占比。
  准确率=算法分出的标准词总数/算法分词总数
* F1值，可以看做是Recall和Precision的加权平均。
* F2值，也是Recall和Precision的加权平均，但是Precision的权重高于Recall。
* F0.5值，同上，但Recall的权重高于Precision。
