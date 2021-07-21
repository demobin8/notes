> 多级缓存的代码太多写入md似乎太长了。。。分类后再放吧。。。

### pom.xml、application.properties
pom.xml
```
...
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-data-redis</artifactId>
</dependency>
...
```
application.properties或者nacos配置
```
...
略
```

### @EnableCaching
在启动类添加注解开启缓存

### RedisConfig
```
package cn.test.cache.config;

import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.cache.CacheManager;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.cache.RedisCacheConfiguration;
import org.springframework.data.redis.cache.RedisCacheManager;
import org.springframework.data.redis.connection.RedisConnectionFactory;
import org.springframework.data.redis.connection.jedis.JedisConnectionFactory;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.data.redis.serializer.StringRedisSerializer;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;


@Configuration
public class RedisConfig {

    @Bean
    @ConditionalOnMissingBean(name = "redisTemplate")
    public RedisTemplate<String, Object> redisTemplate(RedisConnectionFactory redisConnectionFactory) {

        Jackson2JsonRedisSerializer<Object> jackson2JsonRedisSerializer = new Jackson2JsonRedisSerializer<Object>(Object.class);
        
        ObjectMapper om = new ObjectMapper();
        
        om.setVisibility(PropertyAccessor.ALL, JsonAutoDetect.Visibility.ANY);
        om.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
        
        jackson2JsonRedisSerializer.setObjectMapper(om);
        
        StringRedisSerializer stringRedisSerializer = new StringRedisSerializer();
        
        RedisTemplate<String, Object> template = new RedisTemplate<String, Object>();
        
        template.setConnectionFactory(redisConnectionFactory);
        template.setKeySerializer(stringRedisSerializer);
        template.setValueSerializer(jackson2JsonRedisSerializer);
        template.setHashKeySerializer(stringRedisSerializer);
        template.setHashValueSerializer(jackson2JsonRedisSerializer);
        
        template.afterPropertiesSet();
        
        return template;
    }

    @Bean
    @ConditionalOnMissingBean(StringRedisTemplate.class)
    public StringRedisTemplate stringRedisTemplate(RedisConnectionFactory redisConnectionFactory) {
        
        StringRedisTemplate template = new StringRedisTemplate();
        template.setConnectionFactory(redisConnectionFactory);
        
        return template;
    }


    @Bean
    public CacheManager cacheManager(RedisConnectionFactory redisConnectionFactory) {
        RedisCacheConfiguration defaultCacheConfig = RedisCacheConfiguration.defaultCacheConfig()
                // 默认没有特殊指定的
                .entryTtl(Duration.ofHours(12))
                .computePrefixWith(cacheName -> "caching:" + cacheName);

        // 针对不同cacheName，设置不同的过期时间
        Map<String, RedisCacheConfiguration> initialCacheConfiguration = new HashMap<String, RedisCacheConfiguration>() {
            private static final long serialVersionUID = 5501079579657911048L;
            {
                put("test-order", RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofHours(12)));
            }
        };

        return RedisCacheManager.builder(redisConnectionFactory)
                // 默认配置（强烈建议配置上）。  比如动态创建出来的都会走此默认配置
                .cacheDefaults(defaultCacheConfig)
                // 不同cache的个性化配置
                .withInitialCacheConfigurations(initialCacheConfiguration)
                .build();
    }
}

```
### annotation使用
```

@Mapper
@CacheConfig(cacheNames = "order-detail")
public interface OrderDetailMapper {

	...
    
    @Select("select * from order_detail where id = #{id}")
    @Cacheable(key = "#p0") 
    OrderDetail findById(@Param("id") String id);
    
    @CachePut(key = "#p0")
    @Update("update order_detail set status = #{status} where id = #{id}")
    void updataStatusById(@Param("id")String id, @Param("status")String status);
    
    //如果指定为 true，则方法调用后将立即清空所有缓存
    @CacheEvict(key ="#p0", allEntries=true)
    @Delete("delete from order_detail where id = #{id}")
    void deleteById(@Param("id")String id);
	
	...
    
}
```
