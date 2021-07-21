### 动态sql
#failed#
$plain sql$
### situation
在plsql中执行正确，代码中执行报列名无效错误
### reason
ibatis会缓存列名，动态列名需要加入参数remapResults=true
```
<select id="getStatistics" parameterClass="java.util.HashMap" resultClass="java.util.HashMap" remapResults="true"> 
************ 
</select>
```
