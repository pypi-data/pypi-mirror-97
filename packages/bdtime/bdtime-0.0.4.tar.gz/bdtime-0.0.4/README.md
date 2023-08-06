# bode's time model.
> 安装:  
>`pip install bdtime`

```
from bd_time import Time()
tt = Time()
tt.now(1)  # 输出当前运行的时间
tt.during(10)  # 检测运行时间是否在10秒内
tt.get_key_state('a')  # 检测'a'键是否按下
tt.stop('alt + a')      # 如果按下[Alt + a]键就推出

# 测试函数用, [2秒后]运行函数
@tt.run_f_with_sleep(2)
def f():
    ret = 'haha'
    return ret
print(f())

# 测试函数用, [5秒内]循环运行函数, 运行间隔为[1秒]
@tt.run_f_with_during((during_time=5, sleep_time=1)
def f():
    return keyboard.is_pressed('a') #-> True
f()

```