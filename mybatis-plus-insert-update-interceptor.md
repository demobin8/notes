### config
```
package cn.test.payment.config;

import com.baomidou.mybatisplus.extension.plugins.PaginationInterceptor;
import com.baomidou.mybatisplus.extension.plugins.PerformanceInterceptor;
import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.autoconfigure.condition.ConditionalOnMissingBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;
import org.springframework.context.annotation.Profile;

@Configuration
@MapperScan({"cn.test.**.mapper.**"})
public class MyBatisPlusConfig {

    @Bean
    @ConditionalOnMissingBean({PaginationInterceptor.class})
    public PaginationInterceptor mybatisPaginationInterceptor() {
        return new PaginationInterceptor();
    }

    @Bean
    @Primary
    public InsertUpdateMetaObjectHandler insertUpdateMetaObjectHandler() {
        return new InsertUpdateMetaObjectHandler();
    }

    @Bean
    @Profile({"dev", "test", "default"})
    //开启可视化sql日志
    public PerformanceInterceptor performanceInterceptor() {
        PerformanceInterceptor performanceInterceptor = new PerformanceInterceptor();
        performanceInterceptor.setWriteInLog(true);
        return performanceInterceptor;
    }
}

```

### handler
```
package cn.test.payment.config;

import java.util.Date;

import org.apache.ibatis.reflection.MetaObject;

import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;

import cn.test.common.api.CurrentAccount;
import cn.test.common.utils.Func;
import cn.test.common.utils.WebUtil;


public class InsertUpdateMetaObjectHandler implements MetaObjectHandler {
    /**
     * 数据库默认的创建时间
     */
    private static final String CREATE_TIME = "createTime";
    /**
     * 创建人
     */
    private static final String CREATE_USER = "createUser";
    /**
     * 数据库默认的更新时间
     */
    private static final String UPDATE_TIME = "updateTime";
    /**
     * 更新人
     */
    private static final String UPDATE_USER = "updateUser";

    @Override
    public void insertFill(MetaObject metaObject) {
        Object fieldValByName = getFieldValByName(CREATE_TIME, metaObject);
        if (null == fieldValByName) {
            setFieldValByName(CREATE_TIME, new Date(), metaObject);
            setFieldValByName(UPDATE_TIME, new Date(), metaObject);
        }
        if (null == getFieldValByName(CREATE_USER, metaObject)) {
            CurrentAccount dto = WebUtil.getCurrentAccount(false);
            if (dto != null && Func.isNotBlank(dto.getUserCode())) {
                setFieldValByName(CREATE_USER, dto.getUserCode(), metaObject);
            }
        }

    }

    @Override
    public void updateFill(MetaObject metaObject) {
        setFieldValByName(UPDATE_TIME, new Date(), metaObject);
        if (null == getFieldValByName(UPDATE_USER, metaObject)) {
            CurrentAccount dto = WebUtil.getCurrentAccount(false);
            if (dto != null && Func.isNotBlank(dto.getUserCode())) {
                setFieldValByName(UPDATE_USER, dto.getUserCode(), metaObject);
            }
        }
    }
}

```
