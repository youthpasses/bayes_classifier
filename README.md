# bayes_classifier
（文本分类）朴素贝叶斯实现的新闻分类
新闻共分7类，新闻信息在此采集：
1 财经
http://finance.qq.com/l/201108/scroll_17.htm
2 科技
http://tech.qq.com/l/201512/scroll_02.htm
3 汽车
http://auto.qq.com/l/201512/scrollnews_02_2.htm
4 房产
http://gd.qq.com/l/house/fcgdxw/more_7.htm
5 体育
http://sports.qq.com/l/201512/scrollnews_01_2.htm
6 娱乐
http://ent.qq.com/l/201108/scrollents_18_2.htm
7 其他
http://news.ifeng.com/listpage/16873/1/1/46629832/46630185/list.shtml

##原理
贝叶斯定理的公式为：
P(B|A) =  (P(A|B)P(B))/(P(A))
	如果应用到文本分类中，我们假设有类别集合 C = {C_1,C_2,C_3,C_4,C_5,C_6,C_7}，那么文档D属于类别C_i的概率就可以使用贝叶斯公式计算：
P(C_i│D)=  (P(D│C_i )P(C_i ))/P(D)   =  (P(C_i))/(P(D))*P(D|C_i)
因为对每一个分类来说，P(C_i)恒等于1/7，P(D)都相等，所以若要比较C1、C2…C7的大小，只需计算P(D|C_i)即可。
假设文档D的特征集合X有n个特征：X = {x_1,x_2…x_n} ,那么P(D|C_i)的计算公式是：
P(D|Ci) =P(x_1 |Ci)P(x_2 |Ci)…P(x_3 |Ci) = ∏_(j = 1)^n▒〖P(x_j |Ci)〗
	令
P(C_k |D) =max{P(C_1 |D),P(C_2 |D)…P(C_7 |D)}
	那么，我们就判断文档D属于类别C_k。

