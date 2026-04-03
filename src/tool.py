import datetime
import time
def generate_timestamps(start_timestamp: int = None, step_hours: int = 4, count: int = 10):
        if start_timestamp is None:
            start_timestamp = int(time.time() * 1000)
            print(f"当前毫秒级时间戳: {start_timestamp}")
        """
        生成连续递减的时间戳列表
        参数:
            start_timestamp: 起始时间戳（毫秒）
            step_hours: 每次递减的小时数
            count: 生成的时间戳数量
        """
        # 将毫秒时间戳转换为datetime对象
        start_dt = datetime.datetime.utcfromtimestamp(start_timestamp / 1000)
        timestamps = []
        current_dt = start_dt
        for i in range(count):
            # 将当前时间转换为毫秒时间戳
            timestamp_ms = int(current_dt.timestamp() * 1000)
            timestamps.append(timestamp_ms)
            # 减去指定小时数
            current_dt = current_dt - datetime.timedelta(hours=step_hours)
        return timestamps

def now_timestamp():
    now = datetime.datetime.now()
    # 格式化输出：年-月-日 时:分:秒
    return now.strftime("%Y-%m-%d %H:%M:%S")