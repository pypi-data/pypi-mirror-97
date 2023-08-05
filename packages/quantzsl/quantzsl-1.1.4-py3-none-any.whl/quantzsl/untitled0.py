import time
from multiprocessing import Process


def run_forever():
    while 1:
        print(time.time())
        time.sleep(2)


def main():
    p = Process(target=run_forever)
    p.start()
    print('start a process.')
    time.sleep(10)
    if p.is_alive:
        # stop a process gracefully
        p.terminate()
        print('stop process')
        p.join()


if __name__ == '__main__':
    p = Process(target=run_forever)
    p.start()
    print('start a process.')
    time.sleep(10)
    if p.is_alive:
        # stop a process gracefully
        p.terminate()
        print('stop process')
        p.join()