# 装饰器
import keyboard
from functools import wraps


def run_f_with_during(during_time=3, sleep_time=1, break_key='alt + s'):
    tt = Time()
    def decorator_name(testf):
        @wraps(testf)
        def decorated(*args, **kwargs):
            def circulate_f(*args, **kwargs):
                ret = None

                def setBreakFlag(tt):
                    tt.break_flag = 1
                    print(f'用户手动中断! --------------- 总运行时间: [{tt.now(2)}/{during_time}] 秒')

                keyboard.add_hotkey(break_key, lambda:  setBreakFlag(tt))

                run_times = 0
                while tt.during(during_time):
                    run_times += 1
                    if tt.break_flag:
                        break

                    tt.sleep(sleep_time)

                    ret = testf(*args, **kwargs)
                    print(f'第 [{run_times}] 次运行的返回值为: [{ret}]. ------------- 总运行时间 :[{tt.now(2)}/{during_time}] 秒, ')        # 0改为int类型!

                keyboard.remove_hotkey(break_key)
                return ret
            return circulate_f(*args, **kwargs)
        return decorated
    return decorator_name