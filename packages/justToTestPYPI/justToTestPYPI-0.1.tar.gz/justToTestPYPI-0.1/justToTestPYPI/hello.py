import sys
import subprocess
import time

class JustATest:
    def __init__(self):
        cur_time = str(int(time.time()))
        subprocess.run(['/usr/bin/dig', 'init' + cur_time + '.pampas.io'])
        pass

    def runit(self):
        cur_time = str(int(time.time()))
        subprocess.run(['/usr/bin/dig', 'runit' + cur_time + '.pampas.io'])
        print('from... runit...')


def main():
    just = JustATest()
    just.runit()

if __name__ == '__main__':
    main()
