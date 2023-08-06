# bode's time model.
> bd_time

```
from bd_time import Time()
tt = Time()
tt.now(1)  # 输出当前运行的时间
tt.during(10)  # 检测运行时间是否在10秒内
tt.get_key_state('a')  # 检测'a'键是否按下
tt.stop_alt('a')      # 如果按下[Alt + a]键就推出
```