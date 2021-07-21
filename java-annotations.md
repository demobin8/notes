### lambok

@Data - 为所有属性提供get、set方法，提供enqual、tostring方法等

@Getter - 为标注的属性提供get

@Setter - 为标注的属性提供set

@Log4j - 为类提供一个名为log的Log4j方法

@NoArgsConstructor - 为类提供一个无参构造方法

@AllArgsConstructor - 为类提供一个全参构造方法

@Builder

### mapstruct

@Mapper - 映射接口

@Mappings - 字段集合

@Mapping - 字段

### swagger

@EnableSwagger2- 开启swagger

@ApiModel - 数据模型描述

@ApiProperty - 数据模型字段说明

@Api - 接口，一般对应大的路由

@ApiOperation - 命令，对应路由下的路由

@ApiReponses - 接口返回的code集合，用于异常code的处理

@ApiReponse - 接口返回的code

@ApiParam - 接口的请求参数

### springframework

@Configuration - Ioc容器

@Bean - 注册bean

@Scope - 作用域 singleton、prototype、request、session、global session

@Autowired - 注入

@Qualified - 结合@Autowired将注入从byType改为byName

@Resource -

@Inject -

@Component - 通用组件

@Async - 异步调用

@EnableAsync -

@EnableAutoConfiguration

@EnableConfigurationProperties

@EnableCaching

@EnableRedisHttpSession

@Scheduled - 计划任务cron、fixDelay、fixRate

@EnableScheduling

@Entity - 实体bean

@ComponentScan - 扫描

@SpringBootApplication - = @Configuration + @EnableAutoConfiguration + @ComponentScan

@ImportResource - 加载配置文件

@Aspect - 切面

@Pointcut("within(org.worldlinking.qpm.controller..*)")

@AfterThrowing(pointcut = "controllerPointcut()", throwing = "e")

@Before("controllerPointcut()")

@Around

@AfterReturning(returning = "ret", pointcut = "controllerPointcut()")

@Transactional(propagation = Propagation.REQUIRED,isolation = Isolation.DEFAULT,timeout=36000,rollbackFor=Exception.class)

@RefreshScope - 热部署

### springcloud注解

@EnableConfigServer - 配置中心

@EnableEurekaServer - 注册中心

@EnableDiscoveryClient - 服务发现

@EnableCircuitBreaker - 熔断

@HystrixCommand - 熔断

### MVC注解

@Service - 业务层组件

@Repository - 持久层组建

@Controller - 控制层组件

@RestController - RESTful风格控制层组件

@ControllerAdvice - Controller层全局处理器

@RestControllerAdvice - Controller层全局处理器

@RequestMapping - 请求映射

@GetMapping - GET方法映射

@PostMapping - POST方法映射

@PutMapping - PUT方法映射

@ResponseBody - 响应json

@RequestBody - 请求json

@PathVariable

@RequestParam - 请求参数

@CookieValue -

@CrossOrigin - 跨域

@HttpEntity - 访问请求和响应的包头

@Path -

@Method -

@Accept

@Content-Type

@Produces -

@Cosumers

### java

@Override - 重写

@Deprecated - 已过期

@Suppvisewarnings - 抑制告警

@PostConstruct - servlet启动执行一次-用于初始化数据

### javax

@NotNull

@XmlTransient

@Transient
