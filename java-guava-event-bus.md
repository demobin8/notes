### event dto
```
@Data
@Builder
public class PaymentEvent {

    private String orderId;

}

```
### post
```
paymentEventBus.post(PaymentEvent.builder().orderId(dto.getRefRequestCode()).build());
```
### listener
```
@Slf4j
@Component
@SuppressWarnings("UnstableApiUsage")
public class PaymentEventListener {

    @Resource
    private PaymentService paymentService;

    @Subscribe
    public void handler(PaymentEvent event) {

        paymentService.execute(event);

    }

}

```
### event bus
```
@Component
@SuppressWarnings("UnstableApiUsage")
public class PaymentEventBus implements InitializingBean {

    // 开一个线程，异步处理（也可以不开新线程）
    private static final Executor executor = command -> new Thread(command, "PaymentEventThread").start();

    /**
     * event bus
     */
    private static final AsyncEventBus EVENT_BUS = new AsyncEventBus("paymentEventBus", executor);

    @Resource
    private PaymentEventListener paymentEventListener;

    @Resource
    private PaymentCallbackEventListener paymentCallbackEventListener;

    /**
     * pub event
     *
     * @param event e
     */
    public final void post(Object event) {
        EVENT_BUS.post(event);
    }

    @Override
    public void afterPropertiesSet() {
        EVENT_BUS.register(paymentEventListener);
        EVENT_BUS.register(paymentCallbackEventListener);
    }
}
```
### config
```
@Configuration
@SuppressWarnings("UnstableApiUsage")
public class GuavaEventConfig {
    @Bean
    public EventBus eventBus() {
        return new EventBus();
    }
}
```
