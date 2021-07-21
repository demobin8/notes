```
package cn.test.aop.mq;

import io.opentracing.ActiveSpan;
import io.opentracing.Tracer;
import io.opentracing.util.GlobalTracer;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;

import cn.test.utils.TraceUtils;

@Component
@Slf4j
@Aspect
public class MqSkyWalkingAspect {

    @Pointcut("@annotation(org.springframework.amqp.rabbit.annotation.RabbitListener) " +
            "|| @annotation(org.springframework.amqp.rabbit.annotation.RabbitHandler)")
    public void pointCut(){
    }

    @Around(value = "pointCut()")
    public Object doAround(ProceedingJoinPoint pjp) throws Throwable {
    
        String methodName = pjp.getSignature().getName();
        String typeName = pjp.getSignature().getDeclaringTypeName();

        //create trace span
        Tracer tracer = GlobalTracer.get();
        ActiveSpan span = tracer.buildSpan("rabbitMq.method").startActive();

        //get traceId
        String traceId = TraceUtils.getTraceId();
        MDC.put("traceId", traceId);
        
        span.setTag("rabbitMq.method", typeName + "#" + methodName);
        log.info("mq method：{}", typeName + "#" + methodName);
        
        try {
          return pjp.proceed();
        } catch (Throwable e){
            span.setTag("error", e.getMessage());
            throw e;
        }  finally {
            span.deactivate();
        }
    }

}
```
