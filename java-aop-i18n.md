```
@Slf4j
@Aspect
@Configuration
public class RequestI18nAspect {

    @AfterReturning(pointcut =
            "execution("(@within(org.springframework.stereotype.Controller) || " +
                    "@within(org.springframework.web.bind.annotation.RestController))",
            returning = "object"
    )
    public void afterReturn(Object object) throws Throwable {
	
        if (object instanceof R) {
		
            R result = (R) object;
            int code = result.getCode();
            if (ResultCode.SERVER_ERROR.getCode() == code) {
                return;
            }
			
            String msg = result.getMsg();
            String i18n = I18nUtil.getNacosI18n(String.valueOf(code), msg);

            result.setMsg(i18n);
        }
    }

}
```
