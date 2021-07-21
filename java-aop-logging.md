### config
```
package cn.test.config;

import cn.test.aop.logging.LoggingAspect;
import org.springframework.aop.aspectj.AspectJExpressionPointcutAdvisor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class ApiLogConfig {

    @Value("${pointcut.property:within(cn.test.*.controller..*)}")
    private String pointcut;

    @Bean
    public AspectJExpressionPointcutAdvisor configurableAdvisor() {
        AspectJExpressionPointcutAdvisor advisor = new AspectJExpressionPointcutAdvisor();
        advisor.setExpression(pointcut);
        advisor.setAdvice(new LoggingAspect());
        return advisor;
    }
}

```

### interceptor
```
package cn.test.aop.logging;

import cn.test.utils.TraceUtils;

import com.google.common.base.Stopwatch;
import lombok.extern.slf4j.Slf4j;
import org.slf4j.MDC;
import org.aopalliance.intercept.MethodInterceptor;
import org.aopalliance.intercept.MethodInvocation;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

import javax.servlet.http.HttpServletRequest;
import java.util.Arrays;

/**
 * @author demobin
 */
@Slf4j
public class LoggingAspect implements MethodInterceptor {

    static final ThreadLocal<Stopwatch> STOPWATCH_THREAD_LOCAL = new ThreadLocal<>();

    @Override
    public Object invoke(MethodInvocation methodInvocation) throws Throwable {
        STOPWATCH_THREAD_LOCAL.set(Stopwatch.createStarted());
        ServletRequestAttributes attributes = (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();
        String traceId = TraceUtils.getTraceId();
        MDC.put("traceId", traceId);
        if (attributes != null) {
            HttpServletRequest request = attributes.getRequest();
            log.info("request url: {}", request.getRequestURL().toString());
            log.info("request method: {}", request.getMethod());
            log.info("request params: {}", Arrays.toString(methodInvocation.getArguments()));
            log.info("request ip: {}", request.getRemoteAddr());
            log.info("request user agent: {}", request.getHeader("User-Agent"));
            log.info("request Accept-Language: {}", request.getHeader("Accept-Language"));
        }
        else{
            log.error("ServletRequestAttributes attributes null");
        }
        Object result = methodInvocation.proceed();
        try{
            log.info("request time cost: {}", STOPWATCH_THREAD_LOCAL.get());
        } catch (Exception e) {
            log.error("thread local get failed");
        } finally {
            STOPWATCH_THREAD_LOCAL.remove();
        }
        log.info("request ret: {}", result);
        return result;
    }

}
```
