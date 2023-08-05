from datetime import datetime
import time
import random
from concurrent.futures import ProcessPoolExecutor, wait


def job3(msg):
    def run():
        print('[Child-{}][{}]'.format(msg, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))

    # 模拟一个耗时任务
    time.sleep(random.randint(1, 5))
    run()


if __name__ == '__main__':
    # 进程池大小
    pool_size = 2
    # 进程池
    pool = ProcessPoolExecutor(pool_size)
    # 添加任务, 假设我们要添加6个任务，由于进程池大小为2，每次能只有2个任务并行执行，其他任务排队
    tasks = [pool.submit(job3, i) for i in range(6)]
    ### 等待任务执行完, 也可以设置一个timeout时间
    wait(tasks)
    #
    print('main process done')