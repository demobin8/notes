### config
```
@Configuration
public class AuditMqConfig {
    @Bean
    public Exchange auditExchange() {
        return ExchangeBuilder.fanoutExchange(AuditMqConstant.AUDIT_EXCHANGE).durable(true).build();
    }

    @Bean
    public Queue auditQueue() {
        return QueueBuilder.durable(AuditMqConstant.AUDIT_QUEUE).build();
    }

    @Bean
    public Binding bind() {
        return BindingBuilder.bind(auditQueue()).to(auditExchange()).with(AuditMqConstant.AUDIT_KEY).noargs();
    }
}

```
### service
```
@Service
public class AuditTradeCreateSuccessMqService  extends AbstractRabbitFanoutSenderService<AuditDTO> {
    @Override
    protected String bindingKey() {
        return AuditMqConstant.AUDIT_KEY;
    }

    @Override
    protected String exchange() {
        return AuditMqConstant.AUDIT_EXCHANGE;
    }
}
```
### lisener
```
@Service
@Slf4j
@ConditionalOnExpression("!'${env}'.equals('local')")
public class AuditListener {

    @RabbitListener(queues = {AuditMqConstant.AUDIT_QUEUE}, containerFactory = ListenerSelector.MULTI_THREAD)
    public void auditListener(AuditDTO dto) throws Exception {
        Stopwatch stopwatch = Stopwatch.createStarted();
        log.info("audit mq listener start, params: {}",dto);

        service.execute(dto);

        stopwatch.stop();
        log.info("audit mq listener handler stop, cost：{}",stopwatch);
    }
}
```
### abstract service
direct
```
public abstract class AbstractDirectRabbitSenderService<T> implements MqSenderService<T> {
    protected Logger logger = LoggerFactory.getLogger(getClass());

    @Resource
    protected RabbitTemplate template;

    @Override
    public void send(T data) {
        logger.info("send message: {}", data.toString());
        sendMq(data, bindingKey(), exchange());
    }

    @Override
    public void send(T data, String bindingKey, String exchange) {
        logger.info("send message: {}", data.toString());
        sendMq(data, bindingKey, exchange);
    }

    protected void sendMq(T message, String bindingKey, String exchange) {
        this.template.convertAndSend(exchange, bindingKey, message);
    }

    protected abstract String bindingKey();

    protected abstract String exchange();

}
```
fanout
```
public abstract class AbstractRabbitFanoutSenderService<T> implements MqSenderService<T> {
    protected Logger logger = LoggerFactory.getLogger(getClass());

    @Resource
    protected RabbitTemplate template;

    @Override
    public void send(T data) {
        logger.info("send message: {}", data.toString());
        sendMq(data);
    }

    @Override
    public void send(T data, String bindingKey,String exchange) {
        if (StringUtils.isEmpty(bindingKey)) {
            send(data);
        } else {
            throw new RuntimeException("fanout dont need key");
        }
    }

    protected void sendMq(T message) {
        this.template.convertAndSend(fanout(), null, message);
    }
    
    protected abstract String fanout();
}
```
### Interface
```
public interface MqSenderService<T> {
    /**
     * send message
     *
     * @param paramT
     */
    void send(T paramT);

    /**
     * send message to queue
     *
     * @param paramT
     * @param bindingKey
     * @param exchange
     */
    void send(T paramT, String bindingKey, String exchange);

}
```
