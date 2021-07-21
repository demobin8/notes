### pom.xml引用guava包
```
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>20.0</version>
</dependency>
```
### 使用
```
private static final int insertions = 1000000; //100w

private static void test() {
    //初始化一个存储string数据的布隆过滤器，初始化大小100w,不能设置为0
    BloomFilter<String> bf = BloomFilter.create(Funnels.stringFunnel(Charsets.UTF_8), insertions, 0.001);
    //初始化一个存储string数据的set，初始化大小100w
    Set<String> sets = new HashSet<>(insertions);
    //初始化一个存储string数据的set，初始化大小100w
    List<String> lists = new ArrayList<String>(insertions);

    //向三个容器初始化100万个随机并且唯一的字符串---初始化操作
    for (int i = 0; i < insertions; i++) {
        String uuid = UUID.randomUUID().toString();
        bf.put(uuid);
        sets.add(uuid);
        lists.add(uuid);
    }

    int wrong = 0;//布隆过滤器错误判断的次数
    int right = 0;//布隆过滤器正确判断的次数
    for (int i = 0; i < 10000; i++) {
        String test = i % 100 == 0 ? lists.get(i / 100) : UUID.randomUUID().toString();//按照一定比例选择bf中肯定存在的字符串
        if (bf.mightContain(test)) {
            if (sets.contains(test)) {
                right++;
            } else {
                wrong++;
            }
        }
    }

    System.out.println("=================right=====================" + right);//100
    System.out.println("=================wrong=====================" + wrong);
}
```
