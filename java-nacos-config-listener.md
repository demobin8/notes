### NacosListener
```
import java.util.HashMap;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationListener;
import org.springframework.stereotype.Component;

import com.purgeteam.dynamic.config.starter.event.ActionConfigEvent;

import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class NacosListener implements ApplicationListener<ActionConfigEvent> {


    private static final String KEY = "config.key";

    @Override
    public void onApplicationEvent(ActionConfigEvent event) {
        Map<String, HashMap> update = event.getPropertyMap();
        HashMap update = update.get(KEY);
        if (update != null) {
            String before = (String)update.get("before");
            String after = (String)update.get("after");
            log.info("config update, key: {}, before: {}, after: {}", before, after);
			      doBiz();
        }

    }
}
```
