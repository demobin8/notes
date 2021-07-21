### list->map
```
Map<String, String> map = list.stream().collect(Collectors.toMap(Person::getId, Person::getName));
```
有重复key
```
Map<String, BusinessInfo> businessInfoMap = businessInfoList.stream().collect(Collectors.toMap(BusinessInfo::getMerchantId, businessInfo -> businessInfo, (v1, v2) -> v2));
```
### 排序
```
userFeedList.sort(Comparator.comparing(UserFeed::getLikeCount).reversed());
```
### 分组
```
Map<String, List<Payment>> paymentMap = paymentList.stream().collect(Collectors.groupingBy(Payment::getPaymentCode));
```
### 过滤
```
List<BillVO> billList = paymentList.stream().map(Payment::getPaymentCode).filter(key -> !key.startsWith("XXX")).map(key -> buildBillVO(key)).collect(Collectors.toList());
```
### forEach
```
rst.getRecords().forEach(item -> item.setAmount(AmountUtils.getActualAmount(item.getAmount())));
```
### 求和
```
Long total = transactionList.stream().map(Transaction::getAmount).reduce(0L, Long::sum);
```
### join
```
String bills = billList.stream().map(Bill::getBillCode).collect(Collectors.joining(", "));
```
### int[] -> List
```
List<Integer> list = Arrays.stream(data).boxed().collect(Collectors.toList());
```
### List -> int[]
```
int[] data = list.stream().mapToInt(Integer::valueOf).toArray();
```
