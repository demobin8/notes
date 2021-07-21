### config
ThreadPoolConfig
```
package cn.test.config;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

import java.util.concurrent.Executor;
import java.util.concurrent.ThreadPoolExecutor;

@Configuration
@EnableAsync
@Slf4j
public class ThreadPoolConfig {

    @Value("${sequence.thread.pool.corePoolSize:5}")
    private int corePoolSize;

    @Value("${sequence.thread.pool.maxPoolSize:10}")
    private int maxPoolSize;

    @Value("${sequence.thread.pool.queueCapacity:10000}")
    private int queueCapacity;

    @Value("${sequence.thread.pool.threadNamePrefix:SettlementTaskThread-}")
    private String threadNamePrefix;

    @Bean(name = "asyncThreadPoolTaskExecutor")
    public Executor executor(){

        ThreadPoolTaskExecutor threadPoolTaskExecutor = new ThreadPoolTaskExecutor();

        threadPoolTaskExecutor.setCorePoolSize(corePoolSize);
        threadPoolTaskExecutor.setMaxPoolSize(maxPoolSize);
        threadPoolTaskExecutor.setQueueCapacity(queueCapacity);
        threadPoolTaskExecutor.setThreadNamePrefix(threadNamePrefix);
        threadPoolTaskExecutor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());

        threadPoolTaskExecutor.initialize();
        return threadPoolTaskExecutor;
    }

}

```
### execute
```
...
    @Resource(name = "asyncThreadPoolTaskExecutor")
    private ExecutorService executorService;
...

        executorService.execute(() -> {
            doBiz();
        });
    
```
